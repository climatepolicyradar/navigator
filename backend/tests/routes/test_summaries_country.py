from http.client import OK, UNAUTHORIZED


def URL_UNDER_TEST(id: int) -> str:
    return f"/api/v1/summaries/country/{id}"


def test_endpoint_security(client):
    response = client.get(URL_UNDER_TEST(99))
    assert response.status_code == UNAUTHORIZED


def test_endpoint_returns_ok(client, user_token_headers):
    """Test the endpoint returns an empty sets of data"""
    response = client.get(
        URL_UNDER_TEST(11),
        headers=user_token_headers,
    )
    assert response.status_code == OK
    resp = response.json()

    assert resp["document_counts"]["Law"] == 0
    assert resp["document_counts"]["Policy"] == 0
    assert resp["document_counts"]["Case"] == 0

    assert len(resp["top_documents"]["Law"]) == 0
    assert len(resp["top_documents"]["Policy"]) == 0
    assert len(resp["top_documents"]["Case"]) == 0

    assert len(resp["events"]) == 0
    assert len(resp["targets"]) == 0


def test_geography_with_documents(client, user_token_headers, summary_country_data):
    """Test that all the data is returned filtered on category"""
    geography_id = summary_country_data["geos"][0].id
    response = client.get(
        URL_UNDER_TEST(geography_id),
        headers=user_token_headers,
    )
    assert response.status_code == OK
    resp = response.json()

    assert resp["document_counts"]["Law"] == 3
    assert resp["document_counts"]["Policy"] == 2
    assert resp["document_counts"]["Case"] == 0

    assert len(resp["top_documents"]["Law"]) == 3
    assert len(resp["top_documents"]["Policy"]) == 2
    assert len(resp["top_documents"]["Case"]) == 0

    assert len(resp["events"]) == 0
    assert len(resp["targets"]) == 0


def test_geography_with_documents_ordered(
    client, user_token_headers, summary_country_data
):
    """Test that all the data is returned ordered by published date"""
    geography_id = summary_country_data["geos"][0].id
    response = client.get(
        URL_UNDER_TEST(geography_id),
        headers=user_token_headers,
    )
    assert response.status_code == OK
    resp = response.json()

    assert len(resp["top_documents"]["Law"]) == 3

    assert resp["top_documents"]["Law"][0]["document_name"] == "doc3"
    assert resp["top_documents"]["Law"][1]["document_name"] == "doc2"
    assert resp["top_documents"]["Law"][2]["document_name"] == "doc1"
