import json

from sqlalchemy.orm import Session

from app.db.models import Keyword
from .utils import has_rows, load_list


def populate_keyword(db: Session) -> None:
    """Populates the keyword table with pre-defined data."""

    if has_rows(db, Keyword):
        return

    with open("app/data_migrations/data/keyword_data.json") as keyword_file:
        keyword_data = json.load(keyword_file)
        load_list(db, Keyword, keyword_data)
