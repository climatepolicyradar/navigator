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

DOCKER_COMPOSE_TEMPLATE = """version: '3.7'

services:

  nginx:
    image: {nginx_image}
    mem_limit: 128m
    ports:
      - 80:80
    volumes:
      - "${{EB_LOG_BASE_DIR}}/nginx:/var/log/nginx"
    depends_on:
      - backend
      - frontend

  backend:
    image: {backend_image}
    mem_limit: 4096m
    command: python app/main.py
    ports:
      - 8888:8888
    environment:
      PYTHONPATH: .
      PORT: 8888
      OPENSEARCH_INDEX: navigator
      DATABASE_URL: {database_url}
      SECRET_KEY: {secret_key}
      OPENSEARCH_USER: {opensearch_user}
      OPENSEARCH_PASSWORD: {opensearch_password}
      OPENSEARCH_URL: {opensearch_url}
      PUBLIC_APP_URL: {public_app_url}
      SENDGRID_API_KEY: {sendgrid_api_token}
      SENDGRID_FROM_EMAIL: {sendgrid_from_email}
      SENDGRID_ENABLED: "{sendgrid_enabled}"
      ENABLE_SELF_REGISTRATION: "{self_registration_enabled}"
      PIPELINE_BUCKET: "{pipeline_s3_bucket}"

  frontend:
    image: {frontend_image}
    mem_limit: 256m
    command: npm run start
    environment:
      PORT: 3000
      # not sure if these 3 need to be here, as it's already baked into the image.
      NEXT_PUBLIC_API_URL: {frontend_api_url}
      NEXT_PUBLIC_LOGIN_API_URL: {frontend_api_url_login}
      NEXT_PUBLIC_ADOBE_API_KEY: {frontend_pdf_embed_key}
    ports:
      - 3000:3000
    volumes:
      - "${{EB_LOG_BASE_DIR}}/frontend:/root/.npm/_logs"
"""


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
        frontend_pdf_embed_key = config.require_secret("pdf_embed_key")
        pipeline_s3_bucket = config.require_secret("pipeline_s3_bucket")

        app_domain = config.require("domain")
        frontend_api_url = f"https://{app_domain}/api/v1"
        frontend_api_url_login = f"https://{app_domain}/api/tokens"
        public_app_url = f"https://{app_domain}"
        self_registration_enabled = config.require("self_registration_enabled")

        # pulumi.export("opensearch_url", opensearch_url)
        pulumi.export("app_domain", app_domain)
        pulumi.export("self_registration_enabled", self_registration_enabled)
        pulumi.export("frontend_api_url", frontend_api_url)
        pulumi.export("frontend_api_url_login", frontend_api_url_login)
        pulumi.export("public_app_url", public_app_url)

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

        # frontend
        def build_frontend_image(args):
            pdf_embed_key = args[0]
            frontend_docker_context = (
                (Path(os.getcwd()) / ".." / "frontend").resolve().as_posix()
            )
            frontend_dockerfile = (
                (Path(os.getcwd()) / ".." / "frontend" / "Dockerfile")
                .resolve()
                .as_posix()
            )
            return docker.Image(
                f"{target_environment}-frontend-docker-image",
                build=docker.DockerBuild(
                    context=frontend_docker_context,
                    dockerfile=frontend_dockerfile,
                    args={
                        "NEXT_PUBLIC_API_URL": frontend_api_url,
                        "NEXT_PUBLIC_LOGIN_API_URL": frontend_api_url_login,
                        "NEXT_PUBLIC_ADOBE_API_KEY": pdf_embed_key,
                    },
                ),
                image_name=deployment_resources.navigator_frontend_repo.repository_url,
                skip_push=False,
                registry=deployment_resources.docker_registry,
            )

        frontend_image = pulumi.Output.all(frontend_pdf_embed_key).apply(
            build_frontend_image
        )

        # nginx
        nginx_docker_context = (Path(os.getcwd()) / ".." / "nginx").resolve().as_posix()
        nginx_dockerfile = (
            (Path(os.getcwd()) / ".." / "nginx" / "Dockerfile").resolve().as_posix()
        )
        nginx_image = docker.Image(
            f"{target_environment}-nginx-docker-image",
            build=docker.DockerBuild(
                context=nginx_docker_context,
                dockerfile=nginx_dockerfile,
            ),
            image_name=deployment_resources.navigator_nginx_repo.repository_url,
            skip_push=False,
            registry=deployment_resources.docker_registry,
        )

        def fill_template(arg_list):
            template_args = dict(
                zip(
                    [
                        "nginx_image",
                        "backend_image",
                        "frontend_image",
                        "database_url",
                        "secret_key",
                        "opensearch_user",
                        "opensearch_password",
                        "opensearch_url",
                        "sendgrid_api_token",
                        "sendgrid_from_email",
                        "sendgrid_enabled",
                        "public_app_url",
                        "frontend_api_url",
                        "frontend_api_url_login",
                        "frontend_pdf_embed_key",
                        "self_registration_enabled",
                        "pipeline_s3_bucket",
                    ],
                    arg_list,
                )
            )
            return DOCKER_COMPOSE_TEMPLATE.format(**template_args)

        docker_compose_file = pulumi.Output.all(
            nginx_image.image_name,
            backend_image.image_name,
            frontend_image.image_name,
            storage.backend_database_connection_url,
            backend_secret_key,
            opensearch_user,
            opensearch_password,
            opensearch_url,
            sendgrid_api_token,
            sendgrid_from_email,
            sendgrid_enabled,
            public_app_url,
            frontend_api_url,
            frontend_api_url_login,
            frontend_pdf_embed_key,
            self_registration_enabled,
            pipeline_s3_bucket,
        ).apply(fill_template)

        def create_deploy_resource(manifest):
            # TODO delete this file if it exists
            with open("docker-compose.yml", "w") as json_file:
                json_file.write(manifest)

            # DEBUG: set file as read-only
            # compose_path = Path("docker-compose.yml")
            # compose_path.chmod(0o444)

            deploy_resource = aws.s3.BucketObject(
                f"{target_environment}-backend-beanstalk-docker-manifest",
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
            f"{target_environment}-backend-beanstalk-application"
        )
        backend_app_version = aws.elasticbeanstalk.ApplicationVersion(
            f"{target_environment}-app-api-version",
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
        pulumi.export("solution_stack", solution_stack)

        backend_eb_env = aws.elasticbeanstalk.Environment(
            f"{target_environment}-app-api-environ",
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
                    value="t3.large",  # https://aws.amazon.com/ec2/instance-types/
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
            ],
        )

        pulumi.export("backend_eb_env", backend_eb_env.endpoint_url)
        pulumi.export("backend_eb_env_cname", backend_eb_env.cname)

        # DEBUG
        # pulumi.export("backend_eb_env_settings", backend_eb_env.all_settings)
