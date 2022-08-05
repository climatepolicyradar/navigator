#!/usr/bin/env python3

from typing import Dict, Mapping

from app.db.models import DocumentInstrument, DocumentKeyword, Instrument, Keyword
from app.db.session import Base, SessionLocal


LookupID = Mapping[str, int]


def get_model_values(db: SessionLocal, table: Base) -> LookupID:  # type: ignore
    id_lookup: Dict[str, int] = {}

    for row in db.query(table).all():
        should_update_lookup = row.name not in id_lookup or id_lookup[row.name] > int(
            row.id
        )
        if should_update_lookup:
            id_lookup[row.name] = int(row.id)

    return id_lookup


def cleanup_keyword_duplicates(db: SessionLocal) -> None:  # type: ignore
    clean_keyword_lookup_table = get_model_values(db, Keyword)
    desired_keyword_ids = list(clean_keyword_lookup_table.values())
    for document_keyword in db.query(DocumentKeyword).all():
        if int(document_keyword.keyword_id) not in desired_keyword_ids:
            # Get the name of the linked keyword & update to the desired value
            existing_keyword = (
                db.query(Keyword).filter(id=document_keyword.keyword_id).first()
            )
            required_id = clean_keyword_lookup_table[existing_keyword.name]
            document_keyword.keyword_id = required_id

    for keyword in db.query(Keyword).all():
        if keyword.id not in desired_keyword_ids:
            keyword.delete()


def cleanup_instrument_duplicates(db: SessionLocal) -> None:  # type: ignore
    clean_instrument_lookup_table = get_model_values(db, Instrument)
    desired_instrument_ids = list(clean_instrument_lookup_table.values())
    for row in db.query(DocumentInstrument).all():
        if int(row.instrument_id) not in desired_instrument_ids:
            # Get the name of the linked instrument & update to the desired value
            existing_instrument = (
                db.query(Instrument).filter(id=row.instrument_id).first()
            )
            required_id = clean_instrument_lookup_table[existing_instrument.name]
            row.keyword_id = required_id

    for instrument in db.query(Keyword).all():
        if instrument.id not in desired_instrument_ids:
            instrument.delete()


if __name__ == "__main__":
    print("Cleaning duplicated lookups in database...")
    db = SessionLocal()

    print("Cleaning Keywords...")
    cleanup_keyword_duplicates(db)
    print("Cleaning Instruments...")
    cleanup_instrument_duplicates(db)

    db.commit()
    print("Done cleaning duplicated lookups in database")
