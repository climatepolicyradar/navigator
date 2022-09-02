from app.api.api_v1.schemas.document import RelationshipCreateRequest

# from .test_documents import create_4_documents


def _create_10_relationships(client, superuser_token_headers):
    # Set up relationship entities
    for x in range(10):
        response_rel = client.post(
            "/api/v1/document-relationship",
            headers=superuser_token_headers,
            json=RelationshipCreateRequest(
                name=f"Rel{x}", type="test", description=f"test relationship {x}"
            ).dict(),
        )
        assert response_rel.status_code == 201


def test_get_relationships(
    client,
    superuser_token_headers,
    user_token_headers,
    test_db,
):
    _create_10_relationships(client, superuser_token_headers)

    response_get = client.get(
        "/api/v1/document-relationship", headers=superuser_token_headers
    )
    assert response_get.status_code == 200
    assert len(response_get.json()["relationships"]) == 10


# TODO : Un comment when relationships are going to replace associations
#
# def test_document_detail(
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
