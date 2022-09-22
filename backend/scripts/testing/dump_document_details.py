#!/usr/bin/env python3
"""Script that dumps to a json array all the documents in the database by calling the `get_document_detail()` function.

This script is useful to confirm the behaviour of the endpoint.
"""
import json
from app.db.models.document import Document
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
from app.db.crud.document import get_document_detail


def all_document_ids(db: Session):
    return [id for id, in db.query(Document.id)]


if __name__ == "__main__":
    db = SessionLocal()
    ids = all_document_ids(db)

    output = []
    for id in ids:
        detail = get_document_detail(db, id)
        output.append(json.loads(detail.json()))

    print(json.dumps(output, sort_keys=True))
