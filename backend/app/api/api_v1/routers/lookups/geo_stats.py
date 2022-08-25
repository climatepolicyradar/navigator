from http.client import NOT_FOUND
import logging
from typing import Any, Dict, Optional, Union
from app.db.session import get_db
from app.db.models.geography import GeoStatistics
from fastapi import Depends, HTTPException
from app.core.auth import get_current_active_user
from pydantic import BaseModel
from sqlalchemy import exc
from .router import lookups_router

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
    global_emissions_percent: Optional[float] = None
    climate_risk_index: Optional[float] = None
    worldbank_income_group: str
    visibility_status: str


lookup_geo_stats_responses: Dict[Union[int, str], Dict[str, Any]] = {
    404: {"description": "Statistics for Geography Id was not found"}
}


@lookups_router.get(
    "/geo_stats/{geography_id}",
    summary="Get climate statistics for a geography",
    response_model=GeoStatsResponse,
    responses=lookup_geo_stats_responses,
)
def lookup_geo_stats(
    geography_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Get climate statistics for a geography by id.

    **NOTE**: This requires the geography_id to refer to a geography of
    type ISO-3166
    """

    _LOGGER.info(f"Getting geo stats for {geography_id}")
    try:
        row = db.query(GeoStatistics).filter_by(geography_id=geography_id).first()
    except exc.SQLAlchemyError:
        msg = f"Unable to get geo stats for {geography_id}"
        _LOGGER.exception(msg)
        raise HTTPException(status_code=NOT_FOUND, detail=msg)

    if row is None:
        msg = f"Unable to get geo stats for {geography_id}"
        _LOGGER.error(msg)
        raise HTTPException(status_code=NOT_FOUND, detail=msg)

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
