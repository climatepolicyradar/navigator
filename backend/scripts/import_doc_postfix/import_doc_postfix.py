#!/usr/bin/env python3

import sys
from app.db.models.document import Document
from app.db.session import SessionLocal

from app.core.validation.cclw.law_policy.process_csv import (
    validated_input,
    import_id_from_csv_row,
    POSTFIX_FIELD,
)

if __name__ == "__main__":
    print("Importing document postfixes...")
    db = SessionLocal()

    if len(sys.argv) != 2:
        print("Require a CSV file to import")
        sys.exit(1)

    csv_reader = validated_input(open(sys.argv[1]))
    mappings = [
        {
            "import_id": import_id_from_csv_row(row),
            "id": db.query(Document.id)
            .filter(Document.import_id == import_id_from_csv_row(row))
            .scalar(),
            "postfix": row[POSTFIX_FIELD],
        }
        for row in csv_reader
    ]
    id_postfix_mappings = [
        {
            "id": row["id"],
            "postfix": row["postfix"],
        }
        for row in mappings
        if row["id"] is not None
    ]
    print(id_postfix_mappings)

    # Now https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-bulk-update
    db.bulk_update_mappings(Document, id_postfix_mappings)
    db.commit()
