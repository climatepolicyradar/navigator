import typing as t

from pydantic import BaseModel


class UserBase(BaseModel):  # noqa: D101
    email: str
    is_active: bool = True
    is_superuser: bool = False
    names: t.Optional[str] = None
    job_role: t.Optional[str] = None
    location: t.Optional[str] = None
    affiliation_organisation: t.Optional[str] = None
    affiliation_type: t.Optional[t.List[str]] = None
    policy_type_of_interest: t.Optional[t.List[str]] = None
    geographies_of_interest: t.Optional[t.List[str]] = None
    data_focus_of_interest: t.Optional[t.List[str]] = None


class UserOut(UserBase):  # noqa: D101
    pass


class UserCreate(UserBase):  # noqa: D101
    password: str

    class Config:  # noqa: D106
        orm_mode = True


class UserCreateWithActivationToken(UserCreate):  # noqa: D101
    with_activation_token: t.Optional[bool]


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
    email: str
    permissions: str = "user"
