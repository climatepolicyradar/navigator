"""Infra-as-code for CPR stack."""
import json
import pathlib
import pulumi
import pulumi_aws as aws

from cpr.deployment_resources.main import default_tag


def get_instance_profile() -> aws.iam.InstanceProfile:
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

    aws.iam.RolePolicy(
        "profile-role-policy-attach-S3PutObject",
        role=instance_profile_role.name,
        policy=json.dumps(
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Action": [
                            "s3:putObject",
                        ],
                        "Resource": "*",
                    }
                ],
            }
        ),
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

    return aws.iam.InstanceProfile(
        "eb-ec2-instance-profile",
        role=instance_profile_role.name,
        tags=default_tag,
    )


def get_instance_profile_for_bastion() -> aws.iam.InstanceProfile:
    instance_profile_role = aws.iam.Role(
        "bastion-role",
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
                    },
                ],
            }
        ),
        tags=default_tag,
    )

    policy = aws.iam.Policy(
        "allow-ssh-over-ssm",
        policy=json.dumps(
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Action": [
                            "ssm:StartSession",
                        ],
                        "Resource": "arn:aws:ssm:*:*:document/AWS-StartSSHSession",
                    },
                ],
            }
        ),
    )

    # policy attachments for bastion role
    aws.iam.RolePolicyAttachment(
        "bastion-role-policy-attach-AmazonSSMManagedInstanceCore",
        role=instance_profile_role.name,
        policy_arn="arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore",
    )
    aws.iam.RolePolicyAttachment(
        "bastion-role-policy-attach-allow-ssh-over-ssm",
        role=instance_profile_role.name,
        policy_arn=policy.arn,
    )

    return aws.iam.InstanceProfile(
        "bastion-instance-profile",
        role=instance_profile_role.name,
        tags=default_tag,
    )


