import datetime
from unittest.mock import patch

import pytest

from app.db.models import (
    Source,
    Geography,
    ActionType,
    Language,
    Action,
    DocumentInvalidReason,
    Document,
)


@pytest.fixture
def ensure_lookups(test_db):
    # ensure geography_id 1
    test_db.add(Geography(country_code="foo", english_shortname="foo"))
    # ensure action_type_id 1
    test_db.add(ActionType(type_name="foo"))
    # ensure source_id 1
    test_db.add(Source(name="foo"))
    # ensure language_id 1
    test_db.add(Language(language_code="foo"))

    test_db.flush()


@patch("app.api.api_v1.routers.actions.get_document_validity")
def test_post_action(
    mock_get_document_validity,
    client,
    user_token_headers,
    test_s3_client,
    s3_document_bucket_names,
    test_db,
    ensure_lookups,
):
    response = client.post(
        "/api/v1/actions",
        json={
            "action_source_id": 1,
            "name": "test action",
            "year": 2008,
            "month": 9,
            "day": 12,
            "geography_id": 1,
            "action_type_id": 1,
            "documents": [
                {
                    "name": "test document 1",
                    "language_id": 1,
                    "source_url": None,
                    "s3_url": f"https://{s3_document_bucket_names['queue']}.s3.eu-west-2.amazonaws.com/test_document.pdf",
                    "year": 2009,
                    "month": 12,
                    "day": 10,
                }
            ],
        },
        headers=user_token_headers,
    )

    queue_bucket_contents = test_s3_client.client.list_objects(
        Bucket=s3_document_bucket_names["queue"],
    ).get("Contents")

    store_bucket_contents = test_s3_client.client.list_objects(
        Bucket=s3_document_bucket_names["store"],
    ).get("Contents")

    assert response.status_code == 200
    # Queue bucket is empty as test_document.pdf has been moved.
    assert queue_bucket_contents is None
    # Store bucket contains only test_document.pdf.
    assert len(store_bucket_contents) == 1
    assert store_bucket_contents[0].get("Key") == "test_document.pdf"

    # Action table contains one action, with the name 'test action'
    assert len(test_db.query(Action).all()) == 1
    assert test_db.query(Action).all()[0].name == "test action"

    # Document table contains a document with the correct properties
    assert test_db.query(Document).all()[0].name == "test document 1"
    assert test_db.query(Document).all()[0].source_url is None
    assert test_db.query(Document).all()[0].language_id == 1
    assert (
        test_db.query(Document).all()[0].s3_url
        == f"https://{s3_document_bucket_names['store']}.s3.eu-west-2.amazonaws.com/test_document.pdf"
    )
    assert test_db.query(Document).all()[0].is_valid
    assert test_db.query(Document).all()[0].invalid_reason is None
    mock_get_document_validity.assert_not_called()


@patch("app.api.api_v1.routers.actions.get_document_validity")
def test_null_values(
    mock_get_document_validity, client, user_token_headers, test_db, ensure_lookups
):
    # API should be able to deal with missing values for month and year, for both documents and actions, and and null for `s3_url`.
    mock_get_document_validity.return_value = None

    response = client.post(
        "/api/v1/actions",
        json={
            "action_source_id": 1,
            "name": "test action",
            "year": 2008,
            "geography_id": 1,
            "action_type_id": 1,
            "documents": [
                {
                    "name": "test document 1",
                    "language_id": 1,
                    "source_url": "https://valid.com/",
                    "s3_url": None,
                    "year": 2009,
                },
            ],
        },
        headers=user_token_headers,
    )

    assert response.status_code == 200
    assert response.json() == {
        "action_id": 1,
        "action_mod_date": datetime.date.today().isoformat(),
        "action_source_id": 1,
        "name": "test action",
        "description": None,
        "action_date": "2008-01-01",
        "geography_id": 1,
        "action_type_id": 1,
        "documents": [
            {
                "action_id": 1,
                "document_date": "2009-01-01",
                "document_id": 1,
                "document_mod_date": datetime.date.today().isoformat(),
                "invalid_reason": None,
                "is_valid": True,
                "language_id": 1,
                "name": "test document 1",
                "s3_url": None,
                "source_url": "https://valid.com/",
            }
        ],
    }

    assert test_db.query(Document).all()[0].is_valid
    assert test_db.query(Document).all()[0].invalid_reason is None
    mock_get_document_validity.assert_called_once_with("https://valid.com/")


