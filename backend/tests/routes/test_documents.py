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
from app.api.api_v1.schemas.document import DocumentAssociationCreateRequest


def create_4_documents(test_db, client, superuser_token_headers):
    # ensure meta
    test_db.add(Source(name="may it be with you"))
    test_db.add(
        Geography(
            display_value="not my favourite subject", value="NMFS", type="country"
        )
    )
    test_db.add(
        Geography(
            display_value="not my fav subject again", value="NMFSA", type="country"
        )
    )
    test_db.add(DocumentType(name="just my type", description="sigh"))
    test_db.add(Language(language_code="afr", name="Afrikaans"))
    test_db.add(Category(name="a category", description="a category description"))
    test_db.add(Keyword(name="some keyword", description="Imported by CPR loader"))
    test_db.add(
        Keyword(name="some other keyword", description="Imported by CPR loader")
    )
    test_db.add(Hazard(name="some hazard", description="Imported by CPR loader"))
    test_db.add(
        Hazard(name="some other hazard 1", description="Imported by CPR loader")
    )
    test_db.add(
        Hazard(name="some other hazard 2", description="Imported by CPR loader")
    )
    test_db.add(Response(name="Mitigation", description="Imported by CPR loader"))
    test_db.add(Framework(name="some framework", description="Imported by CPR loader"))
    test_db.add(
        Framework(name="some other framework 1", description="Imported by CPR loader")
    )
    test_db.add(
        Framework(name="some other framework 2", description="Imported by CPR loader")
    )
    test_db.commit()

    test_db.add(
        Instrument(
            name="some instrument", description="Imported by CPR loader", source_id=1
        )
    )
    test_db.add(
        Instrument(
            name="some other instrument",
            description="Imported by CPR loader",
            source_id=1,
        )
    )
    test_db.add(
        Instrument(
            name="another instrument", description="Imported by CPR loader", source_id=1
        )
    )
    test_db.add(
        Instrument(
            name="another other instrument",
            description="Imported by CPR loader",
            source_id=1,
        )
    )
    test_db.add(
        Sector(name="Energy", description="Imported by CPR loader", source_id=1)
    )
    test_db.add(
        Sector(name="Agriculture", description="Imported by CPR loader", source_id=1)
    )
    test_db.commit()

    document1_payload = {
        "loaded_ts": "2022-04-26T15:33:40.470413+00:00",
        "publication_ts": "2000-01-01T00:00:00.000000+00:00",
        "name": "Energy Sector Strategy 1387-1391 (2007/8-2012/3)",
        "description": "the document description",
        "source_url": "https://climate-laws.org/rails/active_storage/blobs/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBcG9IIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--be6991246abda10bef5edc0a4d196b73ce1b1a26/f",
        "url": "https://cpr-document-queue.s3.eu-west-2.amazonaws.com/AFG/2008-12-25/AFG-2008-12-25-Energy Sector Strategy 1387-1391 (2007/8-2012/3)-1.pdf",
        "md5_sum": "the md5 sum",
        "type": "just my type",
        "geography": "not my favourite subject",
        "source": "may it be with you",
        "category": "a category",
        "languages": ["afr"],
        "events": [
            {
                "name": "Publication",
                "description": "The publication date",
                "created_ts": "2008-12-25T00:00:00+00:00",
            }
        ],
        "sectors": ["Energy"],
        "instruments": ["some instrument", "another instrument"],
        "frameworks": ["some framework"],
        "topics": ["Mitigation"],
        "hazards": ["some hazard"],
        "keywords": ["some keyword"],
    }
    response1 = client.post(
        "/api/v1/documents", headers=superuser_token_headers, json=document1_payload
    )
    assert response1.status_code == 200
    response1_document = response1.json()

    # Document 2 payload also checks that we correctly associate new documents with
    # existing metadata values.
    document2_payload = {
        "loaded_ts": "2022-04-26T15:34:40.470413+00:00",
        "publication_ts": "1999-01-01T00:00:00.000000+00:00",
        "name": "Agriculture Sector Strategy 1487-1491 (2008/9-2013/4)",
        "description": "the document description",
        "source_url": "https://climate-laws.org/rails/active_storage/blobs/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBcG9IIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--be6991246abda10bef5edc0a4d196b73ce1b1a26/g",
        "url": "https://juan-test-bucket.s3.eu-west-2.amazonaws.com/AFG/2009-10-12/AFG-2009-10-12-Agriculture Sector+Strategy 1487-1491 (2008/9-2013/4)-1.html",
        "md5_sum": "the other md5 sum",
        "type": "just my type",
        "geography": "not my favourite subject",
        "source": "may it be with you",
        "category": "a category",
        "languages": ["afr"],
        "events": [
            {
                "name": "Publication",
                "description": "The publication date",
                "created_ts": "2009-10-12T00:00:00+00:00",
            }
        ],
        "sectors": ["Energy", "Agriculture"],
        "instruments": [
            "some instrument",
            "some other instrument",
            "another other instrument",
        ],
        "frameworks": [
            "some framework",
            "some other framework 1",
            "some other framework 2",
        ],
        "topics": ["Mitigation"],
        "hazards": ["some hazard", "some other hazard 1", "some other hazard 2"],
        "keywords": ["some keyword", "some other keyword"],
    }
    response2 = client.post(
        "/api/v1/documents", headers=superuser_token_headers, json=document2_payload
    )
    assert response2.status_code == 200
    response2_document = response2.json()

    # Document 3 payload checks we find related documents across the master doc.
    document3_payload = {
        "loaded_ts": "2022-04-26T15:35:40.470413+00:00",
        "publication_ts": "1998-01-01T00:00:00.000000+00:00",
        "name": "Energy Sector Strategy 1387-1391 (2009/8-2014/3)",
        "description": "the document description",
        "source_url": "https://climate-laws.org/rails/active_storage/blobs/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBcG9IIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--be6991246abda10bef5edc0a4d196b73ce1b1a26/f",
        "url": "https://cpr-document-queue.s3.eu-west-2.amazonaws.com/AFG/2008-12-25/AFG-2010-12-25-Energy Sector Strategy 1387-1391 (2009/8-2014/3)-1.docx",
        "md5_sum": "the md5 sum",
        "type": "just my type",
        "geography": "not my fav subject again",
        "source": "may it be with you",
        "category": "a category",
        "languages": ["afr"],
        "events": [
            {
                "name": "Publication",
                "description": "The publication date",
                "created_ts": "2010-12-25T00:00:00+00:00",
            }
        ],
        "sectors": ["Energy"],
        "instruments": ["some instrument", "another instrument"],
        "frameworks": ["some framework"],
        "topics": ["Mitigation"],
        "hazards": ["some hazard"],
        "keywords": ["some keyword"],
    }
    response3 = client.post(
        "/api/v1/documents", headers=superuser_token_headers, json=document3_payload
    )
    assert response3.status_code == 200
    response3_document = response3.json()

    # Document 4 payload checks we do not find unrelated docs.
    document4_payload = {
        "loaded_ts": "2022-04-26T15:36:40.470413+00:00",
        "publication_ts": "1997-01-01T00:00:00.000000+00:00",
        "name": "Energy Sector Strategy 1387-1391 (2010/8-2015/3)",
        "description": "the document description",
        "source_url": "https://climate-laws.org/rails/active_storage/blobs/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBcG9IIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--be6991246abda10bef5edc0a4d196b73ce1b1a26/f",
        "url": "https://cpr-document-queue.s3.eu-west-2.amazonaws.com/AFG/2008-12-25/AFG-2012-12-25-Energy Sector Strategy 1387-1391 (2010/8-2015/3)-1.arrrr",
        "md5_sum": "the md5 sum",
        "type": "just my type",
        "geography": "not my favourite subject",
        "source": "may it be with you",
        "category": "a category",
        "languages": ["afr"],
        "events": [
            {
                "name": "Publication",
                "description": "The publication date",
                "created_ts": "2012-12-25T00:00:00+00:00",
            }
        ],
        "sectors": ["Energy"],
        "instruments": ["some instrument", "another instrument"],
        "frameworks": ["some framework"],
        "topics": ["Mitigation"],
        "hazards": ["some hazard"],
        "keywords": ["some keyword"],
    }
    response4 = client.post(
        "/api/v1/documents", headers=superuser_token_headers, json=document4_payload
    )
    assert response4.status_code == 200
    response4_document = response4.json()
    return (
        response1_document,
        document1_payload,
        response2_document,
        document2_payload,
        response3_document,
        document3_payload,
        response4_document,
        document4_payload,
    )


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
    test_db.add(
        Geography(
            display_value="not my favourite subject", value="NMFS", type="country"
        )
    )
    test_db.add(DocumentType(name="just my type", description="sigh"))
    test_db.add(Language(language_code="afr", name="Afrikaans"))
    test_db.add(Category(name="a category", description="a category description"))
    test_db.add(Hazard(name="some hazard", description="Imported by CPR loader"))
    test_db.add(Response(name="Mitigation", description="Imported by CPR loader"))
    test_db.add(Framework(name="some framework", description="Imported by CPR loader"))
    test_db.add(Keyword(name="some keyword", description="Imported by CPR loader"))
    test_db.commit()

    test_db.add(
        Sector(name="Energy", description="Imported by CPR loader", source_id=1)
    )
    test_db.add(
        Instrument(
            name="some instrument", description="Imported by CPR loader", source_id=1
        )
    )
    test_db.add(
        Instrument(
            name="another instrument", description="Imported by CPR loader", source_id=1
        )
    )
    test_db.commit()

    payload = {
        "loaded_ts": "2022-04-26T15:33:40.470413+00:00",
        "publication_ts": "2000-01-01T00:00:00.000000+00:00",
        "name": "Energy Sector Strategy 1387-1391 (2007/8-2012/3)",
        "description": "the document description",
        "source_url": "https://climate-laws.org/rails/active_storage/blobs/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBcG9IIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--be6991246abda10bef5edc0a4d196b73ce1b1a26/f",
        "url": "https://cpr-document-queue.s3.eu-west-2.amazonaws.com/AFG/2008-12-25/AFG-2008-12-25-Energy Sector Strategy 1387-1391 (2007/8-2012/3)-1.pdf",
        "md5_sum": "the md5 sum",
        "type": "just my type",
        "geography": "not my favourite subject",
        "source": "may it be with you",
        "category": "a category",
        "languages": ["afr"],
        "events": [
            {
                "name": "Publication",
                "description": "The publication date",
                "created_ts": "2008-12-25T00:00:00+00:00",
            }
        ],
        "sectors": ["Energy"],
        "instruments": ["some instrument", "another instrument"],
        "frameworks": ["some framework"],
        "topics": ["Mitigation"],
        "hazards": ["some hazard"],
        "keywords": ["some keyword"],
    }

    response = client.post(
        "/api/v1/documents", headers=superuser_token_headers, json=payload
    )

    assert response.status_code == 200

    doc: Document = test_db.query(Document).first()
    assert doc.name == payload["name"]
    assert doc.description == payload["description"]
    assert doc.url == payload["url"]
    assert doc.md5_sum == payload["md5_sum"]
    assert doc.publication_ts == datetime(2000, 1, 1)

    event = test_db.query(Event).first()
    assert event.name == "Publication"
    assert event.created_ts == datetime(2008, 12, 25, 0, 0, tzinfo=timezone.utc)
    assert test_db.query(DocumentLanguage).first().document_id == 1


