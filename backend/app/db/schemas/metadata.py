from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Source(BaseModel):  # noqa: D101
    name: str


class Event(BaseModel):  # noqa: D101
    # document_id: int  # this won't be posted by loader.
    name: str
    description: str
    created_ts: datetime


class SectorCreate(BaseModel):  # noqa: D101
    name: str
    description: str


class Sector(BaseModel):  # noqa: D101
    name: str
    description: str
    source: Source


class InstrumentCreate(BaseModel):  # noqa: D101
    name: str
    description: str


class Instrument(BaseModel):  # noqa: D101
    name: str
    description: str
    source: Source


class Framework(BaseModel):  # noqa: D101
    name: str
    description: str


class Hazard(BaseModel):  # noqa: D101
    name: str
    description: str


class Keyword(BaseModel):  # noqa: D101
    name: str
    description: str


class Language(BaseModel):  # noqa: D101
    language_code: str
    part1_code: Optional[str]
    part2_code: Optional[str]
    name: str


class Geography(BaseModel):  # noqa: D101
    display_value: str
    value: str
    type: str


class DocumentType(BaseModel):  # noqa: D101
    name: str
    description: str


class Category(BaseModel):  # noqa: D101
    name: str
    description: str


# TODO: Remove when the rename from Response -> Topic is complete
class Response(BaseModel):  # noqa: D101
    name: str
    description: str


class Topic(BaseModel):  # noqa: D101
    """Was 'Response' previously."""

    name: str
    description: str
