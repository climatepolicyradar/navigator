import logging
from typing import cast

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.exc import IntegrityError

from app.api.api_v1.routers.admin import ACCOUNT_ACTIVATION_EXPIRE_MINUTES
from app.core.email import (
    send_new_account_email,
    send_password_changed_email,
    send_password_reset_email,
)
from app.core.ratelimit import limiter
from app.db.crud.password_reset import (
    create_password_reset_token,
    get_password_reset_token_by_token,
    get_password_reset_token_by_user_id,
)
from app.db.crud.user import (
    activate_user,
    create_user,
    get_user,
    get_user_by_email,
)
from app.db.schemas.user import ResetPassword, User, UserCreate
from app.db.session import get_db

unauthenticated_router = r = APIRouter()

logger = logging.getLogger(__file__)


@r.post("/registrations", response_model=bool, response_model_exclude_none=True)
@limiter.limit("6/minute")
async def user_create(
    request: Request,  # request unused, but required for rate limiting
    user: UserCreate,
    db=Depends(get_db),
):
    """
    Registers a new user.

    :param user: Details of the user to create
    :param db: Database connection to allow creation of user
    :returns: Always returns True (do not signal failure/success based on
        existing registered email to avoid leaking registered user details)
    """
    try:
        db_user = create_user(db, user)
    except IntegrityError:
        logger.error(f"Email already registered: {user.email}")
        return True

    activation_token = create_password_reset_token(
        db, cast(int, db_user.id), minutes=ACCOUNT_ACTIVATION_EXPIRE_MINUTES
    )
    send_new_account_email(db_user, activation_token)

    return True


@r.post("/activations", response_model=User, response_model_exclude_none=True)
@limiter.limit("6/minute")
async def set_password(
    request: Request,  # request unused, but required for rate limiting
    payload: ResetPassword,
    db=Depends(get_db),
):
    """Activates a new user and sets a password."""

    reset_token = get_password_reset_token_by_token(db, payload.token)
    user = get_user(db, cast(int, reset_token.user_id))
    activated_user = activate_user(db, user, reset_token, payload.password)
    send_password_changed_email(activated_user)
    return activated_user


@r.post(
    "/password-reset/{email}", response_model=bool, response_model_exclude_none=True
)
@limiter.limit("6/minute")
async def request_password_reset(
    request: Request,  # request unused, but required for rate limiting
    email: str,
    db=Depends(get_db),
):
    """
    Kicks off password-reset flow.

    This is the unauthenticated flow, which swallows a lot of the underlying exceptions,
    so as not to leak data.

    Also see the equivalent admin endpoint.
    """

    try:
        user = get_user_by_email(db, email)
        password_reset_token = get_password_reset_token_by_user_id(
            db,
            cast(int, user.id),
        )
        if password_reset_token is None:
            password_reset_token = create_password_reset_token(
                db,
                cast(int, user.id),
            )
        send_password_reset_email(user, password_reset_token)
    except HTTPException:
        # if the user for this email couldn't be found, don't 404
        pass
    return True
