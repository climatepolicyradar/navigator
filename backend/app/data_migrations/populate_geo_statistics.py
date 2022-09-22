import json
from typing import Union

from sqlalchemy.orm import Session

from app.db.models import Geography, GeoStatistics
from .utils import has_rows


def to_float(value: str) -> Union[float, None]:
    first_str = value.split(" ")[0]
    retval = None
    try:
        retval = float(first_str)
    except ValueError:
        print(f"Unparsable for float: {first_str}")
    return retval


def populate_geo_statistics(db: Session) -> None:
    """Populates the geo_statistics table with pre-defined data."""

    if has_rows(db, GeoStatistics):
        return

    # Load geo_stats data from structured data file
    with open("app/data_migrations/data/geo_stats_data.json") as geo_stats_file:
        geo_stats_data = json.load(geo_stats_file)
        for geo_stat in geo_stats_data:
            geography_id = (
                db.query(Geography.id)
                .filter_by(value=geo_stat["iso"], display_value=geo_stat["name"])
                .scalar()
            )
            args = {**geo_stat}
            args["geography_id"] = geography_id
            del args["iso"]
            db.add(GeoStatistics(**args))