def test_post_documents_fail(client, superuser_token_headers, test_db):
    """Document creation should fail unless all referenced metadata already exists."""

    # ensure meta
    test_db.add(Source(name="may it be with you"))
    test_db.add(
        Geography(
            display_value="not my favourite subject", value="NMFS", type="country"
        )
    )
    test_db.add(DocumentType(name="just my type", description="sigh"))
    test_db.add(Language(language_code="afr", name="Afrikaans"))
    test_db.add(Category(name="a category", description="a category description"))
    test_db.add(Hazard(name="some other hazard", description="Imported by CPR loader"))
    test_db.add(Response(name="Mitigation", description="Imported by CPR loader"))
    test_db.add(
        Framework(name="some other framework", description="Imported by CPR loader")
    )
    test_db.add(Keyword(name="some keyword", description="Imported by CPR loader"))
    test_db.commit()

    test_db.add(
        Sector(name="Energy", description="Imported by CPR loader", source_id=1)
    )
    test_db.add(
        Instrument(
            name="some instrument", description="Imported by CPR loader", source_id=1
        )
    )
    test_db.add(
        Instrument(
            name="another instrument", description="Imported by CPR loader", source_id=1
        )
    )
    test_db.commit()

    payload = {
        "loaded_ts": "2022-04-26T15:33:40.470413+00:00",
        "publication_ts": "2000-01-01T00:00:00.000000+00:00",
        "name": "Energy Sector Strategy 1387-1391 (2007/8-2012/3)",
        "description": "the document description",
        "source_url": "https://climate-laws.org/rails/active_storage/blobs/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBcG9IIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--be6991246abda10bef5edc0a4d196b73ce1b1a26/f",
        "url": "https://cpr-document-queue.s3.eu-west-2.amazonaws.com/AFG/2008-12-25/AFG-2008-12-25-Energy Sector Strategy 1387-1391 (2007/8-2012/3)-1.pdf",
        "md5_sum": "the md5 sum",
        "type": "just my type",
        "geography": "not my favourite subject",
        "source": "may it be with you",
        "category": "a category",
        "languages": ["afr"],
        "events": [
            {
                "name": "Publication",
                "description": "The publication date",
                "created_ts": "2008-12-25T00:00:00+00:00",
            }
        ],
        "sectors": ["Energy"],
        "instruments": ["some instrument", "another instrument"],
        "frameworks": ["some framework"],
        "topics": ["Mitigation"],
        "hazards": ["some hazard"],
        "keywords": ["some keyword"],
    }

    response = client.post(
        "/api/v1/documents", headers=superuser_token_headers, json=payload
    )

    assert response.status_code == 422
    assert len(list(test_db.query(Document).all())) == 0
    assert test_db.query(Event).first() is None


