from unittest.mock import Mock
from app.initial_data import populate_initial_data

from app.api.api_v1.routers.geo_stats import (
    GeoStatsResponse,
    add_geo_stats_route,
    get_geo_stats,
)


def test_adds_route():
    router = Mock()
    add_geo_stats_route(router)
    router.add_api_route.assert_called_once()


def test_endpoint_security(client):
    response = client.get("/api/v1/geo_stats/11")
    assert response.status_code == 401


def test_endpoint_returns_correct_data(client, user_token_headers, test_db):
    populate_initial_data(test_db)
    test_db.flush()  # update the session, no need to commit as its just a test

    TEST_ID = 11
    TEST_GEO_NAME = "Antigua and Barbuda"

    response = client.get(
        f"/api/v1/geo_stats/{TEST_ID}",
        headers=user_token_headers,
    )
    stats = response.json()
    assert response.status_code == 200
    assert stats["id"] == 6
    assert stats["geography_id"] == {TEST_ID}
    assert stats["name"] == TEST_GEO_NAME


def test_queries_db():
    db = Mock()
    query = Mock()
    filter_by = Mock()

    db.query.return_value = query
    query.filter_by.return_value = filter_by
    filter_by.first.return_value = GeoStatsResponse(
        id=123,
        name="row.name",
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

    response = get_geo_stats(123, db=db, current_user=None)
    db.query.assert_called_once()
    assert response.id == 123
