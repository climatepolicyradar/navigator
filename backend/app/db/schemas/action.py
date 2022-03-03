import datetime
import typing as t

from pydantic import BaseModel, conint, validator, Field

from app.db.schemas.document import Document, DocumentCreate


class _ActionBase(BaseModel):
    """Properties common across all of this model's schemas.

    Do not use directly.
    """

    name: str
    description: t.Optional[str]
    geography_id: int
    action_type_id: int
    action_source_id: int
    documents: t.List[Document]


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

    class Config:  # noqa: D106
        orm_mode = True
        validate_assignment = True


class ActionCreate(_ActionBase):
    """An action as created via API"""

    year: conint(ge=1900, le=datetime.datetime.now().year)
    month: t.Optional[conint(ge=1, le=12)]
    day: t.Optional[conint(ge=1, le=31)]

    documents: t.List[DocumentCreate]

    @validator("month", "day")
    def set_date(cls, val):  # noqa: D102
        return val or 1


class Action(_ActionInDBBase):
    """An Action to return to the client"""


class ActionInDB(_ActionInDBBase):
    """An Action as stored in the DB"""
