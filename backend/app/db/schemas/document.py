import datetime
import typing as t

from pydantic import BaseModel, HttpUrl, conint, validator

from app.db.models.document import DocumentInvalidReason


class _DocumentBase(BaseModel):  # noqa: D106
    """Properties common across all of this model's schemas.

    Do not use directly.
    """

    name: str
    language_id: t.Optional[int]
    source_url: t.Optional[HttpUrl]
    s3_url: t.Optional[HttpUrl]


class _DocumentInDBBase(_DocumentBase):
    """Properties in the DB.

    Do not use directly.
    """

    document_id: int
    action_id: int
    document_date: datetime.date
    document_mod_date: datetime.date
    is_valid: bool
    invalid_reason: t.Optional[DocumentInvalidReason]

    class Config:  # noqa: D106
        orm_mode = True
        validate_assignment = True


class DocumentCreate(_DocumentBase):  # noqa: D101, D106
    year: conint(ge=1900, le=datetime.datetime.now().year)
    month: t.Optional[conint(ge=1, le=12)]
    day: t.Optional[conint(ge=1, le=31)]

    @validator("month", "day")
    def set_date(cls, val):  # noqa: D102
        return val or 1


class DocumentCreateInternal(DocumentCreate):
    """Like DocumentCreate, but with extra data that only the backend can set."""

    action_id: int
    is_valid: bool
    invalid_reason: t.Optional[DocumentInvalidReason]
    document_mod_date: datetime.date


class Document(_DocumentInDBBase):
    """A Document to return to the client"""


class DocumentInDB(_DocumentInDBBase):
    """A Document as stored in the DB"""
