from enum import Enum


# This can be managed by admins via a
# future admin console.
class CCLWActionType(Enum):
    legislative = "Law"
    executive = "Policy"
