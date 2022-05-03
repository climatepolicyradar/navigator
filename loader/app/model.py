"""External data models.

These models represent all the external data we need from a 3rd-party data contribution.
It will be provided to us as a dictionary, with key/value:

    Key => PolicyData
"""


from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict


@dataclass(frozen=True, eq=True)
class Key:
    """A key representing an action's unique constraint in the DB"""

    policy_name: str
    policy_date: datetime
    country_code: str
    policy_type: str


@dataclass
class Doc:  # noqa: D101
    doc_name: str
    doc_languages: List[str]
    doc_url: str
    # metadata
    events: List[str]
    sectors: List[str]
    instruments: List[str]
    frameworks: List[str]
    responses: List[str]
    hazards: List[str]


@dataclass(frozen=True)
class PolicyData(Key):  # noqa: D101
    policy_description: str
    docs: List[Doc]


PolicyLookup = Dict[Key, PolicyData]
