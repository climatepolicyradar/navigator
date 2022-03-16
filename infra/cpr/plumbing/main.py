"""Infra-as-code for CPR stack."""
import json

import pulumi
import pulumi_aws as aws

from cpr.common import default_tag


class Plumbing:
    """
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
        self.security_group = aws.ec2.SecurityGroup(
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

        self.default_vpc = aws.ec2.DefaultVpc(
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

        self.subnet_ids = pulumi.Output.all(default_az1.id, default_az2.id, default_az3.id).apply(
            lambda az: f"{az[0]},{az[1]},{az[2]}"
        )

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
                )
            ],
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

        self.instance_profile = aws.iam.InstanceProfile(
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
        aws.iam.RolePolicyAttachment(
            "service-role-policy-attach-AWSElasticBeanstalkService",
            role=self.service_role.name,
            policy_arn="arn:aws:iam::aws:policy/service-role/AWSElasticBeanstalkService",
        )
