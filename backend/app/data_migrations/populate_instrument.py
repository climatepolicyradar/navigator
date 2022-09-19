import json

from sqlalchemy.orm import Session

from app.db.models import Instrument
from .utils import has_rows, load_list


def populate_instrument(db: Session) -> None:
    """Populate instruments from CSV file."""

    if has_rows(db, Instrument):
        return

    with open("app/data_migrations/data/instrument_data.json") as instrument_file:
        instrument_data = json.load(instrument_file)
        load_list(db, Instrument, instrument_data)
