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
    try:
        create_superuser(os.getenv("SUPERUSER_EMAIL"), os.getenv("SUPERUSER_PASSWORD"))
    except IntegrityError:
        print("Skipping - super user already exists")

    try:
        create_superuser(
            os.getenv("MACHINE_USER_LOADER_EMAIL"),
            os.getenv("MACHINE_USER_LOADER_PASSWORD"),
        )
    except IntegrityError:
        print("Skipping - loader machine user already exists")


if __name__ == "__main__":
    print("Creating initial data...")
    init()
    print("Done creating initial data")
