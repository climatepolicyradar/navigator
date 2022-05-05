from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status
from jwt import PyJWTError

from app.core import security
from app.db import session
from app.db.crud.user import get_user_by_email
from app.db.models import User


async def get_current_user(
    db=Depends(session.get_db), token: str = Depends(security.oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, security.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        email: Optional[str] = payload.get("sub")
        if email is None:
            raise credentials_exception
        permissions: Optional[str] = payload.get("permissions")
        if permissions is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    user = get_user_by_email(db, email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive User")
    return current_user


async def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
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
    if not security.verify_password(password, user.hashed_password):
        return None
    return user
