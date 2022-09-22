import json

from sqlalchemy.orm import Session

from app.db.models import Framework
from .utils import has_rows, load_list


def populate_framework(db: Session) -> None:
    """Populates the framework table with pre-defined data."""

    if has_rows(db, Framework):
        return

    with open("app/data_migrations/data/framework_data.json") as framework_file:
        framework_data = json.load(framework_file)
        load_list(db, Framework, framework_data)
