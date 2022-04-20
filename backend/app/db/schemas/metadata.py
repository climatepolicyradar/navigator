from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.db.schemas.document import DocumentCreate


class Event(BaseModel):  # noqa: D101
    document_id: int
    name: str
    description: str
    created_ts = datetime


class Sector(BaseModel):  # noqa: D101
    name: str
    description: str


class Instrument(BaseModel):  # noqa: D101
    name: str
    description: str


class Framework(BaseModel):  # noqa: D101
    name: str
    description: str


class DocumentResponse(BaseModel):  # noqa: D101
    name: str
    description: str


class Hazard(BaseModel):  # noqa: D101
    name: str
    description: str


class DocumentCreateWithMetadata(BaseModel):  # noqa: D101
    """Create a document with all its metadata."""

    document: DocumentCreate
    source_id: int
    events: List[Event]
    sectors: List[Sector]
    instruments: List[Instrument]
    frameworks: List[Framework]
    responses: List[DocumentResponse]
    hazards: List[Hazard]
    language_codes: List[str]
    # passages?
