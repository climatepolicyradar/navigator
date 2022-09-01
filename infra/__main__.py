"""Infra-as-code for CPR stack."""
from cpr.backend.main_with_frontend import Backend
from cpr.deployment_resources.main import DeploymentResources

from cpr.plumbing.main import Plumbing
from cpr.util.slackalert import alert_slack
from cpr.util.validate import validate_aws_account
from cpr.storage.main import Storage

validate_aws_account()
alert_slack()

deployment_resources = DeploymentResources()
plumbing = Plumbing()
storage = Storage(plumbing=plumbing)
backend = Backend(
    deployment_resources=deployment_resources, plumbing=plumbing, storage=storage
)
