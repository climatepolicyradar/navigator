import typing as t

from fastapi import APIRouter, Depends, Request, Response

from app.core.auth import get_current_active_superuser
from app.core.email import send_email, EmailType
from app.db.crud.user import (
    create_user,
    deactivate_user,
    edit_user,
    get_user,
    get_users,
    create_password_reset_token,
)
from app.db.schemas.user import User, UserBase
from app.db.session import get_db

admin_users_router = r = APIRouter()


@r.get(
    "/users",
    response_model=t.List[User],
    response_model_exclude_none=True,
)
# TODO paginate
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
    user: UserBase,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """Creates a new user"""
    db_user = create_user(db, user)
    activation_token = create_password_reset_token(db, db_user.id)

    send_email(EmailType.account_new, db_user, activation_token)

    return db_user


@r.put("/users/{user_id}", response_model=User, response_model_exclude_none=True)
async def user_edit(
    request: Request,
    user_id: int,
    user: UserBase,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """Updates existing user"""
    updated_user = edit_user(db, user_id, user)

    send_email(EmailType.account_changed, updated_user)

    return updated_user


@r.delete("/users/{user_id}", response_model=User, response_model_exclude_none=True)
async def user_delete(
    request: Request,
    user_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """Deletes existing user"""
    return deactivate_user(db, user_id)


@r.delete("/passwords/{user_id}", response_model=bool, response_model_exclude_none=True)
async def delete_password(
    request: Request,
    user_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """Deletes a password for a user, and kicks off password-reset flow."""

    deactivated_user = deactivate_user(db, user_id)
    activation_token = create_password_reset_token(db, user_id)
    send_email(EmailType.password_reset_requested, deactivated_user, activation_token)
    return True
