import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.api.api_v1.schemas.metadata import (
    Category,
    DocumentType,
    Event,
    Framework,
    Geography,
    Hazard,
    Instrument,
    Keyword,
    Language,
    Sector,
    Source,
    Topic,
)


class DocumentOverviewResponse(BaseModel):  # noqa: D101
    """A document overview returned in browse & related document lists"""

    document_id: int
    name: str
    description: str
    country_code: str
    country_name: str
    publication_ts: datetime.datetime

    class Config:  # noqa: D106
        frozen = True


class DocumentDetailResponse(BaseModel):
    """A response containing detailed information about a document."""

    id: int
    loaded_ts: Optional[datetime.datetime]
    name: str
    description: str
    publication_ts: datetime.datetime
    source_url: str
    url: str
    content_type: str

    type: DocumentType
    source: Source
    category: Category
    geography: Geography

    frameworks: List[Framework]
    hazards: List[Hazard]
    instruments: List[Instrument]
    keywords: List[Keyword]
    languages: List[Language]
    sectors: List[Sector]
    topics: List[Topic]

    events: List[Event]
    related_documents: Optional[List[DocumentOverviewResponse]] = None

    class Config:  # noqa: D106
        frozen = True


class DocumentCreateRequest(BaseModel):  # noqa: D106
    """Details of a document to create - metadata will be validated & looked up."""

    loaded_ts: Optional[datetime.datetime]
    publication_ts: Optional[datetime.datetime]
    name: str
    description: str
    source_url: str
    url: str
    md5_sum: str

    type: str
    source: str
    category: str

    frameworks: List[str]
    geography: str
    hazards: List[str]
    instruments: List[str]
    keywords: List[str]
    languages: List[str]
    sectors: List[str]
    topics: List[str]

    events: List[Event]

    class Config:  # noqa: D106
        orm_mode = True
        validate_assignment = True


# TODO: replace doc-doc with proper association model
class DocumentAssociationCreateRequest(BaseModel):
    """Schema for associations create request."""

    document_id_from: int
    document_id_to: int
    name: str
    type: str


class DocumentAssociationCreateResponse(DocumentAssociationCreateRequest):
    """Schema for associations create response."""

    id: int

    class Config:  # noqa: D106
        orm_mode = True