import logging

from fastapi import APIRouter, Depends, Request

from app.core.auth import get_current_active_user
from app.core.ratelimit import limiter
from app.db.crud.activation_token import get_activation_token
from app.db.crud.user import get_user, activate_user
from app.db.schemas.user import User, UserCreateFromActivationToken
from app.db.session import get_db

users_router = r = APIRouter()

logger = logging.getLogger(__file__)


@r.get("/users/me", response_model=User, response_model_exclude_none=True)
async def user_me(current_user=Depends(get_current_active_user)):
    """Gets own user"""
    return current_user


@r.post("/users", response_model=User, response_model_exclude_none=True)
@limiter.limit("6/minute")
async def user_create(
    request: Request,
    payload: UserCreateFromActivationToken,
    db=Depends(get_db),
):
    """Activates a new user and sets a password."""

    activation_token = get_activation_token(db, payload.activation_token)
    user = get_user(db, activation_token.user_id)

    return activate_user(db, user, activation_token, payload.password)
