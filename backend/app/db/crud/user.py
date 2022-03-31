import datetime
import typing as t
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.core.security import get_password_hash
from app.core.util import random_string
from app.db.models import User, PasswordResetToken
from app.db.schemas.user import UserBase, User as UserSchema


def get_user(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_user_by_email(db: Session, email: str) -> t.Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> t.List[UserSchema]:
    return [
        UserSchema.from_orm(user)
        for user in db.query(User).offset(skip).limit(limit).all()
    ]


def create_user(db: Session, user: UserBase):
    """Create a user."""
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def deactivate_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    user.is_active = False
    user.hashed_password = None
    db.add(user)
    db.commit()
    return user


def edit_user(db: Session, user_id: int, user: UserBase) -> User:
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    update_data = user.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def activate_user(
    db: Session,
    user: User,
    activation_token: PasswordResetToken,
    password: str,
) -> User:
    """Activate a user.

    Sets a password, and toggles activation flags on user and activation_token.
    """

    user.hashed_password = get_password_hash(password)
    user.is_active = True
    db.add(user)

    activation_token.is_redeemed = True
    db.add(activation_token)

    db.commit()
    db.refresh(user)

    return user


def get_password_reset_token(
    db: Session,
    token: str,
) -> PasswordResetToken:
    activation_token: Optional[PasswordResetToken] = (
        db.query(PasswordResetToken)
        .filter(PasswordResetToken.token == token)
        .one_or_none()
    )
    if activation_token is None:
        raise HTTPException(status_code=404, detail="Token not found")
    if activation_token.expiry_ts > datetime.datetime.utcnow():
        raise HTTPException(status_code=404, detail="Token expired")
    if activation_token.is_redeemed:
        raise HTTPException(status_code=404, detail="Token already redeemed")

    return activation_token


def create_password_reset_token(
    db: Session,
    user_id: int,
) -> PasswordResetToken:
    # TODO make configurable
    future_date = datetime.datetime.utcnow() + datetime.timedelta(weeks=1)

    row = PasswordResetToken(
        user_id=user_id, token=random_string(), expiry_ts=future_date
    )

    db.add(row)
    db.commit()
    db.refresh(row)

    return row
