from dataclasses import dataclass
from typing import List, Optional

import pulumi
import pulumi_aws as aws
from pulumi.dynamic import ResourceProvider

from cpr.tasks.util.resource_provider import FargateRunTaskResourceProvider


@dataclass
class FargateRunTaskResourceInputs:
    aws_region: pulumi.Input[str]
    cluster_arn: pulumi.Input[str]
    task_definition_arn: pulumi.Input[str]
    delete_task_definition_arn: Optional[pulumi.Input[str]]
    subnet_ids: List[pulumi.Input[str]]
    security_group_ids: List[pulumi.Input[str]]


class FargateRunTask(pulumi.dynamic.Resource):
    """A Fargate task."""

    def __init__(
        self,
        name,
        # A Cluster represents a group of tasks and services that work together for a certain purpose
        cluster: aws.ecs.Cluster,
        task_definition: aws.ecs.TaskDefinition,
        subnet_ids: List[pulumi.Input],
        security_group_ids: List[pulumi.Input],
        delete_task_definition: Optional[aws.ecs.TaskDefinition],
        opts: Optional[pulumi.ResourceOptions] = None,
    ):
        config = pulumi.Config()
        aws_region = config.get("aws:region")

        # security_group_ids = None  # TODO securityGroupIds = args.cluster.securityGroups.map(g => g.id)
        # _subnet_ids = subnet_ids or cluster.vpc.getSubnetIds('public')

        resource_args = FargateRunTaskResourceInputs(
            aws_region=aws_region,
            cluster_arn=cluster.arn,
            task_definition_arn=task_definition.arn,
            delete_task_definition_arn=delete_task_definition.arn
            if delete_task_definition
            else None,
            subnet_ids=subnet_ids,
            security_group_ids=security_group_ids,
        )

        super.__init__(FargateRunTaskResourceProvider(), name, resource_args, opts)
