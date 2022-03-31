import typing as t

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.core.security import get_password_hash
from app.db.models import User, ActivationToken
from app.db.schemas.user import (
    UserEdit,
    UserCreate,
    UserBase,
)


def get_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_user_by_email(db: Session, email: str) -> t.Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> t.List[User]:
    return [
        User.from_orm(user) for user in db.query(User).offset(skip).limit(limit).all()
    ]


def create_user(db: Session, user: t.Union[UserCreate, UserBase]):
    """Create a user.

    Allows creating a user without a password (e.g. by admins)
    """
    hashed_password = None
    if isinstance(user, UserCreate):
        hashed_password = get_password_hash(user.password)
    db_user = User(**user.dict(), hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return user


def edit_user(db: Session, user_id: int, user: UserEdit) -> User:
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    update_data = user.dict(exclude_unset=True)

    if user.password:
        update_data["hashed_password"] = get_password_hash(user.password)
        del update_data["password"]

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def activate_user(
    db: Session,
    user: User,
    activation_token: ActivationToken,
    password: str,
) -> User:
    """Activate a user.

    Sets a password, and toggles activation flags on user and activation_token.
    """

    user.hashed_password = get_password_hash(password)
    user.is_active = True
    db.add(user)

    activation_token.is_activated = True
    db.add(activation_token)

    db.commit()
    db.refresh(user)

    return user
