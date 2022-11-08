import json
from typing import cast

from slugify import slugify
from sqlalchemy.orm import Session

from app.db.models import Geography
from .utils import has_rows, load_tree


def _add_geo_slugs(geo_tree: list[dict[str, dict]]):
    for entry in geo_tree:
        data = entry["node"]
        data["slug"] = slugify(data["display_value"], separator="-")

        child_nodes = cast(list[dict[str, dict]], entry["children"])
        if child_nodes:
            _add_geo_slugs(child_nodes)


def populate_geography(db: Session) -> None:
    """Populates the geography table with pre-defined data."""

    if has_rows(db, Geography):
        return

    with open("app/data_migrations/data/geography_data.json") as geo_data_file:
        geo_data = json.loads(geo_data_file.read())
        _add_geo_slugs(geo_data)
        load_tree(db, Geography, geo_data)
