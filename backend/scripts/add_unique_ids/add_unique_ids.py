#!/usr/bin/env python3
import json
import pathlib
from typing import Mapping

from sqlalchemy.orm import Session

from app.db.models import Document
from app.db.session import SessionLocal


LookupID = Mapping[str, str]


def load_id_map() -> Mapping[str, str]:
    current_folder = pathlib.Path(__file__).parent.absolute()
    id_map_path = current_folder / "ids_map.json"
    with open(id_map_path) as id_map_file:
        id_map = json.load(id_map_file)
        return id_map


def add_unique_ids(
    db: Session,
    unique_id_map: Mapping[str, str],
) -> None:
    """Updates each document with an externally derived unique ID"""
    for document in db.query(Document).all():
        doc_id = str(document.id)
        if doc_id not in unique_id_map:
            print(f"Error: Could not find mapping for document database id '{doc_id}'")
            continue
        unique_id = unique_id_map[doc_id]
        document.import_id = unique_id

    db.commit()


if __name__ == "__main__":
    print("Adding unique IDs...")

    db = SessionLocal()
    id_map = load_id_map()
    add_unique_ids(db, id_map)

    print("Done adding unique IDs")
