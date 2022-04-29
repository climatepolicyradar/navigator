from fastapi import (
    HTTPException,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.crud.document import create_document
from app.db.schemas.metadata import DocumentCreateWithMetadata
from app.db.models import (
    Document,
    Event,
    Sector,
    Hazard,
    Response,
    DocumentSector,
    DocumentHazard,
    DocumentResponse,
    Framework,
    DocumentFramework,
    Instrument,
    DocumentInstrument,
)
from sqlalchemy.dialects.postgresql import insert


def persist_document_and_metadata(
    db: Session,
    document_with_metadata: DocumentCreateWithMetadata,
    creator_id: int,
):
    try:
        db_document = create_document(db, document_with_metadata.document, creator_id)
        write_metadata(db, db_document, document_with_metadata)
        db.commit()

        return db_document
    except Exception as e:
        if isinstance(e, IntegrityError):
            raise HTTPException(409, detail="Document already exists")
        raise e


def write_metadata(
    db: Session,
    db_document: Document,
    document_with_metadata: DocumentCreateWithMetadata,
):
    # events
    for event in document_with_metadata.events:
        db_event = Event(
            document_id=db_document.id,
            name=event.name,
            description=event.description,
        )
        db.add(db_event)

    # sectors
    for meta in document_with_metadata.sectors:
        insert_stmt = insert(Sector).values(
            # parent_id=TODO,
            name=meta.name,
            description=meta.description,
            source_id=db_document.source_id,
        )
        do_nothing_stmt = insert_stmt.on_conflict_do_nothing()
        return_value = db.execute(do_nothing_stmt)
        if return_value and return_value.inserted_primary_key:
            meta_id = return_value.inserted_primary_key[0]
            # TODO potentially use meta_id as parent_id
            db_bridge = DocumentSector(
                sector_id=meta_id,
                document_id=db_document.id,
            )
            db.add(db_bridge)

    # instruments
    for meta in document_with_metadata.instruments:
        insert_stmt = insert(Instrument).values(
            # parent_id=TODO,
            name=meta.name,
            description=meta.description,
            source_id=db_document.source_id,
        )
        do_nothing_stmt = insert_stmt.on_conflict_do_nothing()
        return_value = db.execute(do_nothing_stmt)
        if return_value and return_value.inserted_primary_key:
            meta_id = return_value.inserted_primary_key[0]
            # TODO potentially use meta_id as parent_id
            db_bridge = DocumentInstrument(
                instrument_id=meta_id,
                document_id=db_document.id,
            )
            db.add(db_bridge)

    # hazards
    for meta in document_with_metadata.hazards:
        insert_stmt = insert(Hazard).values(
            name=meta.name,
            description=meta.description,
        )
        do_nothing_stmt = insert_stmt.on_conflict_do_nothing()
        return_value = db.execute(do_nothing_stmt)
        if return_value and return_value.inserted_primary_key:
            meta_id = return_value.inserted_primary_key[0]
            db_bridge = DocumentHazard(
                hazard_id=meta_id,
                document_id=db_document.id,
            )
            db.add(db_bridge)

    # responses
    for meta in document_with_metadata.responses:
        insert_stmt = insert(Response).values(
            name=meta.name,
            description=meta.description,
        )
        do_nothing_stmt = insert_stmt.on_conflict_do_nothing()
        return_value = db.execute(do_nothing_stmt)
        if return_value and return_value.inserted_primary_key:
            meta_id = return_value.inserted_primary_key[0]
            db_bridge = DocumentResponse(
                response_id=meta_id,
                document_id=db_document.id,
            )
            db.add(db_bridge)

    # frameworks
    for meta in document_with_metadata.frameworks:
        insert_stmt = insert(Framework).values(
            name=meta.name,
            description=meta.description,
        )
        do_nothing_stmt = insert_stmt.on_conflict_do_nothing()
        return_value = db.execute(do_nothing_stmt)
        if return_value and return_value.inserted_primary_key:
            meta_id = return_value.inserted_primary_key[0]
            db_bridge = DocumentFramework(
                framework_id=meta_id,
                document_id=db_document.id,
            )
            db.add(db_bridge)
