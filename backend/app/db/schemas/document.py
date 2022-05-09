import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.db.schemas import _ValidatedDateComponents
from app.db.schemas.metadata import (
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


class _DocumentBase(BaseModel):  # noqa: D106
    """Properties common across all of this model's schemas.

    Do not use directly.
    """

    loaded_ts: Optional[datetime.datetime]
    name: str
    description: str
    source_url: str
    url: str
    md5_sum: str
    geography_id: int  # the loader gets this via API lookup, so it will exist in the API DB
    type_id: int  # the loader gets this via API lookup, so it will exist in the API DB
    source_id: int  # the loader gets this via API lookup, so it will exist in the API DB
    category_id: int  # the loader gets this via API lookup, so it will exist in the API DB


class _DocumentInDBBase(_DocumentBase):
    """Properties in the DB.

    Do not use directly.
    """

    id: int

    class Config:  # noqa: D106
        orm_mode = True
        validate_assignment = True


class DocumentCreate(_DocumentBase, _ValidatedDateComponents):  # noqa: D101, D106
    pass


class Document(_DocumentInDBBase):
    """A Document to return to the client"""


class DocumentInDB(_DocumentInDBBase):
    """A Document as stored in the DB"""


class _DocumentExtraDetail(BaseModel):
    events: List[Event]
    sectors: List[Sector]
    instruments: List[Instrument]
    frameworks: List[Framework]
    topics: List[Topic]
    hazards: List[Hazard]
    keywords: List[Keyword]


class DocumentCreateWithMetadata(_DocumentExtraDetail):  # noqa: D101
    """Create a document with all its metadata."""

    document: DocumentCreate
    source_id: int
    # the loader gets the language via API lookup, so it will exist on the API passages?
    language_ids: List[int]


class RelatedDocument(BaseModel):  # noqa: D101
    related_id: int
    name: str
    description: str
    country_code: str
    country_name: str
    year: int


class DocumentDetail(_DocumentExtraDetail):
    """A Document to return to the client for the Document cover page"""

    id: int
    loaded_ts: Optional[datetime.datetime]
    name: str
    description: str
    year: Optional[int]
    source_url: str
    url: str
    geography: Geography
    type: DocumentType
    source: Source
    category: Category
    languages: List[Language]
    sectors: List[Sector]
    topics: List[Topic]
    related_documents: List[RelatedDocument]