def test_document_detail(
    client,
    superuser_token_headers,
    user_token_headers,
    test_db,
):

    (
        response1_document,
        document1_payload,
        response2_document,
        document2_payload,
        response3_document,
        document3_payload,
        response4_document,
        document4_payload,
    ) = create_4_documents(test_db, client, superuser_token_headers)

    # Set up associations
    doc_association_payload_1 = DocumentAssociationCreateRequest(
        document_id_from=response2_document["id"],
        document_id_to=response1_document["id"],
        name="related",
        type="related",
    ).dict()
    response_assoc_1 = client.post(
        "/api/v1/associations",
        headers=superuser_token_headers,
        json=doc_association_payload_1,
    )
    assert response_assoc_1.status_code == 200

    doc_association_payload_2 = DocumentAssociationCreateRequest(
        document_id_from=response3_document["id"],
        document_id_to=response1_document["id"],
        name="related",
        type="related",
    ).dict()
    response_assoc_2 = client.post(
        "/api/v1/associations",
        headers=superuser_token_headers,
        json=doc_association_payload_2,
    )
    assert response_assoc_2.status_code == 200

    # Test properties
    get_detail_response_2 = client.get(
        f"/api/v1/documents/{response2_document['id']}",
        headers=user_token_headers,
    )
    assert get_detail_response_2.status_code == 200

    # Check some expected properties of the returned document
    get_detail_json_2 = get_detail_response_2.json()
    assert (
        get_detail_json_2["name"]
        == "Agriculture Sector Strategy 1487-1491 (2008/9-2013/4)"
    )
    assert get_detail_json_2["description"] == "the document description"
    assert get_detail_json_2["publication_ts"] == "1999-01-01T00:00:00"
    assert (
        get_detail_json_2["source_url"]
        == "https://climate-laws.org/rails/active_storage/blobs/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBcG9IIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--be6991246abda10bef5edc0a4d196b73ce1b1a26/g"
    )
    assert (
        get_detail_json_2["url"]
        == "https://cdn.climatepolicyradar.org/AFG/2009-10-12/AFG-2009-10-12-Agriculture+Sector%2BStrategy+1487-1491+%282008/9-2013/4%29-1.html"
    )
    assert get_detail_json_2["source"] == {"name": "may it be with you"}
    assert get_detail_json_2["geography"] == {
        "display_value": "not my favourite subject",
        "value": "NMFS",
        "type": "country",
    }
    assert get_detail_json_2["type"] == {"name": "just my type", "description": "sigh"}
    assert get_detail_json_2["languages"] == [
        {"language_code": "afr", "name": "Afrikaans"}
    ]
    assert get_detail_json_2["category"] == {
        "name": "a category",
        "description": "a category description",
    }

    sorted_related_docs = sorted(
        get_detail_json_2["related_documents"],
        key=lambda d: d["document_id"],
    )
    assert sorted_related_docs == [
        {
            "document_id": response1_document["id"],
            "name": "Energy Sector Strategy 1387-1391 (2007/8-2012/3)",
            "description": "the document description",
            "country_code": "NMFS",
            "country_name": "not my favourite subject",
            "publication_ts": "2000-01-01T00:00:00",
        },
        {
            "document_id": response3_document["id"],
            "name": "Energy Sector Strategy 1387-1391 (2009/8-2014/3)",
            "description": "the document description",
            "country_code": "NMFSA",
            "country_name": "not my fav subject again",
            "publication_ts": "1998-01-01T00:00:00",
        },
    ]

    assert get_detail_json_2["events"] == document2_payload["events"]
    assert get_detail_json_2["sectors"] == [
        {
            "name": s,
            "description": "Imported by CPR loader",
            "source": {"name": "may it be with you"},
        }
        for s in document2_payload["sectors"]
    ]
    assert get_detail_json_2["instruments"] == [
        {
            "name": i,
            "description": "Imported by CPR loader",
            "source": {"name": "may it be with you"},
        }
        for i in document2_payload["instruments"]
    ]
    assert get_detail_json_2["frameworks"] == [
        {
            "name": f,
            "description": "Imported by CPR loader",
        }
        for f in document2_payload["frameworks"]
    ]
    assert get_detail_json_2["topics"] == [
        {
            "name": t,
            "description": "Imported by CPR loader",
        }
        for t in document2_payload["topics"]
    ]
    assert get_detail_json_2["hazards"] == [
        {
            "name": h,
            "description": "Imported by CPR loader",
        }
        for h in document2_payload["hazards"]
    ]
    assert get_detail_json_2["keywords"] == [
        {
            "name": k,
            "description": "Imported by CPR loader",
        }
        for k in document2_payload["keywords"]
    ]

    # Test associations
    get_detail_response_1 = client.get(
        f"/api/v1/documents/{response1_document['id']}",
        headers=user_token_headers,
    )
    assert get_detail_response_1.status_code == 200
    get_detail_json_1 = get_detail_response_1.json()

    assert set(rd["document_id"] for rd in get_detail_json_1["related_documents"]) == {
        2,
        3,
    }

    get_detail_response_3 = client.get(
        f"/api/v1/documents/{response3_document['id']}",
        headers=user_token_headers,
    )
    assert get_detail_response_3.status_code == 200
    get_detail_json_3 = get_detail_response_3.json()

    assert set(rd["document_id"] for rd in get_detail_json_3["related_documents"]) == {
        1,
        2,
    }

    get_detail_response_4 = client.get(
        f"/api/v1/documents/{response4_document['id']}",
        headers=user_token_headers,
    )
    assert get_detail_response_4.status_code == 200
    get_detail_json_4 = get_detail_response_4.json()

    assert get_detail_json_4["related_documents"] == []

    # Check content types
    assert get_detail_json_1["content_type"] == "application/pdf"
    assert get_detail_json_2["content_type"] == "text/html"
    assert (
        get_detail_json_3["content_type"]
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    assert get_detail_json_4["content_type"] == "unknown"
