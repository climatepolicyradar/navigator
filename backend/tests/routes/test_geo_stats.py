from http.client import NOT_FOUND, OK, UNAUTHORIZED
from unittest.mock import Mock
from app.initial_data import populate_initial_data

from app.api.api_v1.routers.lookups.geo_stats import (
    GeoStatsResponse,
    lookup_geo_stats,
)

TEST_ID = 11
TEST_GEO_NAME = "Antigua and Barbuda"
URL_UNDER_TEST = f"/api/v1/geo_stats/{TEST_ID}"


def test_endpoint_security(client):
    response = client.get(URL_UNDER_TEST)
    assert response.status_code == UNAUTHORIZED


def test_endpoint_returns_correct_data(client, user_token_headers, test_db):
    populate_initial_data(test_db)
    test_db.flush()  # update the session, no need to commit as its just a test

    response = client.get(
        URL_UNDER_TEST,
        headers=user_token_headers,
    )
    stats = response.json()
    assert response.status_code == OK
    assert stats["id"] == 6
    assert stats["geography_id"] == TEST_ID
    assert stats["name"] == TEST_GEO_NAME


def test_endpoint_returns_not_found(client, user_token_headers, test_db):
    response = client.get(
        URL_UNDER_TEST,
        headers=user_token_headers,
    )
    assert response.status_code == NOT_FOUND


def test_queries_db():
    db = Mock()
    query = Mock()
    filter_by = Mock()

    db.query.return_value = query
    query.filter_by.return_value = filter_by
    filter_by.first.return_value = GeoStatsResponse(
        id=TEST_ID,
        name=TEST_GEO_NAME,
        geography_id=1,
        legislative_process="row.legislative_process",
        federal=True,
        federal_details="row.federal_details",
        political_groups="row.political_groups",
        global_emissions_percent=0.1,
        climate_risk_index=0.2,
        worldbank_income_group="row.worldbank_income_group",
        visibility_status="row.visibility_status",
    )

    response = lookup_geo_stats(TEST_ID, db=db, current_user=None)
    db.query.assert_called_once()
    assert response.id == TEST_ID
    assert response.name == TEST_GEO_NAME
