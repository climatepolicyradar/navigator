import logging
import typing as t

from fastapi import APIRouter, Depends, Request, Response

from app.core.auth import get_current_active_superuser
from app.db.crud.activation_token import create_activation_token
from app.db.crud.user import create_user, delete_user, edit_user, get_user, get_users
from app.db.schemas.user import User, UserCreateWithActivationToken, UserEdit
from app.db.session import get_db

admin_users_router = r = APIRouter()

logger = logging.getLogger(__file__)


@r.get(
    "/users",
    response_model=t.List[User],
    response_model_exclude_none=True,
)
async def users_list(
    response: Response,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """Gets all users"""
    users = get_users(db)
    # This is necessary for react-admin to work
    response.headers["Content-Range"] = f"0-9/{len(users)}"
    return users


@r.get(
    "/users/{user_id}",
    response_model=User,
    response_model_exclude_none=True,
)
async def user_details(
    request: Request,
    user_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """Gets any user details"""
    user = get_user(db, user_id)
    return user


@r.post("/users", response_model=User, response_model_exclude_none=True)
async def user_create(
    request: Request,
    user: UserCreateWithActivationToken,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """Creates a new user"""
    db_user = create_user(db, user)
    if user.with_activation_token:
        activation_token = create_activation_token(db, db_user.id)
        logger.info(f"Account created with activation token={activation_token.token}")
        db_user.is_active = False
        # TODO send email
    return db_user


@r.put("/users/{user_id}", response_model=User, response_model_exclude_none=True)
async def user_edit(
    request: Request,
    user_id: int,
    user: UserEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """Updates existing user"""
    return edit_user(db, user_id, user)


@r.delete("/users/{user_id}", response_model=User, response_model_exclude_none=True)
async def user_delete(
    request: Request,
    user_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """Deletes existing user"""
    return delete_user(db, user_id)
