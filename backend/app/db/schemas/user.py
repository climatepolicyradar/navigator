import typing as t

from pydantic import BaseModel


class UserBaseWithoutFlags(BaseModel):  # noqa: D101
    email: str
    names: t.Optional[str] = None
    job_role: t.Optional[str] = None
    location: t.Optional[str] = None
    affiliation_organisation: t.Optional[str] = None
    affiliation_type: t.Optional[t.List[str]] = None
    policy_type_of_interest: t.Optional[t.List[str]] = None
    geographies_of_interest: t.Optional[t.List[str]] = None
    data_focus_of_interest: t.Optional[t.List[str]] = None


class UserBase(UserBaseWithoutFlags):  # noqa: D101
    is_active: bool = False
    is_superuser: bool = False


class UserCreate(UserBaseWithoutFlags):  # noqa: D101
    """Used by regular users"""


class UserCreateAdmin(UserBase):  # noqa: D101
    """Used by admin"""


class UserOut(UserBase):  # noqa: D101
    pass


class ResetPassword(BaseModel):
    """Resets a password with a token (latter usu. sent to requester's inbox)."""

    token: str
    password: str


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
