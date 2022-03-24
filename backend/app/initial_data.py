#!/usr/bin/env python3

import os

from sqlalchemy.exc import IntegrityError

from app.db.crud.user import create_user
from app.db.schemas.user import UserCreate
from app.db.session import SessionLocal


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
    superuser_email = os.getenv("SUPERUSER_EMAIL")
    try:
        create_superuser(superuser_email, os.getenv("SUPERUSER_PASSWORD"))
    except IntegrityError:
        print(
            f"Skipping - super user already exists with email/username {superuser_email}"
        )

    machineuser_email = os.getenv("MACHINE_USER_LOADER_EMAIL")
    try:

        create_superuser(
            machineuser_email,
            os.getenv("MACHINE_USER_LOADER_PASSWORD"),
        )
    except IntegrityError:
        print(
            f"Skipping - loader machine user already exists with email/username {machineuser_email}"
        )


if __name__ == "__main__":
    print("Creating initial data...")
    init()
    print("Done creating initial data")
