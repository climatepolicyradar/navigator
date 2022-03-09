import os
import typing as t

import pytest
from fastapi.testclient import TestClient
from moto import mock_s3
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

from app.core import config, security
from app.db.models.user import User
from app.db.session import Base, get_db
from app.main import app
from navigator.core.aws import S3Client, get_s3_client


@pytest.fixture
def s3_document_bucket_names() -> dict:
    return {
        "queue": "cpr-document-queue",
        "store": "cpr-document-store",
    }


@pytest.fixture
def test_s3_client(s3_document_bucket_names):
    bucket_names = s3_document_bucket_names.values()

    with mock_s3():
        s3_client = S3Client()
        for bucket in bucket_names:
            s3_client.client.create_bucket(
                Bucket=bucket,
                CreateBucketConfiguration={
                    "LocationConstraint": os.getenv("AWS_REGION")
                },
            )

        # Test document in queue for action submission
        s3_client.client.put_object(
            Bucket=s3_document_bucket_names["queue"],
            Key="test_document.pdf",
            Body=bytes(1024),
        )

        yield s3_client


def get_test_db_url() -> str:
    return f"{config.SQLALCHEMY_DATABASE_URI}_test"


@pytest.fixture
def create_test_db():
    """Create a test database and use it for the whole test session."""

    test_db_url = get_test_db_url()

    # Create the test database
    assert not database_exists(
        test_db_url
    ), f"Test database already exists at {test_db_url}. Aborting tests."
    create_database(test_db_url)
    try:
        test_engine = create_engine(test_db_url)
        Base.metadata.create_all(test_engine)

        # Run the tests
        yield
    finally:
        # Drop the test database
        drop_database(test_db_url)


@pytest.fixture
def test_db(create_test_db):
    """Provide a test DB.

    Modify the db session to automatically roll back after each test.
    This is to avoid tests affecting the database state of other tests.
    """
    # Connect to the test database
    engine = create_engine(
        get_test_db_url(),
    )

    connection = engine.connect()
    trans = connection.begin()

    # Run a parent transaction that can roll back all changes
    test_session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    test_session = test_session_maker()
    test_session.begin_nested()

    @event.listens_for(test_session, "after_transaction_end")
    def restart_savepoint(s, transaction):
        if transaction.nested and not transaction._parent.nested:
            s.expire_all()
            s.begin_nested()

    yield test_session

    # Roll back the parent transaction after the test is complete
    test_session.close()
    trans.rollback()
    connection.close()


@pytest.fixture
def client(test_db, test_s3_client):
    """Get a TestClient instance that reads/write to the test database."""

    def get_test_db():
        yield test_db

    def get_test_s3_client():
        yield test_s3_client

    app.dependency_overrides[get_db] = get_test_db
    app.dependency_overrides[get_s3_client] = get_test_s3_client

    yield TestClient(app)


@pytest.fixture
def test_password() -> str:
    return "securepassword"


def get_password_hash() -> str:
    """Password hashing can be expensive so a mock will be much faster"""
    return "supersecrethash"


@pytest.fixture
def test_user(test_db) -> User:
    """Make a test user in the database"""

    user = User(
        email="fake@email.com",
        hashed_password=get_password_hash(),
        is_active=True,
    )
    test_db.add(user)
    test_db.commit()
    return user


@pytest.fixture
def test_superuser(test_db) -> User:
    """Superuser for testing"""

    user = User(
        email="fakeadmin@email.com",
        hashed_password=get_password_hash(),
        is_superuser=True,
    )
    test_db.add(user)
    test_db.commit()
    return user


def verify_password_mock(first: str, second: str) -> bool:
    return True


@pytest.fixture
def user_token_headers(
    client: TestClient, test_user, test_password, monkeypatch
) -> t.Dict[str, str]:
    monkeypatch.setattr(security, "verify_password", verify_password_mock)

    login_data = {
        "username": test_user.email,
        "password": test_password,
    }
    r = client.post("/api/token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


@pytest.fixture
def superuser_token_headers(
    client: TestClient, test_superuser, test_password, monkeypatch
) -> t.Dict[str, str]:
    monkeypatch.setattr(security, "verify_password", verify_password_mock)

    login_data = {
        "username": test_superuser.email,
        "password": test_password,
    }
    r = client.post("/api/token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
