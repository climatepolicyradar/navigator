"""Infra-as-code for CPR stack."""

import pulumi
import pulumi_aws as aws

from cpr.deployment_resources.main import default_tag
from cpr.plumbing.main import Plumbing


class Storage:
    """Sets up all storage for the rest of the stack."""

    backend_database_connection_url: pulumi.Output

    def __init__(self, plumbing: Plumbing):
        config = pulumi.Config()
        db_username = config.require("db_username")
        db_password = config.require_secret("db_password")
        db_name = "navigator"

        # app_database_subnetgroup = aws.rds.SubnetGroup(
        #     "cpr-rds-instance-subnetgroup",
        #     subnet_ids=[net.id for net in plumbing.subnets],
        # )

        rds = aws.rds.Instance(
            "rds-instance",
            storage_type="gp2",
            allocated_storage=20,
            max_allocated_storage=0,  # disable autoscaling
            engine="postgres",
            engine_version="12.11",
            instance_class="db.t3.xlarge",
            name=db_name,
            password=db_password,
            skip_final_snapshot=True,
            username=db_username,
            # db_subnet_group_name=app_database_subnetgroup.id,  # TODO not sure if this is necessary
            vpc_security_group_ids=[plumbing.vpc_to_rds.id],
            multi_az=False,
            tags=default_tag,
        )

        self.backend_database_connection_url = pulumi.Output.all(
            rds.address, db_password
        ).apply(
            lambda args: f"postgresql://{db_username}:{args[1]}@{args[0]}/{db_name}"
        )

        pulumi.export("rds.address", rds.address)
