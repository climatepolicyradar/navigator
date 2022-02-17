#!/usr/bin/env python3

from app.db.crud import create_user
from app.db.schemas import UserCreate
from app.db.session import SessionLocal

import os


def create_superuser(email, password):
    db = SessionLocal()

    create_user(
        db,
        UserCreate(
            email=email,
            password=password,
            is_active=True,
            is_superuser=True,
        ),
    )


def init() -> None:
    create_superuser(os.getenv("SUPERUSER_EMAIL"), os.getenv("SUPERUSER_PASSWORD"))
    create_superuser(os.getenv("MACHINE_USER_LOADER_EMAIL"), os.getenv("MACHINE_USER_LOADER_PASSWORD"))


if __name__ == "__main__":
    print("Creating initial data")
    init()
    print("Done creating initial data")
