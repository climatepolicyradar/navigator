import datetime
import typing as t

from pydantic import BaseModel

from app.db.schemas import _ValidatedDateComponents


class _DocumentBase(BaseModel):  # noqa: D106
    """Properties common across all of this model's schemas.

    Do not use directly.
    """

    loaded_ts: t.Optional[datetime.datetime]
    name: str
    source_url: t.Optional[str]
    url: t.Optional[str]
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
