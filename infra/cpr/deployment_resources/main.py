"""Infra-as-code for CPR stack."""
import base64

import pulumi
import pulumi_aws as aws
import pulumi_docker as docker

default_tag = {
    "CPR-Created-By": "pulumi",
    "CPR-Pulumi-Stack-Name": pulumi.get_stack(),
}


class DeploymentResources:
    """Shared resources that aren't used by the running stack.

    These resources are necessary for deployment, e.g. intermediary buckets and Docker image registries.
    """

    ecr_repo: aws.ecr.Repository
    docker_registry: docker.ImageRegistry
    deploy_bucket: aws.s3.Bucket

    def __init__(self):
        target_environment = pulumi.get_stack()

        self.navigator_frontend_repo = aws.ecr.Repository(
            f"navigator-frontend-{target_environment}",
            # image_scanning_configuration=aws.ecr.RepositoryImageScanningConfigurationArgs(
            #     scan_on_push=True,
            # ),
            image_tag_mutability="MUTABLE",
            tags=({"key": "created-by", "value": "pulumi"}),
        )
        self.navigator_backend_repo = aws.ecr.Repository(
            f"navigator-backend-{target_environment}",
            # image_scanning_configuration=aws.ecr.RepositoryImageScanningConfigurationArgs(
            #     scan_on_push=True,
            # ),
            image_tag_mutability="MUTABLE",
            tags=({"key": "created-by", "value": "pulumi"}),
        )
        self.navigator_nginx_repo = aws.ecr.Repository(
            f"navigator-nginx-{target_environment}",
            # image_scanning_configuration=aws.ecr.RepositoryImageScanningConfigurationArgs(
            #     scan_on_push=True,
            # ),
            image_tag_mutability="MUTABLE",
            tags=({"key": "created-by", "value": "pulumi"}),
        )

        # keep the last 5 images
        frontend_lifecycle_policy = aws.ecr.LifecyclePolicy(  # noqa:F841
            f"navigator-frontend-{target_environment}-repository-lifecycle-policy",
            repository=self.navigator_frontend_repo.name,
            policy="""{
                "rules": [
                    {
                        "rulePriority": 10,
                        "description": "Remove untagged images",
                        "selection": {
                            "tagStatus": "untagged",
                            "countType": "imageCountMoreThan",
                            "countNumber": 5
                        },
                        "action": {
                            "type": "expire"
                        }
                    }
                ]
            }""",
        )
        backend_lifecycle_policy = aws.ecr.LifecyclePolicy(  # noqa:F841
            f"navigator-backend-{target_environment}-repository-lifecycle-policy",
            repository=self.navigator_backend_repo.name,
            policy="""{
                "rules": [
                    {
                        "rulePriority": 10,
                        "description": "Remove untagged images",
                        "selection": {
                            "tagStatus": "untagged",
                            "countType": "imageCountMoreThan",
                            "countNumber": 5
                        },
                        "action": {
                            "type": "expire"
                        }
                    }
                ]
            }""",
        )
        nginx_lifecycle_policy = aws.ecr.LifecyclePolicy(  # noqa:F841
            f"navigator-nginx-{target_environment}-repository-lifecycle-policy",
            repository=self.navigator_nginx_repo.name,
            policy="""{
                "rules": [
                    {
                        "rulePriority": 10,
                        "description": "Remove untagged images",
                        "selection": {
                            "tagStatus": "untagged",
                            "countType": "imageCountMoreThan",
                            "countNumber": 5
                        },
                        "action": {
                            "type": "expire"
                        }
                    }
                ]
            }""",
        )

        def get_registry_info(rid):
            creds = aws.ecr.get_credentials(registry_id=rid)
            decoded = base64.b64decode(creds.authorization_token).decode()
            parts = decoded.split(":")
            if len(parts) != 2:
                raise Exception("Invalid credentials")
            return docker.ImageRegistry(creds.proxy_endpoint, parts[0], parts[1])

        self.docker_registry = self.navigator_frontend_repo.registry_id.apply(
            get_registry_info
        )

        pulumi.export(
            "navigator_frontend.repository_url",
            self.navigator_frontend_repo.repository_url,
        )
        pulumi.export(
            "navigator_backend.repository_url",
            self.navigator_backend_repo.repository_url,
        )
        pulumi.export(
            "navigator_nginx.repository_url",
            self.navigator_nginx_repo.repository_url,
        )

        # a bucket which stores deployment resources, like Dockerrun.aws.json (for Elastic Beanstalk)
        self.deploy_bucket = aws.s3.Bucket(
            "backend-beanstalk-deployment-resources",
            acl=aws.s3.CannedAcl.PRIVATE,
            tags=default_tag,
        )
