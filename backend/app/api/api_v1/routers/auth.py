import logging

from app.core.security import create_access_token
from app.core.auth import authenticate_user
from app.db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

auth_router = r = APIRouter()

_LOGGER = logging.getLogger(__file__)


@r.post("/tokens")
async def login(db=Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    _LOGGER.info(
        "Auth token requested",
        extra={"props": {"user_id": form_data.username}},
    )

    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is de-activated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.is_superuser:
        permissions = "admin"
    else:
        permissions = "user"
    access_token = create_access_token(
        data={
            "sub": user.email,
            "permissions": permissions,
            "is_active": user.is_active,
        },
    )

    _LOGGER.info(
        "Auth token generated",
        extra={"props": {"user_id": form_data.username}},
    )
    return {"access_token": access_token, "token_type": "bearer"}
