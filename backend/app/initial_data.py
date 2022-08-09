#!/usr/bin/env python3

import os

from sqlalchemy.exc import IntegrityError

from app.core.security import get_password_hash
from app.db.models import User
from app.db.session import SessionLocal

from app.data_migrations import (
    populate_document_type,
    populate_geography,
    populate_language,
    populate_source,
    populate_geo_statistics,
)


def run_data_migrations(db):
    """Populate lookup tables with standard values"""
    populate_source(db)
    populate_language(db)
    populate_document_type(db)
    populate_geography(db)

    db.commit()  # Geography data is used to geo-stats so commit here

    populate_geo_statistics(db)
    # TODO - framework, keyword, instrument, hazard


def create_user(db, email, password):
    with db.begin_nested():
        db_user = User(
            email=email,
            hashed_password=get_password_hash(password),
            is_active=True,
            is_superuser=True,
        )
        db.add(db_user)
        db.flush()


def create_superuser(db) -> None:
    superuser_email = os.getenv("SUPERUSER_EMAIL")
    try:
        create_user(db, superuser_email, os.getenv("SUPERUSER_PASSWORD"))
    except IntegrityError:
        print(
            f"Skipping - super user already exists with email/username {superuser_email}"
        )


def create_loader_machine_user(db) -> None:
    machineuser_email = os.getenv("MACHINE_USER_LOADER_EMAIL")
    try:

        create_user(
            db,
            machineuser_email,
            os.getenv("MACHINE_USER_LOADER_PASSWORD"),
        )
    except IntegrityError:
        print(
            f"Skipping - loader machine user already exists with email/username {machineuser_email}"
        )


def populate_initial_data(db):
    print("Creating superuser...")
    create_superuser(db)

    print("Creating loader machine user...")
    create_loader_machine_user(db)

    print("Running data migrations...")
    run_data_migrations(db)


if __name__ == "__main__":
    print("Creating initial data...")
    db = SessionLocal()
    populate_initial_data(db)
    db.commit()
    print("Done creating initial data")
