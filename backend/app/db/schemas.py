import datetime
import typing as t

from pydantic import BaseModel, HttpUrl, conint, validator


class UserBase(BaseModel):  # noqa: D101
    email: str
    is_active: bool = True
    is_superuser: bool = False
    first_name: str = None
    last_name: str = None


class UserOut(UserBase):  # noqa: D101
    pass


class UserCreate(UserBase):  # noqa: D101
    password: str

    class Config:  # noqa: D106
        orm_mode = True


class UserEdit(UserBase):  # noqa: D101
    password: t.Optional[str] = None

    class Config:  # noqa: D106
        orm_mode = True


class User(UserBase):  # noqa: D101
    id: int

    class Config:  # noqa: D106
        orm_mode = True


class Token(BaseModel):  # noqa: D101
    access_token: str
    token_type: str


class TokenData(BaseModel):  # noqa: D101
    email: str = None
    permissions: str = "user"


class DocumentBase(BaseModel):  # noqa: D101, D106
    name: str
    language_id: t.Optional[int]
    source_url: t.Optional[HttpUrl]
    s3_url: t.Optional[HttpUrl]
    year: conint(ge=1900, le=datetime.datetime.now().year)
    month: t.Optional[conint(ge=1, le=12)]
    day: t.Optional[conint(ge=1, le=31)]

    @validator("month", "day")
    def set_date(cls, val):  # noqa: D102
        return val or 1

    class Config:  # noqa: D106
        orm_mode = True
        validate_assignment = True


class DocumentCreate(DocumentBase):  # noqa: D101
    action_id: int
    document_mod_date: datetime.date


class ActionBase(BaseModel):  # noqa: D101
    name: str
    description: t.Optional[str]
    year: conint(ge=1900, le=datetime.datetime.now().year)
    month: t.Optional[conint(ge=1, le=12)]
    day: t.Optional[conint(ge=1, le=31)]
    geography_id: int
    type_id: int
    source_id: int
    documents: t.List[DocumentBase]

    @validator("month", "day")
    def set_date(cls, val):  # noqa: D102
        return val or 1

    class Config:  # noqa: D106
        orm_mode = True
        validate_assignment = True


class ActionCreate(ActionBase):  # noqa: D101
    source_json: t.Optional[dict] = None
    mod_date: datetime.date
