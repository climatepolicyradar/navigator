from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status
from jwt import PyJWTError

from app.core import security
from app.db import session
from app.db.crud.user import get_user_by_email
from app.db.models import User
from app.api.api_v1.schemas.user import JWTUser


CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def _get_jwt_user(token: str = Depends(security.oauth2_scheme)) -> JWTUser:
    """Light-weight user-retrieval that only decodes the JWT."""
    try:
        payload = jwt.decode(
            token, security.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        email: Optional[str] = payload.get("sub")
        if email is None:
            raise CREDENTIALS_EXCEPTION
        permissions: Optional[str] = payload.get("permissions")
        if permissions is None:
            raise CREDENTIALS_EXCEPTION
        is_active: Optional[bool] = payload.get("is_active")
        if is_active is None:
            raise CREDENTIALS_EXCEPTION

        jwt_user = JWTUser(
            email=email,
            is_superuser=permissions == "admin",
            is_active=is_active,
        )
        return jwt_user
    except PyJWTError:
        raise CREDENTIALS_EXCEPTION


async def get_current_active_user(
    current_user: JWTUser = Depends(_get_jwt_user),
) -> JWTUser:
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive User")
    return current_user


async def get_current_active_superuser(
    current_user: JWTUser = Depends(get_current_active_user),
) -> JWTUser:
    if not current_user.is_superuser:
        raise HTTPException(status_code=404, detail="Not Found")
    return current_user


async def _get_current_db_user(
    db=Depends(session.get_db),
    jwt_user: JWTUser = Depends(_get_jwt_user),
) -> User:
    """Heavier-weight user-retrieval that fetches the user from the DB after decoding the JWT."""
    user = get_user_by_email(db, jwt_user.email)
    if user is None:
        raise CREDENTIALS_EXCEPTION
    return user


async def get_current_active_db_user(
    current_user: User = Depends(_get_current_db_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive User")
    return current_user


async def get_current_active_db_superuser(
    current_user: User = Depends(get_current_active_db_user),
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(status_code=404, detail="Not Found")
    return current_user


def authenticate_user(db, email: str, password: str) -> Optional[User]:
    try:
        user = get_user_by_email(db, email)
    except HTTPException:
        return None
    if not user:
        return None
    if not security.verify_password(password, str(user.hashed_password)):
        return None
    return user
