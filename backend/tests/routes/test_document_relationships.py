from app.api.api_v1.schemas.document import RelationshipCreateRequest
from app.db.models.document import Document, DocumentRelationship, Relationship

from .test_documents import create_4_documents


def _create_10_relationships(client, superuser_token_headers):
    rel_ids = []
    for x in range(10):
        response_rel = client.post(
            "/api/v1/document-relationships",
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
        "/api/v1/document-relationships",
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
):
    response_create = client.post(
        "/api/v1/document-relationships",
        json=RelationshipCreateRequest(
            name="Rel", type="test", description="test relationship"
        ).dict(),
    )
    assert response_create.status_code == 401
    assert response_create.json() == {"detail": "Not authenticated"}


# --- tests for GET /api/v1/document-relationship


def test_get_relationships(
    client,
    superuser_token_headers,
):
    _create_10_relationships(client, superuser_token_headers)

    response_get = client.get(
        "/api/v1/document-relationships", headers=superuser_token_headers
    )
    assert response_get.status_code == 200
    assert len(response_get.json()) == 10


def test_get_relationships_security(
    client,
    superuser_token_headers,
):
    _create_10_relationships(client, superuser_token_headers)

    response_get = client.get(
        "/api/v1/document-relationships",
    )
    assert response_get.status_code == 401
    assert response_get.json() == {"detail": "Not authenticated"}


# --- tests for POST /api/v1/document-relationships/id/documents/id


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
    ) = create_4_documents(test_db)

    rel_ids = _create_10_relationships(client, superuser_token_headers)

    # Set up document relationship
    response_docrel1 = client.put(
        f"/api/v1/document-relationships/{rel_ids[0]}/documents/{response1_document['id']}",
        headers=superuser_token_headers,
    )
    assert response_docrel1.status_code == 201

    rels = test_db.query(DocumentRelationship).all()
    assert len(rels) == 1
    assert rels[0].relationship_id == rel_ids[0]
    assert rels[0].document_id == response1_document["id"]


def test_add_document_to_relationship_is_idempotent(
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

    rel_ids = _create_10_relationships(client, superuser_token_headers)

    # Set up document relationship
    client.put(
        f"/api/v1/document-relationships/{rel_ids[0]}/documents/{response1_document['id']}",
        headers=superuser_token_headers,
    )
    response_docrel1 = client.put(
        f"/api/v1/document-relationships/{rel_ids[0]}/documents/{response1_document['id']}",
        headers=superuser_token_headers,
    )
    assert response_docrel1.status_code == 200

    rels = test_db.query(DocumentRelationship).all()
    assert len(rels) == 1
    assert rels[0].relationship_id == rel_ids[0]
    assert rels[0].document_id == response1_document["id"]


def test_add_document_to_relationship_security(
    client,
):

    # Set up document relationship
    response_docrel1 = client.put(
        "/api/v1/document-relationships/1/documents/1",
    )
    assert response_docrel1.status_code == 401
    assert response_docrel1.json() == {"detail": "Not authenticated"}


# --- tests for DELETE /api/v1/document-relationships/id/documents/id


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
    ) = create_4_documents(test_db)

    rel_ids = _create_10_relationships(client, superuser_token_headers)

    test_db.add(
        DocumentRelationship(
            document_id=response1_document["id"], relationship_id=rel_ids[0]
        )
    )

    test_db.commit()

    # Delete a document relationship
    response_reldel = client.delete(
        f"/api/v1/document-relationships/{rel_ids[0]}/documents/{response1_document['id']}",
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
    rels_found = test_db.query(Relationship).count()
    assert rels_found == 10


def test_delete_document_from_relationship_security(
    client,
):

    # Delete a document relationship
    response_reldel = client.delete(
        "/api/v1/document-relationships/1/documents/1",
    )
    assert response_reldel.status_code == 401
    assert response_reldel.json() == {"detail": "Not authenticated"}


# --- tests for GET /api/v1/document-relationships/id


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
    ) = create_4_documents(test_db)

    rel_ids = _create_10_relationships(client, superuser_token_headers)

    test_db.add(
        DocumentRelationship(
            document_id=response1_document["id"], relationship_id=rel_ids[0]
        )
    )

    test_db.commit()

    response_get = client.get(
        f"/api/v1/document-relationships/{rel_ids[0]}", headers=superuser_token_headers
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
):

    response_get = client.get(
        "/api/v1/document-relationships/1",
    )

    assert response_get.status_code == 401
    assert response_get.json() == {"detail": "Not authenticated"}
