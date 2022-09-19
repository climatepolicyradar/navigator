import json

from sqlalchemy.orm import Session

from app.db.models import Geography
from .utils import has_rows, load_tree


def populate_geography(db: Session) -> None:
    """Populates the geography table with data in the CSV."""
    if has_rows(db, Geography):
        return

    with open("app/data_migrations/data/geography_data.json") as geo_data_file:
        geo_data = json.loads(geo_data_file.read())
        load_tree(db, Geography, geo_data)
