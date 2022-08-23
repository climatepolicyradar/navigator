import typing as t

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.core.security import get_password_hash
from app.db.models import User, PasswordResetToken
from app.api.api_v1.schemas.user import User as UserSchema, UserCreate, UserCreateAdmin


def get_user(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_user_by_email(db: Session, email: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_users(db: Session, skip: int = 0, limit: int = 100) -> t.List[UserSchema]:
    return [
        UserSchema.from_orm(user)
        for user in db.query(User).offset(skip).limit(limit).all()
    ]


def create_user(db: Session, user: t.Union[UserCreate, UserCreateAdmin]) -> User:
    """Create a user."""
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def deactivate_user(db: Session, user_id: int) -> User:
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    user.is_active = False  # type: ignore
    user.hashed_password = None  # type: ignore
    db.add(user)
    db.commit()
    return user


def edit_user(
    db: Session, user_id: int, user: t.Union[UserCreate, UserCreateAdmin]
) -> User:
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
    password_reset_token: PasswordResetToken,
    password: str,
) -> User:
    """Activate a user.

    Sets a password, and toggles activation flags on user and password_reset_token.
    """

    user.hashed_password = get_password_hash(password)  # type: ignore
    user.is_active = True  # type: ignore
    db.add(user)

    password_reset_token.is_redeemed = True  # type: ignore
    db.add(password_reset_token)

    db.commit()
    db.refresh(user)

    return user
