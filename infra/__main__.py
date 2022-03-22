"""Infra-as-code for CPR stack."""
import base64
import datetime
import json
import os
from pathlib import Path

import pulumi
import pulumi_aws as aws
import pulumi_docker as docker

config = pulumi.Config()

db_username = config.require("db_username")
db_password = config.require_secret("db_password")
backend_secret_key = config.require_secret("backend_secret_key")
db_name = "navigator"

# ==============================================================================
# common
# ==============================================================================

default_tag = {"Created-By": "pulumi"}
# sudo apt install amazon-ecr-credential-helper
ecr_repo = aws.ecr.Repository(
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


# ==============================================================================
# backend
# ==============================================================================

stack = pulumi.get_stack()

# build our backend image!
backend_image_name = "backend"

docker_registry = ecr_repo.registry_id.apply(get_registry_info)

pulumi.export("ecr.repository_url", ecr_repo.repository_url)

# context has to be one level below 'backend' as backend Dockerfile references '../common'
docker_context = Path(os.getcwd()) / ".."
docker_context = docker_context.resolve().as_posix()
backend_dockerfile = Path(os.getcwd()) / ".." / "backend" / "Dockerfile"
backend_dockerfile = backend_dockerfile.resolve().as_posix()

backend_image = docker.Image(
    "backend-docker-image",
    build=docker.DockerBuild(context=docker_context, dockerfile=backend_dockerfile),
    # image_name=f"{backend_image_name}:{stack}",
    image_name=ecr_repo.repository_url,
    skip_push=False,
    registry=docker_registry,
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


dockerrun_file = backend_image.image_name.apply(fill_template)

pulumi.export("dockerrun_file", dockerrun_file)

security_group = aws.ec2.SecurityGroup(
    "navigator-security-group",
    description="Enable HTTP access",
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=80,
            to_port=8888,
            cidr_blocks=["0.0.0.0/0"],
        )
    ],
    tags=default_tag,
)

default_vpc = aws.ec2.DefaultVpc(
    "default-vpc",
    tags={
        "Name": "Default VPC",
    },
)

default_az1 = aws.ec2.DefaultSubnet(
    "default-az-1",
    availability_zone="eu-west-2a",
    tags={
        "Name": "Default subnet for eu-west-2a",
    },
)

default_az2 = aws.ec2.DefaultSubnet(
    "default-az-2",
    availability_zone="eu-west-2b",
    tags={
        "Name": "Default subnet for eu-west-2b",
    },
)

default_az3 = aws.ec2.DefaultSubnet(
    "default-az-3",
    availability_zone="eu-west-2c",
    tags={
        "Name": "Default subnet for eu-west-2c",
    },
)

subnet_ids = pulumi.Output.all(default_az1.id, default_az2.id, default_az3.id).apply(
    lambda az: f"{az[0]},{az[1]},{az[2]}"
)

vpc_to_rds = aws.ec2.SecurityGroup(
    "vpc-to-rds",
    description="Allow the resources inside the VPC to communicate with postgres RDS instance",
    vpc_id=default_vpc.id,
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            from_port=5432,
            to_port=5432,
            protocol="tcp",
            cidr_blocks=[default_vpc.cidr_block],
        )
    ],
    tags=default_tag,
)

rds = aws.rds.Instance(
    "rds-instance",
    storage_type="gp2",
    allocated_storage=20,
    max_allocated_storage=0,  # disable autoscaling
    engine="postgres",
    engine_version="12.10",
    instance_class="db.t3.micro",
    name=db_name,
    password=db_password,
    skip_final_snapshot=True,
    username=db_username,
    vpc_security_group_ids=[vpc_to_rds.id],
    multi_az=False,
    tags=default_tag,
)

# api
instance_profile_role = aws.iam.Role(
    "eb-ec2-role",
    assume_role_policy=json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "sts:AssumeRole",
                    "Effect": "Allow",
                    "Sid": "",
                    "Principal": {
                        "Service": "ec2.amazonaws.com",
                    },
                }
            ],
        }
    ),
    tags=default_tag,
)

