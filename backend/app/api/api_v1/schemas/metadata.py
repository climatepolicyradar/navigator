from datetime import datetime
from typing import Any, Mapping, Optional

from pydantic import BaseModel


class Source(BaseModel):  # noqa: D101
    name: str


class Event(BaseModel):  # noqa: D101
    name: str
    description: str
    created_ts: datetime

    def to_json(self) -> Mapping[str, Any]:
        """Provide a serialisable version of the model"""
        return {
            "name": self.name,
            "description": self.description,
            "created_ts": self.created_ts.isoformat(),
        }


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
    slug: str
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


class CCLWSourceCollection(BaseModel):
    """Metadata sources from CCLW."""

    categories: list[dict]
    document_types: list[dict]
    frameworks: list[dict]
    geographies: list[dict]
    hazards: list[dict]
    instruments: list[dict]
    keywords: list[dict]
    languages: list[dict]
    sectors: list[dict]
    sources: list[dict]
    topics: list[dict]


class SourceCollections(BaseModel):
    """Definition of the CCLW source collection."""

    CCLW: CCLWSourceCollection


class Config(BaseModel):
    """Definition of the metadata response object."""

    metadata: SourceCollections
