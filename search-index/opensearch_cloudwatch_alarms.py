"""Script to create recommended CloudWatch alarms for Opensearch instances in AWS. Run with the instance ID as the first CLI argument.

Documentation for recommended alarms: https://docs.aws.amazon.com/opensearch-service/latest/developerguide/cloudwatch-alarms.html

Note, as we're not using dedicated Master nodes the alarms from the documentation for master nodes aren't included here.
"""

import sys
import boto3

# Create CloudWatch client
cloudwatch = boto3.client("cloudwatch")


def create_cloudwatch_alarms(INSTANCE_ID):
    # CLUSTER STATUS
    cloudwatch.put_metric_alarm(
        AlarmName="ClusterStatus-Red",
        AlarmDescription="At least one primary shard and its replicas are not allocated to a node.",
        ComparisonOperator="GreaterThanThreshold",
        Threshold=0,
        EvaluationPeriods=1,
        MetricName="ClusterStatus.red",
        Namespace="AWS/ES",
        Period=60,
        Statistic="Maximum",
        ActionsEnabled=False,
        Dimensions=[
            {
                "Name": "InstanceId",
                "Value": INSTANCE_ID,
            },
        ],
        Unit="Seconds",
    )

    cloudwatch.put_metric_alarm(
        AlarmName="ClusterStatus-Yellow",
        AlarmDescription="At least one replica shard is not allocated to a node.",
        ComparisonOperator="GreaterThanThreshold",
        Threshold=0,
        EvaluationPeriods=1,
        MetricName="ClusterStatus.yellow",
        Namespace="AWS/ES",
        Period=60,
        Statistic="Maximum",
        ActionsEnabled=False,
        Dimensions=[
            {
                "Name": "InstanceId",
                "Value": INSTANCE_ID,
            },
        ],
        Unit="Seconds",
    )

    # STORAGE SPACE
    # Based on needing 25% free.
    cloudwatch.put_metric_alarm(
        AlarmName="FreeStorageSpace",
        AlarmDescription="Alarm for lack of available storage space.",
        ComparisonOperator="LessThanThreshold",
        # TODO: get the disk size here and set to 25% of that.
        Threshold=20 * 1e9,
        EvaluationPeriods=1,
        MetricName="FreeStorageSpace",
        Namespace="AWS/ES",
        Period=60,
        Statistic="Average",
        ActionsEnabled=False,
        Dimensions=[
            {
                "Name": "InstanceId",
                "Value": INSTANCE_ID,
            },
        ],
        Unit="Seconds",
    )

    # WRITES
    cloudwatch.put_metric_alarm(
        AlarmName="ClusterIndexWritesBlocked",
        AlarmDescription="Alarm for cluster blocking write requests.",
        ComparisonOperator="GreaterThanThreshold",
        Threshold=0,
        EvaluationPeriods=1,
        MetricName="ClusterIndexWritesBlocked",
        Namespace="AWS/ES",
        Period=300,
        ActionsEnabled=False,
        Statistic="SampleCount",
        Dimensions=[
            {
                "Name": "InstanceId",
                "Value": INSTANCE_ID,
            },
        ],
        Unit="Seconds",
    )

    # NODES AND SHARDS
    # All nodes are reachable.
    cloudwatch.put_metric_alarm(
        AlarmName="NodesNotReachable",
        AlarmDescription="Alarm for at least one node unavailable.",
        ComparisonOperator="LessThanThreshold",
        # TODO: get number of nodes for instance and add alarm based on that.
        Threshold=3,
        Statistic="Minimum",
        EvaluationPeriods=1,
        MetricName="Nodes",
        Namespace="AWS/ES",
        Period=86400,
        ActionsEnabled=False,
        Dimensions=[
            {
                "Name": "InstanceId",
                "Value": INSTANCE_ID,
            },
        ],
        Unit="Seconds",
    )

    cloudwatch.put_metric_alarm(
        AlarmName="AutomatedSnapshotFailure",
        AlarmDescription="Alarm for at least one node unavailable.",
        ComparisonOperator="GreaterThanThreshold",
        Threshold=0,
        Statistic="Maximum",
        EvaluationPeriods=1,
        MetricName="AutomatedSnapshotFailure",
        Namespace="AWS/ES",
        Period=60,
        ActionsEnabled=False,
        Dimensions=[
            {
                "Name": "InstanceId",
                "Value": INSTANCE_ID,
            },
        ],
        Unit="Seconds",
    )

    cloudwatch.put_metric_alarm(
        AlarmName="Shards-Active",
        AlarmDescription="Alarm for too many active primary and replica shards.",
        ComparisonOperator="GreaterThanOrEqualToThreshold",
        Threshold=30000,
        Statistic="SampleCount",
        EvaluationPeriods=1,
        MetricName="shards.active",
        Namespace="AWS/ES",
        Period=60,
        ActionsEnabled=False,
        Dimensions=[
            {
                "Name": "InstanceId",
                "Value": INSTANCE_ID,
            },
        ],
        Unit="Seconds",
    )

    # CPU and RAM utilisation
    cloudwatch.put_metric_alarm(
        AlarmName="CPUUtilization",
        AlarmDescription="Alarm for sustained high CPU usage.",
        ComparisonOperator="GreaterThanThreshold",
        Threshold=80,
        Statistic="Maximum",
        EvaluationPeriods=3,
        MetricName="CPUUtilization",
        Namespace="AWS/ES",
        Period=900,
        ActionsEnabled=False,
        Dimensions=[
            {
                "Name": "InstanceId",
                "Value": INSTANCE_ID,
            },
        ],
        Unit="Seconds",
    )

    cloudwatch.put_metric_alarm(
        AlarmName="JVMMemoryPressure",
        AlarmDescription="Alarm for sustained high RAM usage.",
        ComparisonOperator="GreaterThanThreshold",
        Threshold=80,
        Statistic="Maximum",
        EvaluationPeriods=3,
        MetricName="JVMMemoryPressure",
        Namespace="AWS/ES",
        Period=300,
        ActionsEnabled=False,
        Dimensions=[
            {
                "Name": "InstanceId",
                "Value": INSTANCE_ID,
            },
        ],
        Unit="Seconds",
    )

    # Encryption keys
    cloudwatch.put_metric_alarm(
        AlarmName="KMSKeyError",
        AlarmDescription="Alarm for encryption key disabled.",
        ComparisonOperator="GreaterThanThreshold",
        Threshold=0,
        Statistic="SampleCount",
        EvaluationPeriods=1,
        MetricName="KMSKeyError",
        Namespace="AWS/ES",
        Period=60,
        ActionsEnabled=False,
        Dimensions=[
            {
                "Name": "InstanceId",
                "Value": INSTANCE_ID,
            },
        ],
        Unit="Seconds",
    )

    cloudwatch.put_metric_alarm(
        AlarmName="KMSKeyInaccessible",
        AlarmDescription="Alarm for encryption key deleted or grants revoked.",
        ComparisonOperator="GreaterThanThreshold",
        Threshold=0,
        Statistic="SampleCount",
        EvaluationPeriods=1,
        MetricName="KMSKeyInaccessible",
        Namespace="AWS/ES",
        Period=60,
        ActionsEnabled=False,
        Dimensions=[
            {
                "Name": "InstanceId",
                "Value": INSTANCE_ID,
            },
        ],
        Unit="Seconds",
    )

    # Search and Indexing concurrency
    cloudwatch.put_metric_alarm(
        AlarmName="ThreadpoolWriteQueue",
        AlarmDescription="Alarm for high average concurrency of indexing requests.",
        ComparisonOperator="GreaterThanOrEqualToThreshold",
        Threshold=100,
        Statistic="Average",
        EvaluationPeriods=1,
        MetricName="ThreadpoolWriteQueue",
        Namespace="AWS/ES",
        Period=60,
        ActionsEnabled=False,
        Dimensions=[
            {
                "Name": "InstanceId",
                "Value": INSTANCE_ID,
            },
        ],
        Unit="Seconds",
    )

    cloudwatch.put_metric_alarm(
        AlarmName="ThreadpoolSearchQueueAverage",
        AlarmDescription="Alarm for high average concurrency of search requests.",
        ComparisonOperator="GreaterThanOrEqualToThreshold",
        Threshold=500,
        Statistic="Average",
        EvaluationPeriods=1,
        MetricName="ThreadpoolSearchQueue",
        Namespace="AWS/ES",
        Period=60,
        ActionsEnabled=False,
        Dimensions=[
            {
                "Name": "InstanceId",
                "Value": INSTANCE_ID,
            },
        ],
        Unit="Seconds",
    )

    cloudwatch.put_metric_alarm(
        AlarmName="ThreadpoolSearchQueueMaximum",
        AlarmDescription="Alarm for high maximum concurrency of search requests.",
        ComparisonOperator="GreaterThanOrEqualToThreshold",
        Threshold=5000,
        Statistic="Maximum",
        EvaluationPeriods=1,
        MetricName="ThreadpoolSearchQueue",
        Namespace="AWS/ES",
        Period=60,
        ActionsEnabled=False,
        Dimensions=[
            {
                "Name": "InstanceId",
                "Value": INSTANCE_ID,
            },
        ],
        Unit="Seconds",
    )


if __name__ == "__main__":
    instance_id = sys.argv[1]
    create_cloudwatch_alarms(instance_id)
