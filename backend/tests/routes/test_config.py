from app.api.api_v1.routers.lookups.geo_stats import (
    GeoStatsResponse,
    lookup_geo_stats,
)

from app.api.api_v1.routers.lookups.main import lookup_config
from http.client import OK


def test_endpoint_returns_correct_data(
        client,
        user_token_headers
):
    """Tests whether we get the correct data when the /config endpoint is called."""
    url_under_test = "/api/v1/config"
    response = client.get(
        url_under_test,
        headers=user_token_headers,
    )
    print(response)
    assert response.status_code == OK


def test_endpoint_returns_correct_data_unauth(
        client
):
    """Tests whether we get the correct error code when making an unauthenticated request."""
    url_under_test = "/api/v1/config"
    response = client.get(
        url_under_test
    )
    assert response.status_code == 401

