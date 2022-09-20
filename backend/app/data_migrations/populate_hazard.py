import json

from sqlalchemy.orm import Session

from app.db.models import Hazard
from .utils import has_rows, load_list


def populate_hazard(db: Session) -> None:
    """Populates the hazard table with pre-defined data."""

    if has_rows(db, Hazard):
        return

    with open("app/data_migrations/data/hazard_data.json") as hazard_file:
        hazard_data = json.load(hazard_file)
        load_list(db, Hazard, hazard_data)
