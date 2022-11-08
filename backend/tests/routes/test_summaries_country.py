from http.client import OK


def URL_UNDER_TEST(slug: str) -> str:
    return f"/api/v1/summaries/country/{slug}"


def test_endpoint_returns_ok(client):
    """Test the endpoint returns an empty sets of data"""
    response = client.get(
        URL_UNDER_TEST("moldova"),
    )
    assert response.status_code == OK
    resp = response.json()

    assert resp["document_counts"]["Law"] == 0
    assert resp["document_counts"]["Policy"] == 0
    assert resp["document_counts"]["Case"] == 0

    assert len(resp["top_documents"]["Law"]) == 0
    assert len(resp["top_documents"]["Policy"]) == 0
    assert len(resp["top_documents"]["Case"]) == 0

    assert len(resp["targets"]) == 0


def test_geography_with_documents(client, summary_country_data):
    """Test that all the data is returned filtered on category"""
    geography_slug = summary_country_data["geos"][0].slug
    response = client.get(
        URL_UNDER_TEST(geography_slug),
    )
    assert response.status_code == OK
    resp = response.json()

    assert resp["document_counts"]["Law"] == 3
    assert resp["document_counts"]["Policy"] == 2
    assert resp["document_counts"]["Case"] == 0

    assert len(resp["top_documents"]["Law"]) == 3
    assert len(resp["top_documents"]["Policy"]) == 2
    assert len(resp["top_documents"]["Case"]) == 0

    assert len(resp["targets"]) == 0


def test_geography_with_documents_ordered(client, summary_country_data):
    """Test that all the data is returned ordered by published date"""
    geography_slug = summary_country_data["geos"][0].slug
    response = client.get(
        URL_UNDER_TEST(geography_slug),
    )
    assert response.status_code == OK
    resp = response.json()

    assert len(resp["top_documents"]["Law"]) == 3

    assert resp["top_documents"]["Law"][0]["document_name"] == "doc3"
    assert resp["top_documents"]["Law"][1]["document_name"] == "doc2"
    assert resp["top_documents"]["Law"][2]["document_name"] == "doc1"
