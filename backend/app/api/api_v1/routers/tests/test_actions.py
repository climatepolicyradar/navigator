from app.db import models
import datetime


def test_post_action(
    client, user_token_headers, test_s3_client, s3_document_bucket_names, test_db
):

    # ensure geography_id 1
    test_db.add(models.Geography(country_code='foo', english_shortname='foo'))
    # ensure action_type_id 1
    test_db.add(models.ActionType(type_name='foo'))
    # ensure source_id 1
    test_db.add(models.Source(name='foo'))
    # ensure language_id 1
    test_db.add(models.Language(language_code='foo'))

    test_db.flush()

    response = client.post(
        "/api/v1/action",
        json={
            "source_id": 1,
            "name": "test action",
            "year": 2008,
            "month": 9,
            "day": 12,
            "geography_id": 1,
            "type_id": 1,
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
    assert len(test_db.query(models.Action).all()) == 1
    assert test_db.query(models.Action).all()[0].name == "test action"

    # Document table contains a document with the correct properties
    assert test_db.query(models.Document).all()[0].name == "test document 1"
    assert test_db.query(models.Document).all()[0].source_url is None
    assert test_db.query(models.Document).all()[0].language_id == 1
    assert (
        test_db.query(models.Document).all()[0].s3_url
        == f"https://{s3_document_bucket_names['store']}.s3.eu-west-2.amazonaws.com/test_document.pdf"
    )

    # API should be able to take null values for month and year, for both documents and actions, and for `s3_url`.
    response = client.post(
        "/api/v1/action",
        json={
            "source_id": 1,
            "name": "test action",
            "year": 2008,
            "month": None,
            "day": None,
            "geography_id": 1,
            "type_id": 1,
            "documents": [
                {
                    "name": "test document 1",
                    "language_id": 1,
                    "source_url": "https://google.co.uk/",
                    "s3_url": None,
                    "year": 2009,
                    "month": None,
                    "day": None,
                }
            ],
        },
        headers=user_token_headers,
    )

    assert response.status_code == 200
    assert response.json() == {
        "source_id": 1,
        "name": "test action",
        "description": None,
        "year": 2008,
        "month": 1,
        "day": 1,
        "geography_id": 1,
        "type_id": 1,
        "documents": [
            {
                "name": "test document 1",
                "language_id": 1,
                "source_url": "https://google.co.uk/",
                "s3_url": None,
                "year": 2009,
                "month": 1,
                "day": 1,
            }
        ],
    }

    # API should return 400 when user provides `source_url` that doesn't have MIME type pdf or HTML
    response = client.post(
        "/api/v1/action",
        json={
            "source_id": 1,
            "name": "test action",
            "year": 2008,
            "month": None,
            "day": None,
            "geography_id": 1,
            "type_id": 1,
            "documents": [
                {
                    "name": "test document 1",
                    "language_id": 1,
                    "source_url": "https://raw.githubusercontent.com/climatepolicyradar/navigator/dev/backend/app/api/api_v1/routers/tests/data/empty_img.png",
                    "s3_url": None,
                    "year": 2009,
                    "month": None,
                    "day": None,
                }
            ],
        },
        headers=user_token_headers,
    )

    assert response.status_code == 400

    # Providing an action date in the future should raise a 400
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)

    response = client.post(
        "/api/v1/action",
        json={
            "source_id": 1,
            "name": "test action",
            "year": tomorrow.year,
            "month": tomorrow.month,
            "day": tomorrow.day,
            "geography_id": 1,
            "type_id": 1,
            "documents": [
                {
                    "name": "test document 1",
                    "language_id": 1,
                    "source_url": "https://raw.githubusercontent.com/climatepolicyradar/navigator/dev/backend/app/api/api_v1/routers/tests/data/empty_img.png",
                    "s3_url": None,
                    "year": 2009,
                    "month": None,
                    "day": None,
                }
            ],
        },
        headers=user_token_headers,
    )

    assert response.status_code == 400
