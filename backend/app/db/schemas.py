import datetime
import typing as t

from pydantic import BaseModel, HttpUrl, conint, validator


class UserBase(BaseModel):
    email: str
    is_active: bool = True
    is_superuser: bool = False
    first_name: str = None
    last_name: str = None


class UserOut(UserBase):
    pass


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True


class UserEdit(UserBase):
    password: t.Optional[str] = None

    class Config:
        orm_mode = True


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str = None
    permissions: str = "user"


class DocumentBase(BaseModel):
    name: str
    language_id: int
    source_url: t.Optional[HttpUrl]
    s3_url: t.Optional[HttpUrl]
    year: conint(ge=1900, le=datetime.datetime.now().year)
    month: t.Optional[conint(ge=1, le=12)]
    day: t.Optional[conint(ge=1, le=31)]

    @validator("month", "day")
    def set_date(cls, val):
        return val or 1

    class Config:
        orm_mode = True
        validate_assignment = True


class DocumentCreate(DocumentBase):
    action_id: int
    document_mod_date: datetime.date


class ActionBase(BaseModel):
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
    def set_date(cls, val):
        return val or 1

    class Config:
        orm_mode = True
        validate_assignment = True


class ActionCreate(ActionBase):
    source_json: t.Optional[dict] = None
    mod_date: datetime.date
