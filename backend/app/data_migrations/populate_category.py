import json

from sqlalchemy.orm import Session

from app.db.models import Category
from .utils import has_rows, load_list


def populate_category(db: Session) -> None:
    """Populates the category table with pre-defined data."""

    if has_rows(db, Category):
        return

    with open("app/data_migrations/data/category_data.json") as category_file:
        category_data = json.load(category_file)
        load_list(db, Category, category_data)
