import csv

from sqlalchemy.orm import Session

from app.db.models import Sector
from .utils import has_rows


def populate_sector(db: Session) -> None:
    """Populates the sector table with data in the CSV."""
    if has_rows(db, Sector):
        return

    with open("app/data_migrations/data/sector.csv", mode="r") as file:
        # reading the CSV file
        csvFile = csv.DictReader(file)

        for row in csvFile:

            if row["parent_id"] == "null":
                row["parent_id"] = None

            # Add the Sector details
            sector = Sector(
                id=row["id"],
                parent_id=row["parent_id"],
                name=row["name"],
                description=row["description"],
                source_id=row["source_id"],
            )
            db.add(sector)
