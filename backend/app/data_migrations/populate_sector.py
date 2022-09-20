import json

from sqlalchemy.orm import Session

from app.db.models import Sector
from .utils import has_rows, load_tree, map_source_ids


def populate_sector(db: Session) -> None:
    """Populates the sector table with pre-defined data."""

    if has_rows(db, Sector):
        return

    with open("app/data_migrations/data/sector_data.json", mode="r") as sector_file:
        sector_data = json.load(sector_file)
        load_tree(db, Sector, map_source_ids(db, sector_data))
