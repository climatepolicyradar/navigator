import csv
from typing import Union
from app.db.models import Geography, GeoStatistics
from app.db.session import SessionLocal
from .utils import has_rows


def to_float(value: str) -> Union[float, None]:
    first_str = value.split(" ")[0]
    retval = None
    try:
        retval = float(first_str)
    except ValueError:
        print(f"Unparsable for float: {first_str}")
    return retval


def populate_geo_statistics(db: SessionLocal) -> None:
    """Populates the geography table with data in the CSV."""

    if has_rows(db, GeoStatistics):
        return

    # Get iso-3166 country codes. This file contains the standard iso-3166 codes + additional country codes for
    # regions that are missing - e.g. sub-saharan africa
    with open("app/data_migrations/data/geo-stats-Aug2022.csv", mode="r") as file:
        # reading the CSV file
        csvFile = csv.DictReader(file)

        for row in csvFile:
            geography_id = (
                db.query(Geography.id)
                .filter_by(value=row["Iso"], display_value=row["Name"])
                .scalar()
            )
            db.add(
                GeoStatistics(
                    name=row["Name"],
                    geography_id=geography_id,
                    legislative_process=row["Legislative process"],
                    federal=bool(row["Federal"]),
                    federal_details=row["Federal details"],
                    political_groups=row["Political groups"],
                    global_emissions_percent=to_float(row["Percent global emissions"]),
                    climate_risk_index=to_float(row["Climate risk index"]),
                    worldbank_income_group=row["Wb income group"],
                    visibility_status=row["Visibility status"],
                )
            )
