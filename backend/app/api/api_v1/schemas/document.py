import datetime
from typing import Optional, Sequence

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
    """A document overview returned in browse & related document Sequences"""

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
    name: str
    description: str
    publication_ts: datetime.datetime
    source_url: Optional[str]
    url: Optional[str]
    content_type: Optional[str]

    slug: Optional[str]
    import_id: Optional[str]

    type: DocumentType
    source: Source
    category: Category
    geography: Geography

    frameworks: Sequence[Framework]
    hazards: Sequence[Hazard]
    instruments: Sequence[Instrument]
    keywords: Sequence[Keyword]
    languages: Sequence[Language]
    sectors: Sequence[Sector]
    topics: Sequence[Topic]

    events: Sequence[Event]
    related_documents: Optional[Sequence[DocumentOverviewResponse]] = None

    class Config:  # noqa: D106
        frozen = True


class DocumentCreateRequest(BaseModel):  # noqa: D106
    """Details of a document to create - metadata will be validated & looked up."""

    publication_ts: Optional[datetime.datetime]
    name: str
    description: str
    source_url: Optional[str]
    url: Optional[str]
    md5_sum: Optional[str]

    type: str
    source: str
    import_id: str
    category: str

    frameworks: Sequence[str]
    geography: str
    hazards: Sequence[str]
    instruments: Sequence[str]
    keywords: Sequence[str]
    languages: Sequence[str]
    sectors: Sequence[str]
    topics: Sequence[str]

    events: Sequence[Event]

    class Config:  # noqa: D106
        orm_mode = True
        validate_assignment = True


class RelationshipCreateRequest(BaseModel):
    """Schema for Relationship create request."""

    name: str
    type: str
    description: str


class RelationshipEntityResponse(RelationshipCreateRequest):
    """Response for Relationship create request."""

    id: int

    class Config:  # noqa: D106
        orm_mode = True


class RelationshipGetResponse(BaseModel):
    """Response for Relationship get request."""

    relationships: Sequence[RelationshipEntityResponse]

    class Config:  # noqa: D106
        orm_mode = True


class RelationshipAndDocumentsGetResponse(BaseModel):
    """Response for Relationship get request."""

    relationship: RelationshipEntityResponse
    documents: Optional[Sequence[DocumentOverviewResponse]] = None
