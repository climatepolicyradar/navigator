import json

from sqlalchemy.orm import Session

from app.db.models import Instrument
from .utils import has_rows, load_tree, map_source_ids


def populate_instrument(db: Session) -> None:
    """Populates the instrument table with pre-defined data."""

    if has_rows(db, Instrument):
        return

    with open("app/data_migrations/data/instrument_data.json") as instrument_file:
        instrument_data = json.load(instrument_file)
        load_tree(db, Instrument, map_source_ids(db, instrument_data))
