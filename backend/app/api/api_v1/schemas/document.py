import datetime
from typing import Any, Mapping, Optional, Sequence

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
    import_id: str
    slug: str
    name: str
    postfix: Optional[str]
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
    postfix: Optional[str]
    description: str
    publication_ts: datetime.datetime
    source_url: Optional[str]
    url: Optional[str]
    content_type: Optional[str]
    md5_sum: Optional[str]

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


class DocumentUploadRequest(BaseModel):
    """Details of a file we wish to upload."""

    filename: str
    overwrite: Optional[bool] = False


class DocumentUploadResponse(BaseModel):
    """Details required to upload a document to our backend storage."""

    presigned_upload_url: str
    cdn_object: str


class DocumentCreateRequest(BaseModel):  # noqa: D106
    """Details of a document to create - metadata will be validated & looked up."""

    publication_ts: datetime.datetime
    name: str
    description: str
    postfix: Optional[str]
    source_url: Optional[str]

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

    def to_json(self) -> Mapping[str, Any]:
        """Provide a serialisable version of the model"""

        json_dict = self.dict()
        json_dict["publication_ts"] = (
            self.publication_ts.isoformat() if self.publication_ts is not None else None
        )
        json_dict["events"] = [event.to_json() for event in self.events]
        return json_dict

    class Config:  # noqa: D106
        orm_mode = True
        validate_assignment = True


class DocumentParserInput(DocumentCreateRequest):
    """Extend the document create request with the slug calculated during import."""

    slug: str


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


class DocumentUploadCompleteRequest(BaseModel):
    """Information generated during the upload of a document that should be stored."""

    md5_sum: str
    content_type: str


class BulkImportValidatedResult(BaseModel):
    """Response for bulk import request."""

    document_count: int
    document_added_count: int
    document_skipped_count: int
    document_skipped_ids: list[str]
    csv_s3_location: str


class DocumentUpdateRequest(BaseModel):
    """The current supported fields allowed for update."""

    md5_sum: Optional[str]
    content_type: Optional[str]
    cdn_object: Optional[str]
