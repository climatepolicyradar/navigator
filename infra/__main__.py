"""Infra-as-code for CPR stack."""
from cpr.backend.main import Backend
from cpr.common import SharedResources
from cpr.plumbing.main import Plumbing
from cpr.storage.main import Storage

shared = SharedResources()
plumbing = Plumbing()
storage = Storage(plumbing=plumbing)
backend = Backend(shared=shared, plumbing=plumbing, storage=storage)
