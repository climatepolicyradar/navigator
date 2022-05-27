from enum import Enum


# This can be managed by admins via a
# future admin console.
class CCLWActionType(Enum):
    """Maps CCLW action type to internal definition."""

    legislative = "Law"
    executive = "Policy"


# the source data doesn't have descriptions for things like events, or non-lookup/predefined metadata
DEFAULT_DESCRIPTION = "Imported by CPR loader"
