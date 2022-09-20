import json

from sqlalchemy.orm import Session

from app.db.models import Response
from .utils import has_rows, load_list


# TODO: Rename Response -> Topic
def populate_topic(db: Session) -> None:
    """Populates the topics(Response) table with pre-defined data."""

    if has_rows(db, Response):
        return

    with open("app/data_migrations/data/topic_data.json") as topic_file:
        topic_data = json.load(topic_file)
        load_list(db, Response, topic_data)
