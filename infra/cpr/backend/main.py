"""Infra-as-code for CPR stack."""
import datetime
import json
import os
from pathlib import Path

import pulumi
import pulumi_aws as aws
import pulumi_docker as docker

from cpr.deployment_resources.main import DeploymentResources, default_tag
from cpr.plumbing.main import Plumbing
from cpr.storage.main import Storage


class Backend:
    """Deploys all resources necessary for backend API to function."""

    def __init__(
        self,
        deployment_resources: DeploymentResources,
        plumbing: Plumbing,
        storage: Storage,
    ):
        # context has to be one level below 'backend' as backend Dockerfile references '../common'
        docker_context = Path(os.getcwd()) / ".."
        docker_context = docker_context.resolve().as_posix()
        backend_dockerfile = Path(os.getcwd()) / ".." / "backend" / "Dockerfile"
        backend_dockerfile = backend_dockerfile.resolve().as_posix()

        self.backend_image = docker.Image(
            "backend-docker-image",
            build=docker.DockerBuild(
                context=docker_context, dockerfile=backend_dockerfile
            ),
            # image_name=f"{backend_image_name}:{stack}",
            image_name=deployment_resources.ecr_repo.repository_url,
            skip_push=False,
            registry=deployment_resources.docker_registry,
        )

        dockerrun_aws_json_template = json.dumps(
            {
                "AWSEBDockerrunVersion": "1",
                "Image": {"Name": "%s"},
                "Ports": [{"ContainerPort": "8888"}],
            }
        )

        def fill_template(img):
            return dockerrun_aws_json_template % (img)

        dockerrun_file = self.backend_image.image_name.apply(fill_template)

        pulumi.export("dockerrun_file", dockerrun_file)

        def create_deploy_resource(manifest):
            # TODO delete this file if it exists
            with open("Dockerrun.aws.json", "w") as json_file:
                json_file.write(manifest)

            deploy_resource = aws.s3.BucketObject(
                "backend-beanstalk-docker-manifest",
                bucket=deployment_resources.deploy_bucket,
                key=datetime.datetime.today().strftime(
                    "%Y/%M/%d/%H:%M:%S/Dockerrun.aws.json"
                ),
                source=pulumi.asset.FileAsset("Dockerrun.aws.json"),
                tags=default_tag,
            )
            return deploy_resource

        deploy_resource = dockerrun_file.apply(create_deploy_resource)

        # create Elastic Beanstalk app
        backend_eb_app = aws.elasticbeanstalk.Application(
            "backend-beanstalk-application"
        )
        backend_app_version = aws.elasticbeanstalk.ApplicationVersion(
            "navigator-api-version",
            application=backend_eb_app,
            bucket=deployment_resources.deploy_bucket.id,
            key=deploy_resource.id,
            force_delete=True,
            tags=default_tag,
        )

        # Run CLI:
        # aws elasticbeanstalk list-available-solution-stacks
        solution_stack = aws.elasticbeanstalk.get_solution_stack_output(
            most_recent=True,
            name_regex=r"^64bit Amazon Linux 2 (.*) Docker(.*)$",
        )

        config = pulumi.Config()
        backend_secret_key = config.require_secret("backend_secret_key")
        opensearch_user = config.require("opensearch_user")
        opensearch_password = config.require_secret("opensearch_password")
        opensearch_url = config.require("opensearch_url")
        sendgrid_api_key = config.require("sendgrid_api_key")

        backend_eb_env = aws.elasticbeanstalk.Environment(
            "navigator-api-environment",
            application=backend_eb_app.name,
            version=backend_app_version,
            solution_stack_name=solution_stack.name,
            tags=default_tag,
            settings=[
                # nginx is default, but we'd need extra config for frontend?
                # aws.elasticbeanstalk.EnvironmentSettingArgs(
                #     namespace="aws:elasticbeanstalk:environment:proxy",
                #     name="ProxyServer",
                #     value="nginx"
                # ),
                aws.elasticbeanstalk.EnvironmentSettingArgs(
                    namespace="aws:autoscaling:launchconfiguration",
                    name="IamInstanceProfile",
                    value=plumbing.instance_profile.name,
                ),
                aws.elasticbeanstalk.EnvironmentSettingArgs(
                    namespace="aws:ec2:vpc",
                    name="VPCId",
                    value=plumbing.default_vpc.id,
                ),
                aws.elasticbeanstalk.EnvironmentSettingArgs(
                    namespace="aws:ec2:vpc",
                    name="Subnets",
                    value=plumbing.subnet_ids,
                ),
                # aws.elasticbeanstalk.EnvironmentSettingArgs(
                #     namespace="aws:ec2:vpc",
                #     name="ELBSubnets",
                #     value=subnet_ids,
                # ),
                aws.elasticbeanstalk.EnvironmentSettingArgs(
                    namespace="aws:elasticbeanstalk:environment",
                    name="ServiceRole",
                    value=plumbing.service_role.name,
                ),
                aws.elasticbeanstalk.EnvironmentSettingArgs(
                    namespace="aws:ec2:instances",
                    name="InstanceTypes",
                    value="t3.medium",  # https://aws.amazon.com/ec2/instance-types/
                ),
                aws.elasticbeanstalk.EnvironmentSettingArgs(
                    namespace="aws:autoscaling:launchconfiguration",
                    name="SecurityGroups",
                    value=plumbing.security_group.id,
                ),
                aws.elasticbeanstalk.EnvironmentSettingArgs(
                    namespace="aws:elasticbeanstalk:application",
                    name="Application Healthcheck URL",
                    value="/health",
                ),
                aws.elasticbeanstalk.EnvironmentSettingArgs(
                    namespace="aws:elasticbeanstalk:cloudwatch:logs",
                    name="StreamLogs",
                    value="true",
                ),
                aws.elasticbeanstalk.EnvironmentSettingArgs(
                    namespace="aws:elasticbeanstalk:cloudwatch:logs:health",
                    name="HealthStreamingEnabled",
                    value="true",
                ),
                aws.elasticbeanstalk.EnvironmentSettingArgs(
                    namespace="aws:elasticbeanstalk:healthreporting:system",
                    name="SystemType",
                    value="enhanced",
                ),
                aws.elasticbeanstalk.EnvironmentSettingArgs(
                    namespace="aws:autoscaling:launchconfiguration",
                    name="RootVolumeType",
                    value="gp2",
                ),
                aws.elasticbeanstalk.EnvironmentSettingArgs(
                    namespace="aws:autoscaling:launchconfiguration",
                    name="RootVolumeSize",
                    value="16",  # default is 8GB, but we're making space for pytorch
                ),
                # app env vars
                aws.elasticbeanstalk.EnvironmentSettingArgs(
                    namespace="aws:elasticbeanstalk:application:environment",
                    name="DATABASE_URL",
                    value=storage.backend_database_connection_url,
                ),
                aws.elasticbeanstalk.EnvironmentSettingArgs(
                    namespace="aws:elasticbeanstalk:application:environment",
                    name="SECRET_KEY",
                    value=backend_secret_key,
                ),
                aws.elasticbeanstalk.EnvironmentSettingArgs(
                    namespace="aws:elasticbeanstalk:application:environment",
                    name="PORT",
                    value="8888",
                ),
                aws.elasticbeanstalk.EnvironmentSettingArgs(
                    namespace="aws:elasticbeanstalk:application:environment",
                    name="OPENSEARCH_USER",
                    value=opensearch_user,
                ),
                aws.elasticbeanstalk.EnvironmentSettingArgs(
                    namespace="aws:elasticbeanstalk:application:environment",
                    name="OPENSEARCH_PASSWORD",
                    value=opensearch_password,
                ),
                aws.elasticbeanstalk.EnvironmentSettingArgs(
                    namespace="aws:elasticbeanstalk:application:environment",
                    name="OPENSEARCH_URL",
                    value=opensearch_url,
                ),
                aws.elasticbeanstalk.EnvironmentSettingArgs(
                    namespace="aws:elasticbeanstalk:application:environment",
                    name="OPENSEARCH_INDEX",
                    value="navigator",
                ),
                aws.elasticbeanstalk.EnvironmentSettingArgs(
                    namespace="aws:elasticbeanstalk:application:environment",
                    name="SENDGRID_API_KEY",
                    value=sendgrid_api_key,
                ),
            ],
        )

        pulumi.export("backend_eb_env", backend_eb_env.endpoint_url)
