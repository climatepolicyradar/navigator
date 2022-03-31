import logging

from fastapi import APIRouter, Depends, Request

from app.core.auth import get_current_active_user
from app.core.email import send_email, EmailType
from app.core.ratelimit import limiter
from app.db.crud.user import (
    get_user,
    activate_user,
    edit_user,
    get_password_reset_token,
    create_password_reset_token,
    deactivate_user,
)
from app.db.schemas.user import User, ResetPassword, UserBase
from app.db.session import get_db

users_router = r = APIRouter()

logger = logging.getLogger(__file__)


@r.get("/users/me", response_model=User, response_model_exclude_none=True)
async def user_me(current_user=Depends(get_current_active_user)):
    """Gets own user"""

    return current_user


@r.put("/users/me", response_model=User, response_model_exclude_none=True)
async def user_edit(
    request: Request,
    user: UserBase,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Updates existing user"""

    updated_user = edit_user(db, current_user.id, user)
    send_email(EmailType.account_changed, updated_user)
    return updated_user


@r.post("/activations", response_model=User, response_model_exclude_none=True)
@limiter.limit("6/minute")
async def reset_password(
    request: Request,
    payload: ResetPassword,
    db=Depends(get_db),
):
    """Activates a new user and sets a password."""

    reset_token = get_password_reset_token(db, payload.token)
    user = get_user(db, reset_token.user_id)
    send_email(EmailType.password_changed, user)
    return activate_user(db, user, reset_token, payload.password)


@r.delete("/passwords/me", response_model=bool, response_model_exclude_none=True)
async def delete_password(
    request: Request,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Deletes a password, and kicks off password-reset flow."""

    deactivate_user(db, current_user.id)
    activation_token = create_password_reset_token(db, current_user.id)
    send_email(EmailType.password_reset_requested, current_user, activation_token)
    return True
