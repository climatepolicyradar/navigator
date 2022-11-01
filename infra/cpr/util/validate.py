import pulumi
import pulumi_aws as aws


def validate_aws_account() -> None:
    config = pulumi.Config()

    expected_account_id = config.require("validation_account_id")
    deploy_identity = aws.get_caller_identity()

    if expected_account_id != deploy_identity.account_id:
        raise RuntimeError(
            "The AWS credentials in use do not match the expected account ID."
        )
