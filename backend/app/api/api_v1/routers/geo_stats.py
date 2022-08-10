from http.client import NOT_FOUND
import logging
from app.db.session import get_db
from app.db.models.geography import GeoStatistics
from fastapi import Depends
from app.core.auth import get_current_active_user
from pydantic import BaseModel
from sqlalchemy import exc

_LOGGER = logging.getLogger(__name__)


class GeoStatsResponse(BaseModel):
    """The response definition from /get_stats/{geography_id}"""

    id: int
    name: str
    geography_id: int
    legislative_process: str
    federal: bool
    federal_details: str
    political_groups: str
    global_emissions_percent: float
    climate_risk_index: float
    worldbank_income_group: str
    visibility_status: str


get_get_stats_responses = {404: {"description": "Ooops"}}


def get_geo_stats(
    geography_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Get climate statistics for a geography by id.

    **NOTE**: This requires the geography_id to refer to a geography of
    type ISO-3166
    """

    try:
        row = db.query(GeoStatistics).filter_by(geography_id=geography_id).first()
    except exc.SQLAlchemyError as e:
        print(f"Unable to get geo stats for {geography_id}: Exception {e}")
        _LOGGER.error(f"Unable to get geo stats for {geography_id}: Exception {e}")
        return NOT_FOUND

    return GeoStatsResponse(
        id=row.id,
        name=row.name,
        geography_id=row.geography_id,
        legislative_process=row.legislative_process,
        federal=row.federal,
        federal_details=row.federal_details,
        political_groups=row.political_groups,
        global_emissions_percent=row.global_emissions_percent,
        climate_risk_index=row.climate_risk_index,
        worldbank_income_group=row.worldbank_income_group,
        visibility_status=row.visibility_status,
    )


def add_geo_stats_route(router):
    print("Adding route for geo_stats")
    _LOGGER.info("Adding route for geo_stats")
    router.add_api_route(
        "/geo_stats/{geography_id}",
        summary="Get climate statistics for a geography",
        endpoint=get_geo_stats,
        response_model=GeoStatsResponse,
        responses=get_get_stats_responses,
    )