@patch("app.api.api_v1.routers.actions.get_document_validity")
def test_unsupported_mime_type(
    mock_get_document_validity, client, user_token_headers, test_db, ensure_lookups
):
    # API should return 200 but mark doc as invalid when user provides `source_url`
    # that doesn't have MIME type pdf or HTML
    mock_get_document_validity.return_value = (
        DocumentInvalidReason.unsupported_content_type
    )
    response = client.post(
        "/api/v1/actions",
        json={
            "action_source_id": 1,
            "name": "test action",
            "year": 2008,
            "geography_id": 1,
            "action_type_id": 1,
            "documents": [
                {
                    "name": "test document 1",
                    "language_id": 1,
                    "source_url": "https://invalid.com",
                    "s3_url": None,
                    "year": 2009,
                }
            ],
        },
        headers=user_token_headers,
    )

    assert response.status_code == 200
    assert response.json() == {
        "action_date": "2008-01-01",
        "action_id": 1,
        "action_mod_date": datetime.date.today().isoformat(),
        "action_source_id": 1,
        "action_type_id": 1,
        "description": None,
        "documents": [
            {
                "action_id": 1,
                "document_date": "2009-01-01",
                "document_id": 1,
                "document_mod_date": datetime.date.today().isoformat(),
                "invalid_reason": "unsupported_content_type",
                "is_valid": False,
                "language_id": 1,
                "name": "test document 1",
                "s3_url": None,
                "source_url": "https://invalid.com",
            }
        ],
        "geography_id": 1,
        "name": "test action",
    }

    assert not test_db.query(Document).all()[0].is_valid
    assert (
        test_db.query(Document).all()[0].invalid_reason
        == DocumentInvalidReason.unsupported_content_type
    )
    mock_get_document_validity.assert_called_once_with("https://invalid.com")


def test_future_action(client, user_token_headers, test_db, ensure_lookups):
    # Providing an action date in the future should raise a 422
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)

    response = client.post(
        "/api/v1/actions",
        json={
            "action_source_id": 1,
            "name": "test action",
            "year": tomorrow.year,
            "month": tomorrow.month,
            "day": tomorrow.day,
            "geography_id": 1,
            "action_type_id": 1,
            "documents": [
                {
                    "name": "test document 1",
                    "language_id": 1,
                    "source_url": "https://raw.githubusercontent.com/climatepolicyradar/navigator/dev/backend/app/api/api_v1/routers/tests/data/empty_img.png",
                    "s3_url": None,
                    "year": 2009,
                }
            ],
        },
        headers=user_token_headers,
    )

    assert response.status_code == 422


def test_duplicate_actions(client, user_token_headers, test_db, ensure_lookups):
    payload = {
        "action_source_id": 1,
        "name": "test action",
        "year": 2008,
        "month": 1,
        "day": 1,
        "geography_id": 1,
        "action_type_id": 1,
        "documents": [],
    }

    response = client.post(
        "/api/v1/actions",
        json=payload,
        headers=user_token_headers,
    )

    assert response.status_code == 200

    response = client.post(
        "/api/v1/actions",
        json=payload,
        headers=user_token_headers,
    )

    assert response.status_code == 409


