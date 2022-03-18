from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict


@dataclass(frozen=True, eq=True)
class Key:
    # class Key:
    """A key representing an action's unique constraint in the DB"""
    policy_name: str
    policy_date: datetime
    country_code: str
    policy_type: str
    # source_id: 1  # always 1 for CCLW


@dataclass
class Doc:
    doc_name: str
    doc_language: str
    doc_url: str


@dataclass(frozen=True)
class PolicyData(Key):
    policy_description: str
    docs: List[Doc]


PolicyLookup = Dict[Key, PolicyData]
