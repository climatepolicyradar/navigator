import logging

from fastapi import APIRouter, Depends, Request

from app.core.email import send_email, EmailType
from app.core.ratelimit import limiter
from app.db.crud.user import (
    get_user,
    activate_user,
    get_password_reset_token,
)
from app.db.schemas.user import User, ResetPassword
from app.db.session import get_db

unauthenticated_router = r = APIRouter()

logger = logging.getLogger(__file__)


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
    activated_user = activate_user(db, user, reset_token, payload.password)
    send_email(EmailType.password_changed, activated_user)
    return activated_user
