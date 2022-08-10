from fastapi.testclient import TestClient

from unittest.mock import Mock
from app.main import app

from app.api.api_v1.routers.geo_stats import (
    GeoStatsResponse,
    add_geo_stats_route,
    get_geo_stats,
)
from app.core.auth import get_current_active_user

client = TestClient(app)


async def override_current_user():
    return "a test user"


def test_adds_route():
    router = Mock()
    add_geo_stats_route(router)
    router.add_api_route.assert_called_once()


def test_endpoint_security():
    response = client.get("/api/v1/geo_stats/11")
    assert response.status_code == 401


def test_endpoint_returns_correct_data():
    app.dependency_overrides[get_current_active_user] = override_current_user

    response = client.get("/api/v1/geo_stats/11")
    stats = response.json()
    assert response.status_code == 200
    assert stats["id"] == 6
    assert stats["geography_id"] == 11
    assert stats["name"] == "Antigua and Barbuda"


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
