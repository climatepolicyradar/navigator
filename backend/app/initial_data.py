#!/usr/bin/env python3

import os

from sqlalchemy.exc import IntegrityError

from app.core.security import get_password_hash
from app.db.models import User
from app.db.session import SessionLocal


def create_user(email, password):
    db = SessionLocal()

    db_user = User(
        email=email,
        hashed_password=get_password_hash(password),
        is_active=True,
        is_superuser=True,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)


def create_superuser() -> None:
    superuser_email = os.getenv("SUPERUSER_EMAIL")
    try:
        create_user(superuser_email, os.getenv("SUPERUSER_PASSWORD"))
    except IntegrityError:
        print(
            f"Skipping - super user already exists with email/username {superuser_email}"
        )


def create_loader_machine_user() -> None:
    machineuser_email = os.getenv("MACHINE_USER_LOADER_EMAIL")
    try:

        create_user(
            machineuser_email,
            os.getenv("MACHINE_USER_LOADER_PASSWORD"),
        )
    except IntegrityError:
        print(
            f"Skipping - loader machine user already exists with email/username {machineuser_email}"
        )


if __name__ == "__main__":
    print("Creating initial data...")
    create_superuser()
    create_loader_machine_user()
    print("Done creating initial data")
