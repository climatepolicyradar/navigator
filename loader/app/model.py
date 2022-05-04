"""External data models.

These models represent all the external data we need from a 3rd-party data contribution.
It will be provided to us as a dictionary, with key/value:

    Key => PolicyData
"""


from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional


@dataclass(frozen=True, eq=True)
class Key:
    """A key representing a related set of documents.

    Previously, this represented an action's unique constraint in the DB.
    However, documents will have their own dates and categories, so these
    attributes are now optional, and can be used instead of the document-specific
    attributes if there's only one doc, or if a set of docs share these attributes.
    """

    policy_name: str
    country_code: str
    policy_date: Optional[str]
    policy_category: Optional[str]


@dataclass
class Doc:  # noqa: D101
    doc_name: str
    doc_languages: List[str]
    doc_url: str
    document_type: str
    document_date: Optional[datetime]
    document_category: str
    # metadata
    events: List[str]
    sectors: List[str]
    instruments: List[str]
    frameworks: List[str]
    responses: List[str]
    hazards: List[str]
    keywords: List[str]


@dataclass(frozen=True)
class PolicyData(Key):  # noqa: D101
    policy_description: Optional[str]
    docs: List[Doc]


PolicyLookup = Dict[Key, PolicyData]
