from app.db.models import (
    Document,
    Source,
    Geography,
    DocumentType,
    Language,
    Sector,
    Response,
    Hazard,
    Framework,
    Instrument,
    Category,
    Keyword,
)
from app.api.api_v1.schemas.document import (
    DocumentCreateRequest,
    RelationshipCreateRequest,
)
from app.db.crud.document import (
    create_document,
    get_document_detail,
    get_postfix_map,
)


def create_4_documents(test_db):
    # ensure meta
    test_db.add(Source(name="may it be with you"))
    test_db.add(
        Geography(
            display_value="not my favourite subject",
            slug="not-my-favourite-subject",
            value="NMFS",
            type="country",
        )
    )
    test_db.add(
        Geography(
            display_value="not my fav subject again",
            slug="not-my-fav-subject-again",
            value="NMFSA",
            type="country",
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
        "publication_ts": "2000-01-01T00:00:00.000000+00:00",
        "name": "Energy Sector Strategy 1387-1391 (2007/8-2012/3)",
        "postfix": "postfix1",
        "description": "the document description",
        "source_url": "https://climate-laws.org/rails/active_storage/blobs/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBcG9IIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--be6991246abda10bef5edc0a4d196b73ce1b1a26/f",
        "type": "just my type",
        "geography": "not my favourite subject",
        "source": "may it be with you",
        "import_id": "CCLW.001.000.XXX",
        "category": "a category",
        "languages": ["Afrikaans"],
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
    document_create_request_1 = DocumentCreateRequest(**document1_payload)
    with test_db.begin_nested():
        new_document_1 = create_document(test_db, document_create_request_1)

    # This commit is necessary after completing the nested transaction
    test_db.commit()
    document1_created_content = get_document_detail(
        test_db, new_document_1.import_id
    ).dict()

    # Document 2 payload also checks that we correctly associate new documents with
    # existing metadata values.
    document2_payload = {
        "publication_ts": "1999-01-01T00:00:00.000000+00:00",
        "name": "Agriculture Sector Strategy 1487-1491 (2008/9-2013/4)",
        "postfix": "postfix2",
        "description": "the document description",
        "source_url": "https://climate-laws.org/rails/active_storage/blobs/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBcG9IIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--be6991246abda10bef5edc0a4d196b73ce1b1a26/g",
        "type": "just my type",
        "geography": "not my favourite subject",
        "source": "may it be with you",
        "import_id": "CCLW.002.000.XXX",
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
    document_create_request_2 = DocumentCreateRequest(**document2_payload)
    with test_db.begin_nested():
        new_document_2 = create_document(test_db, document_create_request_2)

    # This commit is necessary after completing the nested transaction
    test_db.commit()
    document2_created_content = get_document_detail(
        test_db, new_document_2.import_id
    ).dict()

    # Document 3 payload checks we find related documents across the master doc.
    document3_payload = {
        "publication_ts": "1998-01-01T00:00:00.000000+00:00",
        "name": "Energy Sector Strategy 1387-1391 (2009/8-2014/3)",
        "postfix": "",
        "description": "the document description",
        "source_url": "https://climate-laws.org/rails/active_storage/blobs/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBcG9IIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--be6991246abda10bef5edc0a4d196b73ce1b1a26/f",
        "type": "just my type",
        "geography": "NMFSA",
        "source": "may it be with you",
        "import_id": "CCLW.003.000.XXX",
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
    document_create_request_3 = DocumentCreateRequest(**document3_payload)
    with test_db.begin_nested():
        new_document_3 = create_document(test_db, document_create_request_3)

    # This commit is necessary after completing the nested transaction
    test_db.commit()
    document3_created_content = get_document_detail(
        test_db, new_document_3.import_id
    ).dict()

    # Document 4 payload checks we do not find unrelated docs.
    document4_payload = {
        "publication_ts": "1997-01-01T00:00:00.000000+00:00",
        "name": "Energy Sector Strategy 1387-1391 (2010/8-2015/3)",
        "postfix": None,
        "description": "the document description",
        "source_url": "https://climate-laws.org/rails/active_storage/blobs/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBcG9IIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--be6991246abda10bef5edc0a4d196b73ce1b1a26/f",
        "type": "just my type",
        "geography": "not my favourite subject",
        "source": "may it be with you",
        "import_id": "CCLW.005.000.XXX",
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
    document_create_request_4 = DocumentCreateRequest(**document4_payload)
    with test_db.begin_nested():
        new_document_4 = create_document(test_db, document_create_request_4)

    # This commit is necessary after completing the nested transaction
    test_db.commit()
    document4_created_content = get_document_detail(
        test_db, new_document_4.import_id
    ).dict()

    return (
        document1_created_content,
        document1_payload,
        document2_created_content,
        document2_payload,
        document3_created_content,
        document3_payload,
        document4_created_content,
        document4_payload,
    )


def test_document_detail(
    client,
    superuser_token_headers,
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
    ) = create_4_documents(test_db)

    # Set up doc relationships
    response_create = client.post(
        "/api/v1/document-relationships",
        headers=superuser_token_headers,
        json=RelationshipCreateRequest(
            name="Rel", type="test", description="test relationship"
        ).dict(),
    )
    assert response_create.status_code == 201
    rel_id = response_create.json()["id"]
    doc_ids = [
        response1_document["id"],
        response2_document["id"],
        response3_document["id"],
    ]

    for doc_id in doc_ids:
        response = client.put(
            f"/api/v1/document-relationships/{rel_id}/documents/{doc_id}",
            headers=superuser_token_headers,
        )
        assert response.status_code == 201

    # Test properties
    get_detail_response_2 = client.get(
        f"/api/v1/documents/{response2_document['import_id']}",
    )
    assert get_detail_response_2.status_code == 200

    # Check some expected properties of the returned document
    get_detail_json_2 = get_detail_response_2.json()
    assert (
        get_detail_json_2["name"]
        == "Agriculture Sector Strategy 1487-1491 (2008/9-2013/4)"
    )
    assert get_detail_json_2["description"] == "the document description"
    assert get_detail_json_2["postfix"] == "postfix2"
    assert get_detail_json_2["publication_ts"] == "1999-01-01T00:00:00"
    assert (
        get_detail_json_2["source_url"]
        == "https://climate-laws.org/rails/active_storage/blobs/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBcG9IIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--be6991246abda10bef5edc0a4d196b73ce1b1a26/g"
    )

    assert get_detail_json_2["source"] == {"name": "may it be with you"}
    assert get_detail_json_2["geography"] == {
        "display_value": "not my favourite subject",
        "slug": "not-my-favourite-subject",
        "value": "NMFS",
        "type": "country",
    }
    assert get_detail_json_2["type"] == {"name": "just my type", "description": "sigh"}
    assert get_detail_json_2["languages"] == [
        {
            "language_code": "afr",
            "part1_code": None,
            "part2_code": None,
            "name": "Afrikaans",
        }
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
            "import_id": "CCLW.001.000.XXX",
            "name": "Energy Sector Strategy 1387-1391 (2007/8-2012/3)",
            "postfix": "postfix1",
            "description": "the document description",
            "country_code": "NMFS",
            "country_name": "not my favourite subject",
            "publication_ts": "2000-01-01T00:00:00",
            "slug": "not-my-favourite-subject_2000_energy-sector-strategy-1387-1391-2007-8-2012-3_000_xxx",
        },
        {
            "document_id": response3_document["id"],
            "import_id": "CCLW.003.000.XXX",
            "name": "Energy Sector Strategy 1387-1391 (2009/8-2014/3)",
            "postfix": "",
            "description": "the document description",
            "country_code": "NMFSA",
            "country_name": "not my fav subject again",
            "publication_ts": "1998-01-01T00:00:00",
            "slug": "not-my-fav-subject-again_1998_energy-sector-strategy-1387-1391-2009-8-2014-3_000_xxx",
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
        f"/api/v1/documents/{response1_document['import_id']}",
    )
    assert get_detail_response_1.status_code == 200
    get_detail_json_1 = get_detail_response_1.json()

    assert set(rd["document_id"] for rd in get_detail_json_1["related_documents"]) == {
        2,
        3,
    }

    get_detail_response_3 = client.get(
        f"/api/v1/documents/{response3_document['import_id']}",
    )
    assert get_detail_response_3.status_code == 200
    get_detail_json_3 = get_detail_response_3.json()

    assert set(rd["document_id"] for rd in get_detail_json_3["related_documents"]) == {
        1,
        2,
    }

    get_detail_response_4 = client.get(
        f"/api/v1/documents/{response4_document['slug']}",
    )
    assert get_detail_response_4.status_code == 200
    get_detail_json_4 = get_detail_response_4.json()

    assert get_detail_json_4["related_documents"] == []

    # Check content types are all unknown before update endpoint is called
    assert get_detail_json_1["content_type"] == "unknown"
    assert get_detail_json_2["content_type"] == "unknown"
    assert get_detail_json_3["content_type"] == "unknown"
    assert get_detail_json_4["content_type"] == "unknown"

    document1_object = (
        test_db.query(Document).filter(Document.id == response1_document["id"]).first()
    )
    document1_object.cdn_object = "hello1.pdf"
    document1_object.url = "some_url1"

    document2_object = (
        test_db.query(Document).filter(Document.id == response2_document["id"]).first()
    )
    document2_object.url = "https://ab.s3.cde.amazonaws.com/url2.htm"

    test_db.flush()

    get_detail_response_1 = client.get(
        f"/api/v1/documents/{response1_document['import_id']}",
    )
    assert get_detail_response_1.status_code == 200
    get_detail_json_1 = get_detail_response_1.json()

    get_detail_response_2 = client.get(
        f"/api/v1/documents/{response2_document['import_id']}",
    )
    assert get_detail_response_2.status_code == 200
    get_detail_json_2 = get_detail_response_2.json()


def test_update_document_security(
    client,
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
    ) = create_4_documents(test_db)

    doc_id = response1_document["id"]
    payload = {
        "md5sum": "abc123",
        "content_type": "content_type",
        "source_url": "source_url",
    }

    response = client.put(f"/api/v1/admin/documents/{doc_id}", json=payload)

    assert response.status_code == 401


def test_update_document(
    client,
    superuser_token_headers,
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
    ) = create_4_documents(test_db)

    import_id = response1_document["import_id"]
    payload = {
        "md5_sum": "c184214e-4870-48e0-adab-3e064b1b0e76",
        "content_type": "updated/content_type",
        "cdn_object": "folder/file",
    }

    response = client.put(
        f"/api/v1/admin/documents/{import_id}",
        headers=superuser_token_headers,
        json=payload,
    )

    assert response.status_code == 200
    json_object = response.json()
    assert json_object["md5_sum"] == "c184214e-4870-48e0-adab-3e064b1b0e76"
    assert json_object["content_type"] == "updated/content_type"
    assert json_object["cdn_object"] == "folder/file"

    get_response = client.get(
        f"/api/v1/documents/{import_id}",
    )

    assert get_response.status_code == 200
    json_object = get_response.json()
    assert json_object["content_type"] == "updated/content_type"
    assert "folder/file" in json_object["url"]


def test_update_document_with_import_id(
    client,
    superuser_token_headers,
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
    ) = create_4_documents(test_db)

    import_id = response1_document["import_id"]
    payload = {
        "md5_sum": "c184214e-4870-48e0-adab-3e064b1b0e76",
        "content_type": "updated/content_type",
        "cdn_object": "folder/file",
    }

    update_response = client.put(
        f"/api/v1/admin/documents/{import_id}",
        headers=superuser_token_headers,
        json=payload,
    )

    assert update_response.status_code == 200
    json_object = update_response.json()
    assert json_object["import_id"] == import_id
    assert json_object["md5_sum"] == "c184214e-4870-48e0-adab-3e064b1b0e76"
    assert json_object["content_type"] == "updated/content_type"

    get_response = client.get(
        f"/api/v1/documents/{import_id}",
    )

    assert get_response.status_code == 200
    json_object = get_response.json()
    assert json_object["import_id"] == import_id
    assert json_object["content_type"] == "updated/content_type"
    assert "folder/file" in json_object["url"]


def test_postfix_map(
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
    ) = create_4_documents(test_db)

    pf_map = get_postfix_map(
        test_db,
        [
            response1_document["import_id"],
            response2_document["import_id"],
            response3_document["import_id"],
            response4_document["import_id"],
        ],
    )

    assert len(pf_map) == 4
    assert pf_map[response1_document["import_id"]] == "postfix1"
    assert pf_map[response2_document["import_id"]] == "postfix2"
    assert pf_map[response3_document["import_id"]] == ""
    assert pf_map[response4_document["import_id"]] == ""
