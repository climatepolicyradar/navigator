import logging

from fastapi import APIRouter, Depends, Request, Response

from app.core.auth import get_current_active_db_user
from app.db.crud.user import (
    edit_user,
)
from app.db.schemas.user import User, UserCreate
from app.db.session import get_db

users_router = r = APIRouter()

logger = logging.getLogger(__file__)


@r.get("/users/me", response_model=User, response_model_exclude_none=True)
async def user_me(
    response: Response,
    current_user=Depends(get_current_active_db_user),
):
    """Gets own user"""
    response.headers["Cache-Control"] = "no-cache, no-store, private"
    return current_user


@r.put("/users/me", response_model=User, response_model_exclude_none=True)
async def user_edit(
    request: Request,
    response: Response,
    user: UserCreate,
    db=Depends(get_db),
    current_user=Depends(get_current_active_db_user),
):
    """Updates existing user"""
    updated_user = edit_user(db, current_user.id, user)

    # TODO: send account updated email
    # send_account_updated_email(updated_user)

    response.headers["Cache-Control"] = "no-cache, no-store, private"
    return updated_user
