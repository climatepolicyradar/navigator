from app.api.api_v1.schemas.document import RelationshipCreateRequest
from app.db.models.document import Document, DocumentRelationship

from .test_documents import create_4_documents


def _create_10_relationships(client, superuser_token_headers):
    rel_ids = []
    for x in range(10):
        response_rel = client.post(
            "/api/v1/document-relationship",
            headers=superuser_token_headers,
            json=RelationshipCreateRequest(
                name=f"Rel{x}", type="test", description=f"test relationship {x}"
            ).dict(),
        )
        assert response_rel.status_code == 201
        rel_ids.append(response_rel.json()["id"])
    return rel_ids


# --- tests for POST /api/v1/document-relationship


def test_create_relationship(
    client,
    superuser_token_headers,
):
    response_create = client.post(
        "/api/v1/document-relationship",
        headers=superuser_token_headers,
        json=RelationshipCreateRequest(
            name="Rel", type="test", description="test relationship"
        ).dict(),
    )
    assert response_create.status_code == 201
    assert response_create.json() == {
        "description": "test relationship",
        "id": 1,
        "name": "Rel",
        "type": "test",
    }


def test_create_relationship_security(
    client,
    user_token_headers,
):
    response_create = client.post(
        "/api/v1/document-relationship",
        headers=user_token_headers,
        json=RelationshipCreateRequest(
            name="Rel", type="test", description="test relationship"
        ).dict(),
    )
    assert response_create.status_code == 404
    assert response_create.json() == {"detail": "Not Found"}


# --- tests for GET /api/v1/document-relationship


def test_get_relationships(
    client,
    superuser_token_headers,
):
    _create_10_relationships(client, superuser_token_headers)

    response_get = client.get(
        "/api/v1/document-relationship", headers=superuser_token_headers
    )
    assert response_get.status_code == 200
    assert len(response_get.json()["relationships"]) == 10


def test_get_relationships_security(
    client,
    superuser_token_headers,
    user_token_headers,
):
    _create_10_relationships(client, superuser_token_headers)

    response_get = client.get(
        "/api/v1/document-relationship", headers=user_token_headers
    )
    assert response_get.status_code == 404
    assert response_get.json() == {"detail": "Not Found"}


# --- tests for POST /api/v1/document-relationship/id/document/id


def test_add_document_to_relationship(
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
    ) = create_4_documents(test_db, client, superuser_token_headers)

    rel_ids = _create_10_relationships(client, superuser_token_headers)

    # Set up document relationship
    response_docrel1 = client.post(
        f"/api/v1/document-relationship/{rel_ids[0]}/document/{response1_document['id']}",
        headers=superuser_token_headers,
    )
    assert response_docrel1.status_code == 201

    rels = test_db.query(DocumentRelationship).all()
    assert len(rels) == 1
    assert rels[0].relationship_id == rel_ids[0]
    assert rels[0].document_id == response1_document["id"]


def test_add_document_to_relationship_security(
    client,
    user_token_headers,
):

    # Set up document relationship
    response_docrel1 = client.post(
        "/api/v1/document-relationship/1/document/1",
        headers=user_token_headers,
    )
    assert response_docrel1.status_code == 404
    assert response_docrel1.json() == {"detail": "Not Found"}


# --- tests for DELETE /api/v1/document-relationship/id/document/id


def test_delete_document_from_relationship(
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
    ) = create_4_documents(test_db, client, superuser_token_headers)

    rel_ids = _create_10_relationships(client, superuser_token_headers)

    test_db.add(
        DocumentRelationship(
            document_id=response1_document["id"], relationship_id=rel_ids[0]
        )
    )

    test_db.commit()

    # Delete a document relationship
    response_reldel = client.delete(
        f"/api/v1/document-relationship/{rel_ids[0]}/document/{response1_document['id']}",
        headers=superuser_token_headers,
    )
    assert response_reldel.status_code == 200

    rel_found = (
        test_db.query(DocumentRelationship)
        .filter(DocumentRelationship.document_id == response1_document["id"])
        .filter(DocumentRelationship.relationship_id == rel_ids[0])
        .all()
    )

    assert len(rel_found) == 0

    docs_found = test_db.query(Document).count()

    assert docs_found == 4


def test_delete_document_from_relationship_security(
    client,
    user_token_headers,
):

    # Delete a document relationship
    response_reldel = client.delete(
        "/api/v1/document-relationship/1/document/1",
        headers=user_token_headers,
    )
    assert response_reldel.status_code == 404
    assert response_reldel.json() == {"detail": "Not Found"}


# --- tests for GET /api/v1/document-relationship/id


