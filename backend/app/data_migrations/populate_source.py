import json

from sqlalchemy.orm import Session

from app.db.models import Source
from .utils import has_rows, load_list


def populate_source(db: Session) -> None:
    """Populates the source table with pre-defined data."""

    if has_rows(db, Source):
        return

    with open("app/data_migrations/data/source_data.json") as source_file:
        source_data = json.load(source_file)
        load_list(db, Source, source_data)
