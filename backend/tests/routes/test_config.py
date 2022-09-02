from http.client import OK, UNAUTHORIZED


def test_endpoint_returns_correct_data(client, user_token_headers):
    """Tests whether we get the correct data when the /config endpoint is called."""
    url_under_test = "/api/v1/config"

    response = client.get(
        url_under_test,
        headers=user_token_headers,
    )

    response_json = response.json()

    assert response.status_code == OK
    assert list(response_json["metadata"].keys()) == ["CCLW"]
    assert list(response_json["metadata"]["CCLW"].keys()) == [
        "geographies",
        "document_types",
        "sectors",
        "instruments",
    ]


def test_endpoint_returns_correct_data_unauth(client):
    """Tests whether we get the correct error code when making an unauthenticated request."""
    url_under_test = "/api/v1/config"
    response = client.get(url_under_test)
    assert response.status_code == UNAUTHORIZED