import logging
from http.client import NOT_FOUND
from typing import Any, Dict, Optional, Union

from fastapi import Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import exc

from app.db.session import get_db
from app.db.models.geography import Geography, GeoStatistics
from .router import lookups_router

_LOGGER = logging.getLogger(__name__)


class GeoStatsResponse(BaseModel):
    """The response definition from /get_stats/{geography_id}"""

    name: str
    geography_slug: str
    legislative_process: str
    federal: bool
    federal_details: str
    political_groups: str
    global_emissions_percent: Optional[float] = None
    climate_risk_index: Optional[float] = None
    worldbank_income_group: str
    visibility_status: str


lookup_geo_stats_responses: Dict[Union[int, str], Dict[str, Any]] = {
    404: {"description": "Statistics for Geography Id was not found"}
}


@lookups_router.get(
    "/geo_stats/{geography_slug}",
    summary="Get climate statistics for a geography",
    response_model=GeoStatsResponse,
    responses=lookup_geo_stats_responses,
)
def lookup_geo_stats(
    geography_slug: str,
    db=Depends(get_db),
):
    """
    Get climate statistics for a geography by id.

    **NOTE**: This requires the geography_id to refer to a geography of
              type ISO-3166
    """
    _LOGGER.info(f"Getting geo stats for {geography_slug}")
    not_found_msg = f"Unable to get geo stats for {geography_slug}"

    try:
        existing_geography_id = (
            db.query(Geography.id).filter(Geography.slug == geography_slug).scalar()
        )
        if existing_geography_id is None:
            raise HTTPException(status_code=NOT_FOUND, detail=not_found_msg)

        existing_geo_stats = (
            db.query(GeoStatistics)
            .filter_by(geography_id=existing_geography_id)
            .first()
        )
        if existing_geo_stats is None:
            _LOGGER.error(not_found_msg)
            raise HTTPException(status_code=NOT_FOUND, detail=not_found_msg)
    except exc.SQLAlchemyError:
        _LOGGER.exception(not_found_msg)
        raise HTTPException(status_code=NOT_FOUND, detail=not_found_msg)

    return GeoStatsResponse(
        name=existing_geo_stats.name,
        geography_slug=geography_slug,
        legislative_process=existing_geo_stats.legislative_process,
        federal=existing_geo_stats.federal,
        federal_details=existing_geo_stats.federal_details,
        political_groups=existing_geo_stats.political_groups,
        global_emissions_percent=existing_geo_stats.global_emissions_percent,
        climate_risk_index=existing_geo_stats.climate_risk_index,
        worldbank_income_group=existing_geo_stats.worldbank_income_group,
        visibility_status=existing_geo_stats.visibility_status,
    )
