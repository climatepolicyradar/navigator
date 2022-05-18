from datetime import datetime, timezone
from pathlib import Path

from app.db.models import (
    Document,
    Source,
    Geography,
    DocumentType,
    Language,
    Event,
    Sector,
    Response,
    Hazard,
    Framework,
    Instrument,
    DocumentLanguage,
    Category,
    Keyword,
)
from app.db.schemas.document import DocumentAssociation


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
    test_db.add(Category(name="a category", description="a category description"))
    test_db.commit()

    payload = {
        "document": {
            "loaded_ts": "2022-04-26T15:33:40.470413+00:00",
            "publication_ts": "2000-01-01T00:00:00.000000+00:00",
            "name": "Energy Sector Strategy 1387-1391 (2007/8-2012/3)",
            "description": "the document description",
            "source_url": "https://climate-laws.org/rails/active_storage/blobs/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBcG9IIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--be6991246abda10bef5edc0a4d196b73ce1b1a26/f",
            "url": "https://cpr-document-queue.s3.eu-west-2.amazonaws.com/AFG/2008-12-25/AFG-2008-12-25-Energy Sector Strategy 1387-1391 (2007/8-2012/3)-1.pdf",
            "md5_sum": "the md5 sum",
            "type_id": 1,
            "geography_id": 1,
            "source_id": 1,
            "category_id": 1,
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
                "name": "some instrument",
                "description": "Imported by CPR loader",
                "source_id": 1,
            },
            {
                "name": "another instrument",
                "description": "Imported by CPR loader",
                "source_id": 1,
            },
        ],
        "frameworks": [
            {"name": "some framework", "description": "Imported by CPR loader"}
        ],
        "responses": [{"name": "Mitigation", "description": "Imported by CPR loader"}],
        "hazards": [{"name": "some hazard", "description": "Imported by CPR loader"}],
        "keywords": [{"name": "some keyword", "description": "Imported by CPR loader"}],
    }

    response = client.post(
        "/api/v1/documents", headers=superuser_token_headers, json=payload
    )

    assert response.status_code == 200

    doc: Document = test_db.query(Document).first()
    assert doc.name == payload["document"]["name"]
    assert doc.description == payload["document"]["description"]
    assert doc.url == payload["document"]["url"]
    assert doc.md5_sum == payload["document"]["md5_sum"]
    assert doc.publication_ts == datetime(2000, 1, 1)

    event = test_db.query(Event).first()
    assert event.name == "Publication"
    assert event.created_ts == datetime(2008, 12, 25, 0, 0, tzinfo=timezone.utc)
    assert test_db.query(Sector).first().name == "Energy"
    assert test_db.query(Response).first().name == "Mitigation"
    assert test_db.query(Hazard).first().name == "some hazard"
    assert test_db.query(Framework).first().name == "some framework"
    assert test_db.query(Keyword).first().name == "some keyword"
    instruments = test_db.query(Instrument).all()
    assert instruments[0].name == "some instrument"
    assert instruments[1].name == "another instrument"
    assert test_db.query(DocumentLanguage).first().document_id == 1


