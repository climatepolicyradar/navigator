"""Infra-as-code for CPR stack."""
import base64

import pulumi
import pulumi_aws as aws
import pulumi_docker as docker

default_tag = {"Created-By": "pulumi"}


class SharedResources:
    """Shared resources that aren't used by the running stack.

    These resources are necessary for deployment, e.g. intermediary buckets and Docker image registries.
    """

    ecr_repo: aws.ecr.Repository
    docker_registry: docker.ImageRegistry
    deploy_bucket: aws.s3.Bucket

    def __init__(self):
        self.ecr_repo = aws.ecr.Repository(
            "cpr-container-registry",
            # image_scanning_configuration=aws.ecr.RepositoryImageScanningConfigurationArgs(
            #     scan_on_push=True,
            # ),
            image_tag_mutability="MUTABLE",
            tags=({"key": "created-by", "value": "pulumi"}),
        )

        # TODO aws.ecr.LifecyclePolicy to expire old images

        docker_registry_credentials = aws.ecr.get_authorization_token()

        def get_registry_info(rid):
            creds = aws.ecr.get_credentials(registry_id=rid)
            decoded = base64.b64decode(creds.authorization_token).decode()
            parts = decoded.split(":")
            if len(parts) != 2:
                raise Exception("Invalid credentials")
            return docker.ImageRegistry(creds.proxy_endpoint, parts[0], parts[1])

        self.docker_registry = self.ecr_repo.registry_id.apply(get_registry_info)

        pulumi.export("ecr.repository_url", self.ecr_repo.repository_url)

        # a bucket which stores deployment resources, like Dockerrun.aws.json (for Elastic Beanstalk)
        self.deploy_bucket = aws.s3.Bucket(
            "backend-beanstalk-deployment-resources",
            acl=aws.s3.CannedAcl.PRIVATE,
            tags=default_tag,
        )
