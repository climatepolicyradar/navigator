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

        # frontend
        docker_context = Path(os.getcwd()) / ".." / "frontend"
        docker_context = docker_context.resolve().as_posix()
        frontend_dockerfile = Path(os.getcwd()) / ".." / "frontend" / "Dockerfile"
        frontend_dockerfile = frontend_dockerfile.resolve().as_posix()

        frontend_image = docker.Image(
            "frontend-docker-image",
            build=docker.DockerBuild(
                context=docker_context,
                dockerfile=frontend_dockerfile,
                args={"NEXT_PUBLIC_API_URL": "https://api.climatepolicyradar.org/"},
            ),
            image_name=deployment_resources.ecr_repo.repository_url,
            skip_push=False,
            registry=deployment_resources.docker_registry,
        )

        # nginx
        docker_context = Path(os.getcwd()) / ".." / "nginx"
        docker_context = docker_context.resolve().as_posix()
        nginx_dockerfile = Path(os.getcwd()) / ".." / "nginx" / "Dockerfile"
        nginx_dockerfile = nginx_dockerfile.resolve().as_posix()

        nginx_image = docker.Image(
            "nginx-docker-image",
            build=docker.DockerBuild(
                context=docker_context, dockerfile=nginx_dockerfile
            ),
            image_name=deployment_resources.ecr_repo.repository_url,
            skip_push=False,
            registry=deployment_resources.docker_registry,
        )

        config = pulumi.Config()
        backend_secret_key = config.require_secret("backend_secret_key")

        docker_compose_template = """version: '3.7'

services:

  nginx:
    image: %s
    mem_limit: 128m
    ports:
      - 80:80
    volumes:
      - "${EB_LOG_BASE_DIR}/nginx:/var/log/nginx"
    depends_on:
      - backend
      - frontend

  backend:
    image: %s
    mem_limit: 256m
    command: python app/main.py
    environment:
      PYTHONPATH: .
      DATABASE_URL: %s
      SECRET_KEY: %s

  frontend:
    image: %s
    mem_limit: 256m
    command: npm run prod
    volumes:
      - "${EB_LOG_BASE_DIR}/frontend:/root/.npm/_logs"
        """

        def fill_template(arg):
            return docker_compose_template % (arg[0], arg[1], arg[2], arg[3], arg[4])

        docker_compose_file = pulumi.Output.all(
            nginx_image.image_name,
            self.backend_image.image_name,
            storage.backend_database_connection_url,
            backend_secret_key,
            frontend_image.image_name,
        ).apply(fill_template)

        pulumi.export("docker_compose_file", docker_compose_file)

        def create_deploy_resource(manifest):
            # TODO delete this file if it exists
            with open("docker-compose.yml", "w") as json_file:
                json_file.write(manifest)

            deploy_resource = aws.s3.BucketObject(
                "backend-beanstalk-docker-manifest",
                bucket=deployment_resources.deploy_bucket,
                key=datetime.datetime.today().strftime(
                    "%Y/%m/%d/%H:%M:%S/docker-compose.yml"
                ),
                source=pulumi.asset.FileAsset("docker-compose.yml"),
                tags=default_tag,
            )
            return deploy_resource

        deploy_resource = docker_compose_file.apply(create_deploy_resource)

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
            # name_regex=r"^64bit Amazon Linux(.*)Multi-container Docker(.*)$",
        )
        pulumi.export("solution_stack", solution_stack)

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
                    value="t3.micro",  # https://aws.amazon.com/ec2/instance-types/
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
                    namespace="aws:elasticbeanstalk:application:environment",
                    name="SECRET_KEY",
                    value=backend_secret_key,
                ),
            ],
        )

        pulumi.export("backend_eb_env", backend_eb_env.endpoint_url)