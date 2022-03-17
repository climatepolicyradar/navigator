from pulumi.dynamic import ResourceProvider, CreateResult, DiffResult

from cpr.tasks.util.run_task import run_task


class FargateRunTaskResourceProvider(ResourceProvider):
    def create(self, inputs):
        exit_code, task_arn = run_task(inputs)

        if exit_code != 0:
            raise Exception(f"Task run failed: {task_arn}")

        # The task is ephemeral, we don't need an ID because it will be
        # gone by the time this resource runs
        return CreateResult(id_="not-needed", outs={"task_arn": task_arn})

    def diff(self):
        # Always report changes so Pulumi will run this task's lifecycle functions
        return DiffResult(changes=True)

    # TODO update, delete ?
    # https://github.com/sevenwestmedia-labs/pulumi/blob/master/packages/run-fargate-task/src/fargate-run-task-resource-provider.ts#L25
