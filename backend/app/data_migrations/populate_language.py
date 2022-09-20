import json

from sqlalchemy.orm import Session

from app.db.models import Language
from .utils import has_rows, load_list


def populate_language(db: Session) -> None:
    """Populates the langauge table with pre-defined data."""

    if has_rows(db, Language):
        return

    with open("app/data_migrations/data/language_data.json") as language_file:
        language_data = json.load(language_file)
        load_list(db, Language, language_data)
