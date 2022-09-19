import pulumi_aws as aws
import mimetypes
import os
from pathlib import Path

import pulumi
import pulumi_docker as docker
from pulumi import export, FileAsset, ResourceOptions, Output

from cpr.deployment_resources.main import DeploymentResources, default_tag
from cpr.plumbing.main import Plumbing
from cpr.storage.main import Storage


class Frontend:
    def __init__(
        self,
        deployment_resources: DeploymentResources,
        plumbing: Plumbing,
        storage: Storage,
    ):

        # frontend
        target_environment = pulumi.get_stack()
        # get all config
        config = pulumi.Config()
        app_domain = config.require("domain")
        frontend_api_url = f"https://{app_domain}/api/v1"
        frontend_pdf_embed_key = config.require_secret("pdf_embed_key")
        frontend_api_url_login = f"https://{app_domain}/api/tokens"
        public_app_url = f"https://{app_domain}"
        self_registration_enabled = config.require("self_registration_enabled")

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