def test_document_detail(
    client,
    superuser_token_headers,
    user_token_headers,
    test_db,
):
    # ensure meta
    test_db.add(Source(name="may it be with you"))
    test_db.add(
        Geography(
            display_value="not my favourite subject", value="NMFS", type="country"
        )
    )
    test_db.add(DocumentType(name="just my type", description="sigh"))
    test_db.add(Language(language_code="afr", name="AFRAFR"))
    test_db.add(Category(name="a category", description="a category description"))
    test_db.commit()

    document1_payload = {
        "document": {
            "loaded_ts": "2022-04-26T15:33:40.470413+00:00",
            "publication_ts": "2000-01-01T00:00:00.000000+00:00",
            "name": "Energy Sector Strategy 1387-1391 (2007/8-2012/3)",
            "description": "the document description",
            "source_url": "https://climate-laws.org/rails/active_storage/blobs/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBcG9IIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--be6991246abda10bef5edc0a4d196b73ce1b1a26/f",
            "url": "https://cpr-document-queue.s3.eu-west-2.amazonaws.com/AFG/2008-12-25/AFG-2008-12-25-Energy Sector Strategy 1387-1391 (2007/8-2012/3)-1.pdf",
            "md5_sum": "the md5 sum",
            "type_id": 1,
            "geography_id": 1,
            "source_id": 1,
            "category_id": 1,
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
                "name": "some instrument",
                "description": "Imported by CPR loader",
                "source_id": 1,
            },
            {
                "name": "another instrument",
                "description": "Imported by CPR loader",
                "source_id": 1,
            },
        ],
        "frameworks": [
            {"name": "some framework", "description": "Imported by CPR loader"}
        ],
        "responses": [{"name": "Mitigation", "description": "Imported by CPR loader"}],
        "hazards": [{"name": "some hazard", "description": "Imported by CPR loader"}],
        "keywords": [{"name": "some keyword", "description": "Imported by CPR loader"}],
    }
    response1 = client.post(
        "/api/v1/documents", headers=superuser_token_headers, json=document1_payload
    )
    assert response1.status_code == 200
    response1_document = response1.json()

    # Document 2 payload also checks that we correctly associate new documents with
    # existing metadata values.
    document2_payload = {
        "document": {
            "loaded_ts": "2022-04-26T15:34:40.470413+00:00",
            "publication_ts": "1999-01-01T00:00:00.000000+00:00",
            "name": "Agriculture Sector Strategy 1487-1491 (2008/9-2013/4)",
            "description": "the document description",
            "source_url": "https://climate-laws.org/rails/active_storage/blobs/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBcG9IIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--be6991246abda10bef5edc0a4d196b73ce1b1a26/g",
            "url": "https://juan-test-bucket.s3.eu-west-2.amazonaws.com/AFG/2009-10-12/AFG-2009-10-12-Agriculture Sector Strategy 1487-1491 (2008/9-2013/4)-1.pdf",
            "md5_sum": "the other md5 sum",
            "type_id": 1,
            "geography_id": 1,
            "source_id": 1,
            "category_id": 1,
        },
        "language_ids": [1],
        "source_id": 1,
        "events": [
            {
                "name": "Publication",
                "description": "The publication date",
                "created_ts": "2009-10-12T00:00:00+00:00",
            }
        ],
        "sectors": [
            {
                "name": "Energy",
                "description": "Imported by CPR loader",
                "source_id": 1,
            },
            {
                "name": "Agriculture",
                "description": "Imported by CPR loader",
                "source_id": 1,
            },
        ],
        "instruments": [
            {
                "name": "some instrument",
                "description": "Imported by CPR loader",
                "source_id": 1,
            },
            {
                "name": "some other instrument",
                "description": "Imported by CPR loader",
                "source_id": 1,
            },
            {
                "name": "another other instrument",
                "description": "Imported by CPR loader",
                "source_id": 1,
            },
        ],
        "frameworks": [
            {"name": "some framework", "description": "Imported by CPR loader"},
            {"name": "some other framework 1", "description": "Imported by CPR loader"},
            {"name": "some other framework 2", "description": "Imported by CPR loader"},
        ],
        "responses": [{"name": "Mitigation", "description": "Imported by CPR loader"}],
        "hazards": [
            {"name": "some hazard", "description": "Imported by CPR loader"},
            {"name": "some other hazard1", "description": "Imported by CPR loader"},
            {"name": "some other hazard2", "description": "Imported by CPR loader"},
        ],
        "keywords": [
            {"name": "some keyword", "description": "Imported by CPR loader"},
            {"name": "some other keyword", "description": "Imported by CPR loader"},
        ],
    }
    response2 = client.post(
        "/api/v1/documents", headers=superuser_token_headers, json=document2_payload
    )
    assert response2.status_code == 200
    response2_document = response2.json()

    doc_association_payload = DocumentAssociation(
        document_id_from=response2_document["id"],
        document_id_to=response1_document["id"],
        name="related",
        type="related",
    ).dict()

    response_assoc = client.post(
        "/api/v1/associations",
        headers=superuser_token_headers,
        json=doc_association_payload,
    )
    assert response_assoc.status_code == 200

    get_detail_response = client.get(
        f"/api/v1/documents/{response2_document['id']}",
        headers=user_token_headers,
    )
    assert get_detail_response.status_code == 200

    # Check some expected properties of the returned document
    get_detail_json = get_detail_response.json()
    assert (
        get_detail_json["name"]
        == "Agriculture Sector Strategy 1487-1491 (2008/9-2013/4)"
    )
    assert get_detail_json["description"] == "the document description"
    assert get_detail_json["publication_ts"] == "1999-01-01T00:00:00"
    assert (
        get_detail_json["source_url"]
        == "https://climate-laws.org/rails/active_storage/blobs/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBcG9IIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--be6991246abda10bef5edc0a4d196b73ce1b1a26/g"
    )
    assert (
        get_detail_json["url"]
        == "https://cdn.climatepolicyradar.org/AFG/2009-10-12/AFG-2009-10-12-Agriculture Sector Strategy 1487-1491 (2008/9-2013/4)-1.pdf"
    )
    assert get_detail_json["source"] == {"name": "may it be with you"}
    assert get_detail_json["geography"] == {
        "display_value": "not my favourite subject",
        "value": "NMFS",
        "type": "country",
    }
    assert get_detail_json["type"] == {"name": "just my type", "description": "sigh"}
    assert get_detail_json["languages"] == [{"language_code": "afr", "name": "AFRAFR"}]
    assert get_detail_json["category"] == {
        "name": "a category",
        "description": "a category description",
    }
    assert get_detail_json["related_documents"] == [
        {
            "related_id": response1_document["id"],
            "name": "Energy Sector Strategy 1387-1391 (2007/8-2012/3)",
            "description": "the document description",
            "country_code": "NMFS",
            "country_name": "not my favourite subject",
            "publication_ts": "2000-01-01T00:00:00",
        },
    ]
    assert get_detail_json["events"] == document2_payload["events"]
    assert get_detail_json["sectors"] == [
        {
            "name": s["name"],
            "description": s["description"],
            "source": {"name": "may it be with you"},
        }
        for s in document2_payload["sectors"]
    ]
    assert get_detail_json["instruments"] == [
        {
            "name": i["name"],
            "description": i["description"],
            "source": {"name": "may it be with you"},
        }
        for i in document2_payload["instruments"]
    ]
    assert get_detail_json["frameworks"] == document2_payload["frameworks"]
    assert get_detail_json["topics"] == document2_payload["responses"]
    assert get_detail_json["hazards"] == document2_payload["hazards"]
    assert get_detail_json["keywords"] == document2_payload["keywords"]
