import random
import string

from sqlalchemy.orm import Session

from app.db.models import ActivationToken


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
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))
