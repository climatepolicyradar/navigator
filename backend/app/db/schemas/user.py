import typing as t

from pydantic import BaseModel


class UserBase(BaseModel):  # noqa: D101
    email: str
    is_active: bool = True
    is_superuser: bool = False
    first_name: t.Optional[str] = None
    last_name: t.Optional[str] = None


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
    email: str
    permissions: str = "user"