@patch("app.api.api_v1.routers.actions.get_document_validity")
def test_listing_with_pagination(
    mock_get_document_validity,
    client,
    user_token_headers,
    test_db,
    ensure_lookups,
):
    mock_get_document_validity.return_value = None

    payload = {
        "action_source_id": 1,
        "name": "test action",
        "year": 2008,
        "geography_id": 1,
        "action_type_id": 1,
        "documents": [
            {
                "name": "test document 1",
                "language_id": 1,
                "source_url": "https://valid.com",
                "s3_url": None,
                "year": 2009,
            }
        ],
    }

    response = client.post(
        "/api/v1/actions",
        json=payload,
        headers=user_token_headers,
    )

    assert response.status_code == 200

    payload["name"] = "test action 2"

    response = client.post(
        "/api/v1/actions",
        json=payload,
        headers=user_token_headers,
    )

    assert response.status_code == 200

    # page 1
    response = client.get(
        "/api/v1/actions?page=1&size=1",
        json=payload,
        headers=user_token_headers,
    )

    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "action_date": "2008-01-01",
                "action_id": 1,
                "action_mod_date": datetime.date.today().isoformat(),
                "action_source_id": 1,
                "action_type_id": 1,
                "documents": [
                    {
                        "action_id": 1,
                        "document_date": "2009-01-01",
                        "document_id": 1,
                        "document_mod_date": datetime.date.today().isoformat(),
                        "is_valid": True,
                        "language_id": 1,
                        "name": "test document 1",
                        "source_url": "https://valid.com",
                    }
                ],
                "geography_id": 1,
                "name": "test action",
            }
        ],
        "page": 1,
        "size": 1,
        "total": 2,
    }

    # page 2
    response = client.get(
        "/api/v1/actions?page=2&size=1",
        json=payload,
        headers=user_token_headers,
    )

    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "action_date": "2008-01-01",
                "action_id": 2,
                "action_mod_date": datetime.date.today().isoformat(),
                "action_source_id": 1,
                "action_type_id": 1,
                "documents": [
                    {
                        "action_id": 2,
                        "document_date": "2009-01-01",
                        "document_id": 2,
                        "document_mod_date": datetime.date.today().isoformat(),
                        "is_valid": True,
                        "language_id": 1,
                        "name": "test document 1",
                        "source_url": "https://valid.com",
                    }
                ],
                "geography_id": 1,
                "name": "test action 2",
            }
        ],
        "page": 2,
        "size": 1,
        "total": 2,
    }


@patch("app.api.api_v1.routers.actions.get_document_validity")
def test_get_action(
    mock_get_document_validity,
    client,
    user_token_headers,
    test_s3_client,
    s3_document_bucket_names,
    test_db,
    ensure_lookups,
):
    mock_get_document_validity.return_value = None

    response = client.post(
        "/api/v1/actions",
        json={
            "action_source_id": 1,
            "name": "test action",
            "year": 2008,
            "month": 9,
            "day": 12,
            "geography_id": 1,
            "action_type_id": 1,
            "documents": [
                {
                    "name": "test document 1",
                    "language_id": 1,
                    "source_url": "https://valid.com/",
                    "s3_url": None,
                    "year": 2009,
                    "month": 12,
                    "day": 10,
                }
            ],
        },
        headers=user_token_headers,
    )

    assert response.status_code == 200
    action_id = response.json()["action_id"]

    # fetch action
    response = client.get(f"/api/v1/actions/{action_id}", headers=user_token_headers)
    assert response.status_code == 200
    assert response.json() == {
        "action_id": 1,
        "action_mod_date": datetime.date.today().isoformat(),
        "action_source_id": 1,
        "name": "test action",
        "action_date": "2008-09-12",
        "geography_id": 1,
        "action_type_id": 1,
        "documents": [
            {
                "action_id": 1,
                "document_date": "2009-12-10",
                "document_id": 1,
                "document_mod_date": datetime.date.today().isoformat(),
                "is_valid": True,
                "language_id": 1,
                "name": "test document 1",
                "source_url": "https://valid.com/",
            }
        ],
    }

    # verify missing action raises 404
    response = client.get("/api/v1/actions/2", headers=user_token_headers)
    assert response.status_code == 404

    # test auth required
    response = client.get(f"/api/v1/actions/{action_id}")
    assert response.status_code == 401
