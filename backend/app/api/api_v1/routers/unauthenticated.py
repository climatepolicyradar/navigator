import logging

from fastapi import APIRouter, Depends, Request, HTTPException

from app.core.email import send_password_changed_email, send_password_reset_email
from app.core.ratelimit import limiter
from app.db.crud.user import (
    get_user,
    activate_user,
    get_user_by_email,
)
from app.db.crud.password_reset import (
    get_password_reset_token_by_token,
    get_password_reset_token_by_user_id,
    create_password_reset_token,
)
from app.db.schemas.user import User, ResetPassword
from app.db.session import get_db

unauthenticated_router = r = APIRouter()

logger = logging.getLogger(__file__)


@r.post("/activations", response_model=User, response_model_exclude_none=True)
@limiter.limit("6/minute")
async def set_password(
    request: Request,
    payload: ResetPassword,
    db=Depends(get_db),
):
    """Activates a new user and sets a password."""

    reset_token = get_password_reset_token_by_token(db, payload.token)
    user = get_user(db, reset_token.user_id)
    activated_user = activate_user(db, user, reset_token, payload.password)
    send_password_changed_email(activated_user)
    return activated_user


@r.post(
    "/password-reset/{email}", response_model=bool, response_model_exclude_none=True
)
@limiter.limit("6/minute")
async def request_password_reset(
    request: Request,
    email: str,
    db=Depends(get_db),
):
    """Deletes a password, and kicks off password-reset flow.

    This is the unauthenticated flow, which swallows a lot of the underlying exceptions,
    so as not to leak data.

    Also see the equivalent admin endpoint.
    """

    try:
        user = get_user_by_email(db, email)
        try:
            _ = get_password_reset_token_by_user_id(db, user.id)
            # if a token existed, hasn't expired, and hasn't been redeemed, then do nothing
        except HTTPException:
            # otherwise, create new token
            password_reset_token = create_password_reset_token(db, user.id)
            send_password_reset_email(user, password_reset_token)
    except HTTPException:
        # if the user for this email couldn't be found, don't 404
        pass
    return True