class Plumbing:
    """Deploys necessary "glue" components for the stack.

    Plumbing is a blanket term for all the "invisible" things we need in the infrastructure:
    - security groups
    - availability zones
    - virtual private clouds (VPCs)
    - IAM roles
    """

    security_group: aws.ec2.SecurityGroup
    default_vpc: aws.ec2.DefaultVpc
    subnet_ids: pulumi.Output
    vpc_to_rds: aws.ec2.SecurityGroup
    instance_profile: aws.iam.InstanceProfile
    service_role: aws.iam.Role

    def __init__(self):
        self.default_vpc = aws.ec2.DefaultVpc(
            "default-vpc",
            tags={
                "Name": "Default VPC",
            },
        )

        # Security groups control traffic flow between applications running inside our VPC
        security_group_bastion = aws.ec2.SecurityGroup(
            "bastion-security-group",
            description="Enable SSH access",
            vpc_id=self.default_vpc.id,
            ingress=[
                aws.ec2.SecurityGroupIngressArgs(
                    protocol="tcp",
                    from_port=22,
                    to_port=22,
                    cidr_blocks=["0.0.0.0/0"],
                )
            ],
            egress=[
                aws.ec2.SecurityGroupEgressArgs(
                    protocol="-1",  # -1 means ALL protocols
                    from_port=0,
                    to_port=0,
                    cidr_blocks=["0.0.0.0/0"],
                )
            ],
            tags=default_tag,
        )

        bastion_ami = aws.ec2.get_ami(
            filters=[
                aws.ec2.GetAmiFilterArgs(
                    name="name",
                    values=["amzn2-ami-hvm-*"],
                ),
            ],
            owners=["137112412989"],  # This owner ID is Amazon
            most_recent=True,
        )

        stack_name = pulumi.get_stack()

        keypair = aws.ec2.KeyPair(
            "bastion-ssh-key",
            key_name=f"bastion-{stack_name}-ssh-key",
            public_key="ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA14swrmHESs/dE8+nhj8twLPpbq//FHAVw7fXEQIvflJ+03yb6ostNLcXNroenoKzfRAwqVx0BRgYB0RKoBP5yIL7K5UkzxnWHEpIj3oC+kIrR1kn8LlsGa1aP05BYmZvsBXFzBjiBie3vhOTGOiEVEzqxdJLZExa6HIeoarKukAi94uQNDFZbnBNqdjRdgIPUdDHYlL5abSKC+yTS2+L96y6Dzt47i+rkn2rZzld1nYgRNLfAtvooIPZ60IfCnhRGPGuPA+nyYLtgRYVKCfC5yZ6QFUp0WH9NjE7PJMY2UX6w465bgbWlVtu8Ue687oWNyJf3r39S73gmpHOUHMkuw== opyate@gmail.com",
            tags=default_tag,
        )

        # Security groups control traffic flow between applications running inside our VPC
        self.security_group = aws.ec2.SecurityGroup(
            "navigator-security-group",
            description="Enable HTTP access",
            vpc_id=self.default_vpc.id,
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

        default_az1 = aws.ec2.DefaultSubnet(
            "default-az-1",
            availability_zone="eu-west-2a",  # TODO make this dynamic
            tags={
                "Name": "Default subnet for eu-west-2a",
            },
        )

        default_az2 = aws.ec2.DefaultSubnet(
            "default-az-2",
            availability_zone="eu-west-2b",  # TODO make this dynamic
            tags={
                "Name": "Default subnet for eu-west-2b",
            },
        )

        default_az3 = aws.ec2.DefaultSubnet(
            "default-az-3",
            availability_zone="eu-west-2c",  # TODO make this dynamic
            tags={
                "Name": "Default subnet for eu-west-2c",
            },
        )
        self.subnets = [default_az1, default_az2, default_az3]

        self.subnet_ids = pulumi.Output.all(
            default_az1.id, default_az2.id, default_az3.id
        ).apply(lambda az: f"{az[0]},{az[1]},{az[2]}")

        self.vpc_to_rds = aws.ec2.SecurityGroup(
            "vpc-to-rds",
            description="Allow the resources inside the VPC to communicate with postgres RDS instance",
            vpc_id=self.default_vpc.id,
            ingress=[
                aws.ec2.SecurityGroupIngressArgs(
                    from_port=5432,
                    to_port=5432,
                    protocol="tcp",
                    cidr_blocks=[self.default_vpc.cidr_block],
                    security_groups=[security_group_bastion.id],
                )
            ],
            tags=default_tag,
        )

        # api
        self.instance_profile = get_instance_profile()

        # service role
        service_role_txt = json.dumps(
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": "sts:AssumeRole",
                        "Condition": {
                            "StringEquals": {"sts:ExternalId": "elasticbeanstalk"}
                        },
                        "Principal": {"Service": "elasticbeanstalk.amazonaws.com"},
                        "Effect": "Allow",
                    }
                ],
            }
        )

        self.service_role = aws.iam.Role(
            "backend-service-role",
            assume_role_policy=service_role_txt,
            tags=default_tag,
        )
        # policy attachments for service role
        aws.iam.RolePolicyAttachment(
            "service-role-policy-attach-AWSElasticBeanstalkEnhancedHealth",
            role=self.service_role.name,
            policy_arn="arn:aws:iam::aws:policy/service-role/AWSElasticBeanstalkEnhancedHealth",
        )
        # TODO This policy is on a deprecation path.
        #  See documentation for guidance: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/iam-servicerole.html.
        #  AWS Elastic Beanstalk Service role policy which grants permissions to create & manage resources
        #  (i.e.: AutoScaling, EC2, S3, CloudFormation, ELB, etc.) on your behalf.
        aws.iam.RolePolicyAttachment(
            "service-role-policy-attach-AWSElasticBeanstalkService",
            role=self.service_role.name,
            policy_arn="arn:aws:iam::aws:policy/service-role/AWSElasticBeanstalkService",
        )

        # TODO A gateway and routing table are needed to allow the VPC to communicate with the Internet.
        # Once created, we associate the routing table with our VPC.
        _comment = """
        app_gateway = aws.ec2.InternetGateway("navigator-gateway",
            vpc_id=app_vpc.id)

        app_routetable = aws.ec2.RouteTable("navigator-routetable",
            routes=[
                {
                    "cidr_block": "0.0.0.0/0",
                    "gateway_id": app_gateway.id,
                }
            ],
            vpc_id=app_vpc.id)

        app_routetable_association = aws.ec2.MainRouteTableAssociation("navigator_routetable_association",
            route_table_id=app_routetable.id,
            vpc_id=app_vpc)
        """  # noqa: F841

        bastion_extra = pathlib.Path(__file__) / ".." / "bastion_extra.sh"
        with open(bastion_extra.resolve()) as f:
            user_data = f.read()

        instance = aws.ec2.Instance(
            "bastion-server",
            ami=bastion_ami.id,
            associate_public_ip_address=True,
            instance_type=aws.ec2.InstanceType.T2_NANO,
            key_name=keypair.key_name,
            vpc_security_group_ids=[security_group_bastion.id],
            subnet_id=default_az1.id,
            user_data=user_data,
            tags=default_tag,
            iam_instance_profile=get_instance_profile_for_bastion().name,
        )

        pulumi.export("bastion.public_dns", instance.public_dns)
        pulumi.export("bastion.public_ip", instance.public_ip)
        pulumi.export("bastion.id", instance.id)
