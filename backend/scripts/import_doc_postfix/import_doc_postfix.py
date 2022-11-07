#!/usr/bin/env python3

import sys
from app.db.session import SessionLocal
from sqlalchemy.orm import Session

from app.core.validation.cclw.law_policy.process_csv import (
    validated_input,
    import_id_from_csv_row,
    POSTFIX_FIELD,
)


def _convert_associations_to_relationship(db: Session, id: int):
    db.commit()


if __name__ == "__main__":
    print("Importing document postfixes...")
    db = SessionLocal()

    if len(sys.argv) != 2:
        print("Require a CSV file to import")
        sys.exit(1)

    csv_reader = validated_input(open(sys.argv[1]))
    rows = [(row[POSTFIX_FIELD], import_id_from_csv_row(row)) for row in csv_reader]

    print(rows)
