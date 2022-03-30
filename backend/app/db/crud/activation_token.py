import datetime
import random
import string
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models import ActivationToken


def get_activation_token(
    db: Session,
    token: str,
) -> ActivationToken:
    activation_token: Optional[ActivationToken] = (
        db.query(ActivationToken).filter(ActivationToken.token == token).one_or_none()
    )
    if activation_token is None:
        raise HTTPException(status_code=404, detail="Token not found")
    if activation_token.expiry_ts > datetime.datetime.utcnow():
        raise HTTPException(status_code=404, detail="Token expired")
    if activation_token.is_activated:
        raise HTTPException(status_code=404, detail="Token already activated")

    return activation_token


def create_activation_token(
    db: Session,
    user_id: int,
) -> ActivationToken:
    row = ActivationToken(
        user_id=user_id,
        token=random_string(),
    )

    db.add(row)
    db.commit()
    db.refresh(row)

    return row


def random_string(length=12):
    return "".join(random.choice(string.ascii_lowercase) for i in range(length))
