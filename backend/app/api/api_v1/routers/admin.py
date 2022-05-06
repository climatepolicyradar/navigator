import typing as t

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.exc import IntegrityError

from app.core.auth import get_current_active_superuser
from app.core.email import send_email, EmailType
from app.db.crud.user import (
    create_user,
    deactivate_user,
    edit_user,
    get_user,
    get_users,
)
from app.db.crud.password_reset import (
    create_password_reset_token,
    invalidate_existing_password_reset_tokens,
)
from app.db.schemas.user import User, UserCreateAdmin
from app.db.session import get_db
from app.core.ratelimit import limiter

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
    user: UserCreateAdmin,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """Creates a new user"""
    try:
        db_user = create_user(db, user)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email already registered: {user.email}",
        )

    activation_token = create_password_reset_token(db, db_user.id)
    send_email(EmailType.account_new, db_user, activation_token)

    return db_user


@r.put("/users/{user_id}", response_model=User, response_model_exclude_none=True)
async def user_edit(
    request: Request,
    user_id: int,
    user: UserCreateAdmin,
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
    # TODO send email?
    return deactivate_user(db, user_id)


@r.post(
    "/password-reset/{user_id}", response_model=bool, response_model_exclude_none=True
)
@limiter.limit("6/minute")
async def request_password_reset(
    request: Request,
    user_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """Deletes a password for a user, and kicks off password-reset flow.

    As this flow is initiated by admins, it always
    - cancels existing tokens
    - creates a new token
    - sends an email

    Also see the equivalent unauthenticated endpoint.
    """

    deactivated_user = deactivate_user(db, user_id)
    invalidate_existing_password_reset_tokens(db, user_id)
    activation_token = create_password_reset_token(db, user_id)
    send_email(EmailType.password_reset_requested, deactivated_user, activation_token)
    return True
