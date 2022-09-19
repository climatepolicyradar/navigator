"""Infra-as-code for CPR stack."""
import datetime
import os
from pathlib import Path

import pulumi
import pulumi_aws as aws
import pulumi_docker as docker

from cpr.deployment_resources.main import DeploymentResources, default_tag
from cpr.plumbing.main import Plumbing
from cpr.storage.main import Storage

# for logging, see https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create_deploy_docker.container.console.html#docker-env-cfg.dc-customized-logging


class Backend:
    """Deploys all resources necessary for backend API to function."""

    def __init__(
        self,
        deployment_resources: DeploymentResources,
        plumbing: Plumbing,
        storage: Storage,
    ):
        target_environment = pulumi.get_stack()
        # get all config
        config = pulumi.Config()
        backend_secret_key = config.require_secret("backend_secret_key")
        opensearch_user = config.require_secret("opensearch_user")
        opensearch_password = config.require_secret("opensearch_password")
        opensearch_url = config.require_secret("opensearch_url")
        sendgrid_api_token = config.require_secret("sendgrid_api_token")
        sendgrid_from_email = config.require_secret("sendgrid_from_email")
        sendgrid_enabled = config.require_secret("sendgrid_enabled")

        # backend
        backend_docker_context = (
            (Path(os.getcwd()) / ".." / "backend").resolve().as_posix()
        )
        backend_dockerfile = (
            (Path(os.getcwd()) / ".." / "backend" / "Dockerfile").resolve().as_posix()
        )
        backend_image = docker.Image(
            f"{target_environment}-backend-docker-image",
            build=docker.DockerBuild(
                context=backend_docker_context,
                dockerfile=backend_dockerfile,
            ),
            image_name=deployment_resources.navigator_backend_repo.repository_url,
            skip_push=False,
            registry=deployment_resources.docker_registry,
        )

        backend_app_runner_app = aws.apprunner.Service(
            "cpr-backend",
            service_name="cpr-backend",
            source_configuration=aws.apprunner.ServiceSourceConfigurationArgs(
                auto_deployments_enabled=False,
                image_repository=aws.apprunner.ServiceSourceConfigurationImageRepositoryArgs(
                    image_configuration=aws.apprunner.ServiceSourceConfigurationImageRepositoryImageConfigurationArgs(
                        port="8000",
                    ),
                    image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest",
                    image_repository_type="ECR_PUBLIC",
                ),
            ),
            tags={
                "Name": "cpr-backend-service",
            },
        )

        # def create_deploy_resource(manifest):
        #     # TODO delete this file if it exists
        #     with open("docker-compose.yml", "w") as json_file:
        #         json_file.write(manifest)

        #     # DEBUG: set file as read-only
        #     # compose_path = Path("docker-compose.yml")
        #     # compose_path.chmod(0o444)

        #     deploy_resource = aws.s3.BucketObject(
        #         f"{target_environment}-backend-beanstalk-docker-manifest",
        #         bucket=deployment_resources.deploy_bucket,
        #         key=datetime.datetime.today().strftime(
        #             "%Y/%m/%d/%H:%M:%S/docker-compose.yml"
        #         ),
        #         source=pulumi.asset.FileAsset("docker-compose.yml"),
        #         tags=default_tag,
        #     )
        #     return deploy_resource

        # deploy_resource = docker_compose_file.apply(create_deploy_resource)

        # create Elastic Beanstalk app
        # backend_eb_app = aws.elasticbeanstalk.Application(
        #     f"{target_environment}-backend-beanstalk-application"
        # )
        # backend_app_version = aws.elasticbeanstalk.ApplicationVersion(
        #     f"{target_environment}-app-api-version",
        #     application=backend_eb_app,
        #     bucket=deployment_resources.deploy_bucket.id,
        #     key=deploy_resource.id,
        #     force_delete=True,
        #     tags=default_tag,
        # )

        # Run CLI:
        # aws elasticbeanstalk list-available-solution-stacks
        # solution_stack = aws.elasticbeanstalk.get_solution_stack_output(
        #     most_recent=True,
        #     name_regex=r"^64bit Amazon Linux 2 (.*) Docker(.*)$",
        # )
        # pulumi.export("solution_stack", solution_stack)

        # backend_eb_env = aws.elasticbeanstalk.Environment(
        #     f"{target_environment}-app-api-environ",
        #     application=backend_eb_app.name,
        #     version=backend_app_version,
        #     solution_stack_name=solution_stack.name,
        #     tags=default_tag,
        #     settings=[
        #         # nginx is default, but we'd need extra config for frontend?
        #         # aws.elasticbeanstalk.EnvironmentSettingArgs(
        #         #     namespace="aws:elasticbeanstalk:environment:proxy",
        #         #     name="ProxyServer",
        #         #     value="nginx"
        #         # ),
        #         aws.elasticbeanstalk.EnvironmentSettingArgs(
        #             namespace="aws:autoscaling:launchconfiguration",
        #             name="IamInstanceProfile",
        #             value=plumbing.instance_profile.name,
        #         ),
        #         aws.elasticbeanstalk.EnvironmentSettingArgs(
        #             namespace="aws:ec2:vpc",
        #             name="VPCId",
        #             value=plumbing.default_vpc.id,
        #         ),
        #         aws.elasticbeanstalk.EnvironmentSettingArgs(
        #             namespace="aws:ec2:vpc",
        #             name="Subnets",
        #             value=plumbing.subnet_ids,
        #         ),
        #         # aws.elasticbeanstalk.EnvironmentSettingArgs(
        #         #     namespace="aws:ec2:vpc",
        #         #     name="ELBSubnets",
        #         #     value=subnet_ids,
        #         # ),
        #         aws.elasticbeanstalk.EnvironmentSettingArgs(
        #             namespace="aws:elasticbeanstalk:environment",
        #             name="ServiceRole",
        #             value=plumbing.service_role.name,
        #         ),
        #         aws.elasticbeanstalk.EnvironmentSettingArgs(
        #             namespace="aws:ec2:instances",
        #             name="InstanceTypes",
        #             value="t3.large",  # https://aws.amazon.com/ec2/instance-types/
        #         ),
        #         aws.elasticbeanstalk.EnvironmentSettingArgs(
        #             namespace="aws:autoscaling:launchconfiguration",
        #             name="SecurityGroups",
        #             value=plumbing.security_group.id,
        #         ),
        #         aws.elasticbeanstalk.EnvironmentSettingArgs(
        #             namespace="aws:elasticbeanstalk:application",
        #             name="Application Healthcheck URL",
        #             value="/health",
        #         ),
        #         aws.elasticbeanstalk.EnvironmentSettingArgs(
        #             namespace="aws:elasticbeanstalk:cloudwatch:logs",
        #             name="StreamLogs",
        #             value="true",
        #         ),
        #         aws.elasticbeanstalk.EnvironmentSettingArgs(
        #             namespace="aws:elasticbeanstalk:cloudwatch:logs:health",
        #             name="HealthStreamingEnabled",
        #             value="true",
        #         ),
        #         aws.elasticbeanstalk.EnvironmentSettingArgs(
        #             namespace="aws:elasticbeanstalk:healthreporting:system",
        #             name="SystemType",
        #             value="enhanced",
        #         ),
        #         aws.elasticbeanstalk.EnvironmentSettingArgs(
        #             namespace="aws:autoscaling:launchconfiguration",
        #             name="RootVolumeType",
        #             value="gp2",
        #         ),
        #         aws.elasticbeanstalk.EnvironmentSettingArgs(
        #             namespace="aws:autoscaling:launchconfiguration",
        #             name="RootVolumeSize",
        #             value="16",  # default is 8GB, but we're making space for pytorch
        #         ),
        #     ],
        # )

        # pulumi.export("backend_eb_env", backend_eb_env.endpoint_url)
        # pulumi.export("backend_eb_env_cname", backend_eb_env.cname)

        # DEBUG
        # pulumi.export("backend_eb_env_settings", backend_eb_env.all_settings)
