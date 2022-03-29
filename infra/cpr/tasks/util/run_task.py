from cpr.tasks.util.run_task_resource import (
    FargateRunTask,
    FargateRunTaskResourceInputs,
)
import boto3
import pulumi
import time


def run_task(inputs: FargateRunTaskResourceInputs):
    config = pulumi.Config()
    aws_region = config.get("aws:region")

    ecs_client = boto3.resource("ecs", region_name=aws_region)

    result = ecs_client.run_task(
        cluster=inputs.cluster_arn,
        taskDefinition=inputs.task_definition_arn,
        launchType="FARGATE",
        networkConfiguration={
            "awsvpcConfiguration": {
                "subnets": inputs.subnet_ids,
                "securityGroups": inputs.security_group_ids,
            },
        },
    )

    if "tasks" not in result and not result["tasks"]:
        raise Exception("Missing tasks")

    tasklen = len(result["tasks"])
    if tasklen != 1:
        raise Exception(f"Unexpected number of tasks: {tasklen}")

    task = result["tasks"][0]

    if "taskArn" not in task and not task["taskArn"]:
        raise Exception("Task missing taskArn")

    task_arn = task["taskArn"]

    waiter = ecs_client.get_waiter("tasks_stopped")
    waiter.wait(
        cluster=inputs.cluster_arn,
        tasks=[
            task_arn,
        ],
        include=[
            "TAGS",
        ],
        WaiterConfig={"Delay": 6, "MaxAttempts": 50},
    )

    time.sleep(2)

    run_result = ecs_client.describe_tasks(
        cluster=inputs.cluster_arn,
        tasks=[
            task_arn,
        ],
    )

    if "tasks" not in run_result and not run_result["tasks"]:
        raise Exception("Missing tasks")

    tasklen = len(run_result["tasks"])
    if tasklen != 1:
        raise Exception(f"Unexpected number of tasks: {tasklen}")

    task = run_result["tasks"][0]
    if "containers" not in task and not task["containers"]:
        raise Exception("Task status is missing container")

    containerlen = len(task["containers"])
    if containerlen != 1:
        raise Exception(
            f"Unexpected number of containers: {containerlen}. Single container required."
        )

    # return {"taskArn": task_arn, "exitCode": task["containers"][0]["exitCode"]}
    return task["containers"][0]["exitCode"], task_arn
