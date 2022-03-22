import json
import pulumi
import pulumi_aws as aws

from cpr.backend.main import Backend
from cpr.plumbing.main import Plumbing
from cpr.storage.main import Storage
from cpr.tasks.util.run_task_resource import FargateRunTask


class Tasks:
    """Runs one-off tasks, e.g. database migrations.

    Inspired by https://github.com/sevenwestmedia-labs/pulumi/tree/master/packages/run-fargate-task
    """

    def __init__(
        self,
        backend: Backend,
        storage: Storage,
        plumbing: Plumbing,
    ):
        # Create an IAM role that can be used by our service's task.
        role = aws.iam.Role(
            "task-exec-role",
            assume_role_policy=json.dumps(
                {
                    "Version": "2008-10-17",
                    "Statement": [
                        {
                            "Sid": "",
                            "Effect": "Allow",
                            "Principal": {"Service": "ecs-tasks.amazonaws.com"},
                            "Action": "sts:AssumeRole",
                        }
                    ],
                }
            ),
        )
        aws.iam.RolePolicyAttachment(
            "task-exec-policy",
            role=role.name,
            policy_arn="arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy",
        )

        # see https://docs.aws.amazon.com/AmazonECS/latest/userguide/task_definitions.html
        update_db_taskdef = aws.ecs.TaskDefinition(
            "db-upgrade",
            family="cpr-tasks",
            execution_role_arn=role.arn,
            requires_compatibilities=["FARGATE"],
            cpu="256",  # smallest value
            memory="512",  # smallest value
            network_mode="awsvpc",
            runtime_platform=aws.ecs.TaskDefinitionRuntimePlatformArgs(
                cpu_architecture="X86_64",
                operating_system_family="LINUX",
            ),
            container_definitions=pulumi.Output.all(
                backend.backend_image, storage.backend_database_connection_url
            ).apply(
                lambda args: json.dumps(
                    [
                        {
                            "name": "database-migration-upgrade",
                            "image": args[0],
                            "command": "alembic upgrade head",
                            "essential": False,
                            "environment": [
                                {"name": "DATABASE_URL", "value": args[1]},
                            ],
                        }
                    ]
                )
            ),
        )

        # An Amazon ECS cluster is a logical grouping of tasks or services.
        # https://docs.aws.amazon.com/AmazonECS/latest/developerguide/clusters.html
        task_cluster = aws.ecs.Cluster(
            "cpr-tasks-cluster",
        )

        # migrate DB!
        FargateRunTask(
            name="cpr-tasks-migrations",
            cluster=task_cluster,
            task_definition=update_db_taskdef,
            subnet_ids=[net.id for net in plumbing.subnets],
            security_group_ids=[plumbing.security_group.id],
            delete_task_definition=None,  # TODO downgrade task?
        )
