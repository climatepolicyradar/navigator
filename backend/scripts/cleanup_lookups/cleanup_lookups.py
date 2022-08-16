#!/usr/bin/env python3

import pathlib
from csv import DictReader
from typing import Dict, Mapping

from sqlalchemy.orm import Session

from app.db.models import (
    DocumentInstrument,
    DocumentKeyword,
    DocumentSector,
    Instrument,
    Keyword,
    Sector,
)
from app.db.session import Base, SessionLocal


LookupID = Mapping[str, int]


def get_model_clean_lookup_table(db: Session, table: Base) -> LookupID:
    """Gets values for metadata tables & spots duplicates by string matched on name"""
    id_lookup: Dict[str, int] = {}

    for object_instance in db.query(table).all():
        should_update_lookup = object_instance.name not in id_lookup or id_lookup[
            object_instance.name
        ] > int(object_instance.id)
        if should_update_lookup:
            id_lookup[object_instance.name] = int(object_instance.id)

    return id_lookup


def cleanup_keyword_duplicates(db: SessionLocal) -> None:  # type: ignore
    clean_keyword_lookup_table = get_model_clean_lookup_table(db, Keyword)
    desired_keyword_ids = list(clean_keyword_lookup_table.values())
    for document_keyword in db.query(DocumentKeyword).all():
        if int(document_keyword.keyword_id) not in desired_keyword_ids:
            # Get the name of the linked keyword & update to the desired value
            existing_keyword = db.query(Keyword).get(document_keyword.keyword_id)
            required_id = clean_keyword_lookup_table[existing_keyword.name]
            document_keyword.keyword_id = required_id

    db.flush()

    for keyword in db.query(Keyword).all():
        if keyword.id not in desired_keyword_ids:
            db.delete(keyword)


def cleanup_instrument_duplicates(db: SessionLocal) -> None:  # type: ignore
    clean_instrument_lookup_table = get_model_clean_lookup_table(db, Instrument)
    desired_instrument_ids = list(clean_instrument_lookup_table.values())
    for document_instrument in db.query(DocumentInstrument).all():
        if int(document_instrument.instrument_id) not in desired_instrument_ids:
            # Get the name of the linked instrument & update to the desired value
            existing_instrument = db.query(Instrument).get(
                document_instrument.instrument_id
            )
            required_id = clean_instrument_lookup_table[existing_instrument.name]
            document_instrument.instrument_id = required_id

    db.flush()

    for instrument in db.query(Instrument).all():
        if instrument.id not in desired_instrument_ids:
            db.delete(instrument)


def cleanup_sector_duplicates(db: SessionLocal) -> None:  # type: ignore
    clean_sector_lookup_table = get_model_clean_lookup_table(db, Sector)
    desired_sector_ids = list(clean_sector_lookup_table.values())
    for document_sector in db.query(DocumentSector).all():
        if int(document_sector.sector_id) not in desired_sector_ids:
            # Get the name of the linked sector & update to the desired value
            existing_sector = db.query(Sector).get(document_sector.sector_id)
            required_id = clean_sector_lookup_table[existing_sector.name]
            document_sector.sector_id = required_id

    db.flush()

    for sector in db.query(Sector).all():
        if sector.id not in desired_sector_ids:
            db.delete(sector)


def load_keyword_map() -> Mapping[str, str]:
    current_folder = pathlib.Path(__file__).parent.absolute()
    keyword_map_file = current_folder / "keyword_map.csv"
    with open(keyword_map_file, "r") as keyword_map_file_handle:
        keyword_map_csv = DictReader(keyword_map_file_handle)
        keyword_map = {}
        for row in keyword_map_csv:
            keyword_map[row["name"]] = row["desired_keyword"]

        return keyword_map


def get_clean_keyword_map(db: SessionLocal) -> Mapping[int, int]:  # type: ignore
    """Gets values for updating document keyword references"""
    keyword_map = load_keyword_map()

    existing_keywords = set(keyword_map.keys())
    desired_keywords = set(keyword_map.values())
    keywords_to_create = desired_keywords - existing_keywords

    name_lookup: Dict[str, int] = {}
    for k in keywords_to_create:
        new_keyword = Keyword(name=k, description="Imported by CPR loader")
        db.add(new_keyword)
        db.flush()
        db.refresh(new_keyword)
        name_lookup[k] = int(new_keyword.id)  # type: ignore

    id_lookup: Dict[int, int] = {}
    for keyword in db.query(Keyword).all():
        name_lookup[keyword.name] = int(keyword.id)

    for keyword_name, keyword_id in name_lookup.items():
        # Only provide mappings from the original keywords to the updated ones
        if keyword_name in keyword_map:
            id_lookup[keyword_id] = name_lookup[keyword_map[keyword_name]]

    return id_lookup


def update_keyword_links(
    db: SessionLocal,  # type: ignore
    clean_keyword_lookup_table: Mapping[int, int],
) -> None:
    """Updates the join tables between document & keyword to the preferred IDs"""
    for document_keyword in db.query(DocumentKeyword).all():
        dkid = document_keyword.keyword_id
        if dkid in clean_keyword_lookup_table:
            document_keyword.keyword_id = clean_keyword_lookup_table[dkid]

    db.flush()

    for kid in clean_keyword_lookup_table:
        if clean_keyword_lookup_table[kid] != kid:
            keyword_to_delete = db.query(Keyword).get(kid)
            db.delete(keyword_to_delete)


def cleanup_human_error_keywords(db: SessionLocal) -> None:  # type: ignore
    clean_keyword_lookup_table = get_clean_keyword_map(db)
    update_keyword_links(db, clean_keyword_lookup_table)


if __name__ == "__main__":
    print("Cleaning duplicated lookups in database...")
    db = SessionLocal()

    print("Cleaning Keywords...")
    cleanup_keyword_duplicates(db)
    db.commit()

    print("Updating Human Error Keywords...")
    cleanup_human_error_keywords(db)
    db.commit()

    print("Cleaning Instruments...")
    cleanup_instrument_duplicates(db)
    db.commit()

    print("Cleaning Sectors...")
    cleanup_sector_duplicates(db)
    db.commit()

    print("Done cleaning duplicated lookups in database")
