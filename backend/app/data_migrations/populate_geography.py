import csv

from sqlalchemy.orm import Session

from app.db.models import Geography
from .utils import has_rows


def populate_geography(db: Session) -> None:
    """Populates the geography table with data in the CSV."""
    if has_rows(db, Geography):
        return

    # Get iso-3166 country codes. This file contains the standard iso-3166 codes + additional country codes for
    # regions that are missing - e.g. sub-saharan africa
    with open("app/data_migrations/data/geography-iso-3166.csv", mode="r") as file:
        # reading the CSV file
        csvFile = csv.DictReader(file)

        for row in csvFile:

            args = {
                "display_value": row["World Bank Region"],
                "value": row["World Bank Region"],
                "type": "World Bank Region",
            }

            # Query for the parent already existing
            geo_parent = db.query(Geography).filter_by(**args).first()

            if not geo_parent:
                # Create the parent
                geo_parent = Geography(**args)
                db.add(geo_parent)
                db.flush()

            # Add the ISO-3166 Geography details
            geo = Geography(
                display_value=row["Name"],
                value=row["Iso"],
                type="ISO-3166",
                parent_id=geo_parent.id,
            )
            db.add(geo)
