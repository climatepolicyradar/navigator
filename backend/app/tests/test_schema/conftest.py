import contextlib
import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.session import Base
from app.tests.test_schema.helpers import clean_tables


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
