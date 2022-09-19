import json

from sqlalchemy.orm import Session

from app.db.models import Response
from .utils import has_rows, load_list


# TODO: Rename Response -> Topic
def populate_response(db: Session) -> None:
    """Populate responses from CSV file."""

    if has_rows(db, Response):
        return

    with open("app/data_migrations/data/response_data.json") as response_file:
        response_data = json.load(response_file)
        load_list(db, Response, response_data)