# policy attachments for profile role
aws.iam.RolePolicyAttachment(
    "profile-role-policy-attach-AWSElasticBeanstalkWebTier",
    role=instance_profile_role.name,
    policy_arn="arn:aws:iam::aws:policy/AWSElasticBeanstalkWebTier",
)
aws.iam.RolePolicyAttachment(
    "profile-role-policy-attach-AWSElasticBeanstalkWorkerTier",
    role=instance_profile_role.name,
    policy_arn="arn:aws:iam::aws:policy/AWSElasticBeanstalkWorkerTier",
)
aws.iam.RolePolicyAttachment(
    "profile-role-policy-attach-AWSElasticBeanstalkMulticontainerDocker",
    role=instance_profile_role.name,
    policy_arn="arn:aws:iam::aws:policy/AWSElasticBeanstalkMulticontainerDocker",
)
aws.iam.RolePolicyAttachment(
    "profile-role-policy-attach-AmazonEC2ContainerRegistryReadOnly",
    role=instance_profile_role.name,
    policy_arn="arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly",
)

instance_profile = aws.iam.InstanceProfile(
    "eb-ec2-instance-profile",
    role=instance_profile_role.name,
    tags=default_tag,
)

# service role
service_role_txt = json.dumps(
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": "sts:AssumeRole",
                "Condition": {"StringEquals": {"sts:ExternalId": "elasticbeanstalk"}},
                "Principal": {"Service": "elasticbeanstalk.amazonaws.com"},
                "Effect": "Allow",
            }
        ],
    }
)

service_role = aws.iam.Role(
    "backend-service-role",
    assume_role_policy=service_role_txt,
    tags=default_tag,
)
# policy attachments for service role
aws.iam.RolePolicyAttachment(
    "service-role-policy-attach-AWSElasticBeanstalkEnhancedHealth",
    role=service_role.name,
    policy_arn="arn:aws:iam::aws:policy/service-role/AWSElasticBeanstalkEnhancedHealth",
)
aws.iam.RolePolicyAttachment(
    "service-role-policy-attach-AWSElasticBeanstalkService",
    role=service_role.name,
    policy_arn="arn:aws:iam::aws:policy/service-role/AWSElasticBeanstalkService",
)

backend_database_connection_url = pulumi.Output.all(rds.address, db_password).apply(
    lambda out: f"postgresql://{db_username}:{out[1]}@{out[0]}/{db_name}"
)

backend_eb_app = aws.elasticbeanstalk.Application("backend-beanstalk-application")

deploy_bucket = aws.s3.Bucket(
    "backend-beanstalk-deployment-resources",
    acl=aws.s3.CannedAcl.PRIVATE,
    tags=default_tag,
)


def create_deploy_resource(manifest):
    # TODO delete this file if it exists
    with open("Dockerrun.aws.json", "w") as json_file:
        json_file.write(manifest)

    deploy_resource = aws.s3.BucketObject(
        "backend-beanstalk-docker-manifest",
        bucket=deploy_bucket,
        key=datetime.datetime.today().strftime("%Y/%M/%d/%H:%M:%S/Dockerrun.aws.json"),
        source=pulumi.asset.FileAsset("Dockerrun.aws.json"),
        tags=default_tag,
    )
    return deploy_resource


deploy_resource = dockerrun_file.apply(create_deploy_resource)

backend_app_version = aws.elasticbeanstalk.ApplicationVersion(
    "navigator-api-version",
    application=backend_eb_app,
    bucket=deploy_bucket.id,
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
            value=instance_profile.name,
        ),
        aws.elasticbeanstalk.EnvironmentSettingArgs(
            namespace="aws:ec2:vpc",
            name="VPCId",
            value=default_vpc.id,
        ),
        aws.elasticbeanstalk.EnvironmentSettingArgs(
            namespace="aws:ec2:vpc",
            name="Subnets",
            value=subnet_ids,
        ),
        # aws.elasticbeanstalk.EnvironmentSettingArgs(
        #     namespace="aws:ec2:vpc",
        #     name="ELBSubnets",
        #     value=subnet_ids,
        # ),
        aws.elasticbeanstalk.EnvironmentSettingArgs(
            namespace="aws:elasticbeanstalk:environment",
            name="ServiceRole",
            value=service_role.name,
        ),
        aws.elasticbeanstalk.EnvironmentSettingArgs(
            namespace="aws:ec2:instances",
            name="InstanceTypes",
            value="t3.micro",  # https://aws.amazon.com/ec2/instance-types/
        ),
        aws.elasticbeanstalk.EnvironmentSettingArgs(
            namespace="aws:autoscaling:launchconfiguration",
            name="SecurityGroups",
            value=security_group.id,
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
        # app env vars
        aws.elasticbeanstalk.EnvironmentSettingArgs(
            namespace="aws:elasticbeanstalk:application:environment",
            name="DATABASE_URL",
            value=backend_database_connection_url,
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
    ],
)
