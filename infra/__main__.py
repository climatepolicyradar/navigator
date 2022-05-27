"""Infra-as-code for CPR stack."""
from cpr.backend.main_with_frontend import Backend
from cpr.deployment_resources.main import DeploymentResources

# from cpr.frontend.main import Frontend
from cpr.plumbing.main import Plumbing
from cpr.util.slackalert import alert_slack
from cpr.storage.main import Storage

# from cpr.tasks.main import Tasks

alert_slack()

deployment_resources = DeploymentResources()
plumbing = Plumbing()
storage = Storage(plumbing=plumbing)
backend = Backend(
    deployment_resources=deployment_resources, plumbing=plumbing, storage=storage
)
# tasks = Tasks()
# frontend = Frontend()
