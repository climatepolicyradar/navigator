import contextlib
import os

import pytest
from app.db.session import Base
from app.tests.test_schema.helpers import clean_tables
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database


@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    """Create a test database and use it for the whole test session."""

    test_db_url = os.environ.get("DATABASE_URL") + "_test"

    # Create the test database
    if database_exists(test_db_url):
        drop_database(test_db_url)
    create_database(test_db_url)
    test_engine = create_engine(test_db_url)
    Base.metadata.create_all(test_engine)

    # Run the tests
    yield

    # Drop the test database
    drop_database(test_db_url)


@pytest.fixture(scope="session")
def sqlalchemy_base():
    return Base


@pytest.fixture(scope="session")
def original_engine():
    engine = create_engine(os.environ.get("DATABASE_URL") + "_test")
    yield engine


@pytest.fixture()
def engine(original_engine, sqlalchemy_base):
    session_cls = sessionmaker(original_engine)
    sqlalchemy_base.metadata.create_all(original_engine)
    yield original_engine
    with contextlib.closing(session_cls()) as session:
        clean_tables(session, set(), sqlalchemy_base)
