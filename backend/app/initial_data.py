#!/usr/bin/env python3

from app.db.crud import create_user
from app.db.schemas import UserCreate
from app.db.session import SessionLocal

import os


def init() -> None:
    db = SessionLocal()

    superuser_email = os.environ.get("SUPERUSER_EMAIL", "")
    superuser_pw = os.environ.get("SUPERUSER_PASSWORD", "")

    create_user(
        db,
        UserCreate(
            email=superuser_email,
            password=superuser_pw,
            is_active=True,
            is_superuser=True,
        ),
    )


if __name__ == "__main__":
    print("Creating superuser")
    init()
    print("Superuser created")
