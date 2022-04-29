from app.db.models import Document, Source, Geography, DocumentType, Language
from pathlib import Path


def test_document_upload(
    client, superuser_token_headers, test_s3_client, s3_document_bucket_names
):

    test_valid_filename = (
        Path(__file__) / "../data/cclw-1618-884b7d6efcf448ff92d27f37ff22cb65.pdf"
    ).resolve()

    with open(test_valid_filename, "rb") as f:
        response = client.post(
            "/api/v1/document",
            files={"file": (test_valid_filename.name, f, "application/pdf")},
            headers=superuser_token_headers,
        )

    queue_bucket_contents = test_s3_client.client.list_objects(
        Bucket=s3_document_bucket_names["queue"],
    ).get("Contents")

    assert response.status_code == 200
    # There should be 2 documents in the mocked bucket: test_document.pdf, and the document just uploaded.
    assert len(queue_bucket_contents) == 2

    test_invalid_filename = (Path(__file__) / "../data/empty_img.png").resolve()

    with open(test_invalid_filename, "rb") as f:
        response = client.post(
            "/api/v1/document",
            files={"file": (test_invalid_filename.name, f, "application/pdf")},
            headers=superuser_token_headers,
        )

    queue_bucket_contents = test_s3_client.client.list_objects(
        Bucket=s3_document_bucket_names["queue"],
    ).get("Contents")
    assert response.status_code == 415
    # No more documents should have been uploaded to the queue bucket.
    assert len(queue_bucket_contents) == 2


def test_post_documents(client, superuser_token_headers, test_db):

    # ensure meta
    test_db.add(Source(name="may it be with you"))
    test_db.add(Geography(display_value="not my favourite subject"))
    test_db.add(DocumentType(name="just my type", description="sigh"))
    test_db.add(Language(language_code="afr"))
    test_db.commit()

    payload = {
        "document": {
            "loaded_ts": "2022-04-26T15:33:40.470413+00:00",
            "name": "Energy Sector Strategy 1387-1391 (2007/8-2012/3)",
            "source_url": "https://climate-laws.org/rails/active_storage/blobs/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBcG9IIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--be6991246abda10bef5edc0a4d196b73ce1b1a26/f",
            "url": "https://cpr-document-queue.s3.eu-west-2.amazonaws.com/AFG/2008-12-25/AFG-2008-12-25-Energy Sector Strategy 1387-1391 (2007/8-2012/3)-1.pdf",
            "type_id": 1,
            "geography_id": 1,
            "source_id": 1,
        },
        "language_ids": [1],
        "source_id": 1,
        "events": [
            {
                "name": "Publication",
                "description": "The publication date",
                "created_ts": "2008-12-25T00:00:00+00:00",
            }
        ],
        "sectors": [
            {
                "name": "Energy",
                "description": "Imported by CPR loader",
                "source_id": 1,
            }
        ],
        "instruments": [
            {
                "name": "Developing plans and strategies|Governance and planning",
                "description": "Imported by CPR loader",
                "source_id": 1,
            },
            {
                "name": "Capacity-building - general|Capacity-building",
                "description": "Imported by CPR loader",
                "source_id": 1,
            },
        ],
        "frameworks": [],
        "responses": [{"name": "Mitigation", "description": "Imported by CPR loader"}],
        "hazards": [],
    }

    response = client.post(
        "/api/v1/documents", headers=superuser_token_headers, json=payload
    )

    assert response.status_code == 200

    # for now, only the document is persisted
    doc = test_db.query(Document).first()
    assert doc.name == "Energy Sector Strategy 1387-1391 (2007/8-2012/3)"
