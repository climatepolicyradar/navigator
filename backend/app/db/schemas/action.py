import datetime
import typing as t

from app.db.schemas import _ValidatedDateComponents
from app.db.schemas.document import Document, DocumentCreate
from pydantic import BaseModel, Field


class _ActionBase(BaseModel):
    """Properties common across all of this model's schemas.

    Do not use directly.
    """

    name: str
    description: t.Optional[str]
    geography_id: int
    action_type_id: int
    action_source_id: int


class _ActionInDBBase(_ActionBase):
    """Properties in the DB.

    Do not use directly.
    """

    action_id: int
    action_date: datetime.date
    # TODO https://pydantic-docs.helpmanual.io/usage/types/#json-type ?
    # Disabling for now, as it's use is unclear.
    # action_source_json: t.Optional[dict] = None
    action_mod_date: datetime.date = Field(default_factory=datetime.datetime.utcnow)
    documents: t.List[Document]

    class Config:  # noqa: D106
        orm_mode = True
        validate_assignment = True


class ActionCreate(_ActionBase, _ValidatedDateComponents):
    """An action as created via API"""

    documents: t.List[DocumentCreate]


class Action(_ActionInDBBase):
    """An Action to return to the client"""


class ActionInDB(_ActionInDBBase):
    """An Action as stored in the DB"""
