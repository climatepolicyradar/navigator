import datetime
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_password_reset_token_expiry_ts
from app.core.util import random_string
from app.db.models import PasswordResetToken


def get_password_reset_token_by_token(
    db: Session,
    token: str,
) -> PasswordResetToken:
    password_reset_token: Optional[PasswordResetToken] = (
        db.query(PasswordResetToken)
        .filter(PasswordResetToken.token == token)
        .one_or_none()
    )
    return _validate_and_return(password_reset_token)


def get_password_reset_token_by_user_id(
    db: Session,
    user_id: int,
) -> PasswordResetToken:
    password_reset_token: Optional[PasswordResetToken] = (
        db.query(PasswordResetToken)
        .filter(PasswordResetToken.user_id == user_id)
        .one_or_none()
    )
    return _validate_and_return(password_reset_token)


def _validate_and_return(
    password_reset_token: Optional[PasswordResetToken],
) -> PasswordResetToken:
    if password_reset_token is None:
        raise HTTPException(status_code=404, detail="Token not found")
    if password_reset_token.expiry_ts < datetime.datetime.utcnow():
        raise HTTPException(status_code=404, detail="Token expired")
    if password_reset_token.is_redeemed:
        raise HTTPException(status_code=404, detail="Token already redeemed")
    if password_reset_token.is_cancelled:
        raise HTTPException(status_code=404, detail="Token is not valid")

    return password_reset_token


def create_password_reset_token(
    db: Session,
    user_id: int,
) -> PasswordResetToken:
    expiry_ts = get_password_reset_token_expiry_ts()

    row = PasswordResetToken(
        user_id=user_id, token=random_string(), expiry_ts=expiry_ts
    )

    db.add(row)
    db.commit()
    db.refresh(row)

    return row


def invalidate_existing_password_reset_tokens(db: Session, user_id: int) -> None:
    for existing_token in (
        db.query(PasswordResetToken).filter(PasswordResetToken.user_id == user_id).all()
    ):
        existing_token.is_cancelled = True
        db.add(existing_token)
        db.commit()