def test_get_relationship_documents(
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
    ) = create_4_documents(test_db, client, superuser_token_headers)

    rel_ids = _create_10_relationships(client, superuser_token_headers)

    test_db.add(
        DocumentRelationship(
            document_id=response1_document["id"], relationship_id=rel_ids[0]
        )
    )

    test_db.commit()

    response_get = client.get(
        f"/api/v1/document-relationship/{rel_ids[0]}", headers=superuser_token_headers
    )
    assert response_get.status_code == 200
    relationship = response_get.json()["relationship"]
    assert relationship == {
        "description": "test relationship 0",
        "id": 1,
        "name": "Rel0",
        "type": "test",
    }

    documents = response_get.json()["documents"]
    assert len(documents) == 1
    assert documents[0]["name"] == "Energy Sector Strategy 1387-1391 (2007/8-2012/3)"


def test_get_relationship_documents_security(
    client,
    user_token_headers,
):

    response_get = client.get(
        "/api/v1/document-relationship/1", headers=user_token_headers
    )

    assert response_get.status_code == 404
    assert response_get.json() == {"detail": "Not Found"}


# TODO : Un comment when relationships are going to replace associations
#
# def test_relationships_from_document_detail(
#     client,
#     superuser_token_headers,
#     user_token_headers,
#     test_db,
# ):
#
#     (
#         response1_document,
#         document1_payload,
#         response2_document,
#         document2_payload,
#         response3_document,
#         document3_payload,
#         response4_document,
#         document4_payload,
#     ) = create_4_documents(test_db, client, superuser_token_headers)
#
#     # Set up relationship entities
#     response_rel1 = client.post(
#         "/api/v1/document-relationship",
#         headers=superuser_token_headers,
#         json=RelationshipCreateRequest(
#             name="Rel1", type="test", description="test relationship 1"
#         ).dict(),
#     )
#     assert response_rel1.status_code == 201
#     rel1_id = response_rel1.json()["id"]
#
#     # Set up document relationship
#     response_docrel1 = client.post(
#         f"/api/v1/document-relationship/{rel1_id}/document/{response1_document['id']}",
#         headers=superuser_token_headers,
#     )
#     assert response_docrel1.status_code == 201
#
#     response_docrel2 = client.post(
#         f"/api/v1/document-relationship/{rel1_id}/document/{response2_document['id']}",
#         headers=superuser_token_headers,
#     )
#     assert response_docrel2.status_code == 201
#
#     response_docrel3 = client.post(
#         f"/api/v1/document-relationship/{rel1_id}/document/{response3_document['id']}",
#         headers=superuser_token_headers,
#     )
#     assert response_docrel3.status_code == 201
#
#     # Test properties
#     get_detail_response_2 = client.get(
#         f"/api/v1/documents/{response2_document['id']}",
#         headers=user_token_headers,
#     )
#     assert get_detail_response_2.status_code == 200
#
#     # Check some expected properties of the returned document
#     get_detail_json_2 = get_detail_response_2.json()
#
#
#     sorted_related_docs = sorted(
#         get_detail_json_2["related_documents"],
#         key=lambda d: d["document_id"],
#     )
#     assert sorted_related_docs == [
#         {
#             "document_id": response1_document["id"],
#             "name": "Energy Sector Strategy 1387-1391 (2007/8-2012/3)",
#             "description": "the document description",
#             "country_code": "NMFS",
#             "country_name": "not my favourite subject",
#             "publication_ts": "2000-01-01T00:00:00",
#         },
#         {
#             "document_id": response3_document["id"],
#             "name": "Energy Sector Strategy 1387-1391 (2009/8-2014/3)",
#             "description": "the document description",
#             "country_code": "NMFSA",
#             "country_name": "not my fav subject again",
#             "publication_ts": "1998-01-01T00:00:00",
#         },
#     ]
#
#     # Test related documents
#     get_detail_response_1 = client.get(
#         f"/api/v1/documents/{response1_document['id']}",
#         headers=user_token_headers,
#     )
#     assert get_detail_response_1.status_code == 200
#     get_detail_json_1 = get_detail_response_1.json()
#
#     assert set(rd["document_id"] for rd in get_detail_json_1["related_documents"]) == {
#         2,
#         3,
#     }
#
#     get_detail_response_3 = client.get(
#         f"/api/v1/documents/{response3_document['id']}",
#         headers=user_token_headers,
#     )
#     assert get_detail_response_3.status_code == 200
#     get_detail_json_3 = get_detail_response_3.json()
#
#     assert set(rd["document_id"] for rd in get_detail_json_3["related_documents"]) == {
#         1,
#         2,
#     }
#
#     get_detail_response_4 = client.get(
#         f"/api/v1/documents/{response4_document['id']}",
#         headers=user_token_headers,
#     )
#     assert get_detail_response_4.status_code == 200
#     get_detail_json_4 = get_detail_response_4.json()
#
#     assert get_detail_json_4["related_documents"] == []
#
#     # Check content types
#     assert get_detail_json_1["content_type"] == "application/pdf"
#     assert get_detail_json_2["content_type"] == "text/html"
#     assert (
#         get_detail_json_3["content_type"]
#         == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
#     )
#     assert get_detail_json_4["content_type"] == "unknown"
#
