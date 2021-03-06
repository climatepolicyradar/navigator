import logging

from fastapi import (
    HTTPException,
)
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.crud.document import create_document
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
    DocumentLanguage,
    Keyword,
    DocumentKeyword,
)
from app.db.schemas.document import DocumentCreateWithMetadata

logger = logging.getLogger(__file__)


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
        logger.error(
            f"Error saving document {document_with_metadata.document}", exc_info=e
        )
        if isinstance(e, IntegrityError):
            raise HTTPException(409, detail="Document already exists")
        raise e


def write_metadata(
    db: Session,
    db_document: Document,
    document_with_metadata: DocumentCreateWithMetadata,
):
    # doc language
    for language_id in document_with_metadata.language_ids:
        db_doc_lang = DocumentLanguage(
            language_id=language_id,
            document_id=db_document.id,
        )
        db.add(db_doc_lang)

    # events
    for event in document_with_metadata.events:
        db_event = Event(
            document_id=db_document.id,
            name=event.name,
            description=event.description,
            created_ts=event.created_ts,
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
        else:
            # This is guaranteed to exist
            existing_sector = (
                db.query(Sector)
                .filter(Sector.name == meta.name)
                .filter(Sector.source_id == db_document.source_id)
            ).first()
            meta_id = existing_sector.id  # type: ignore

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
        else:
            # This is guaranteed to exist
            existing_instrument = (
                db.query(Instrument)
                .filter(Instrument.name == meta.name)
                .filter(Instrument.source_id == db_document.source_id)
            ).first()
            meta_id = existing_instrument.id  # type: ignore

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
        else:
            # This is guaranteed to exist
            existing_hazard = (
                db.query(Hazard).filter(Hazard.name == meta.name)
            ).first()
            meta_id = existing_hazard.id  # type: ignore

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
        else:
            # This is guaranteed to exist
            existing_sector = (
                db.query(Response).filter(Response.name == meta.name)
            ).first()
            meta_id = existing_sector.id  # type: ignore

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
        else:
            # This is guaranteed to exist
            existing_framework = (
                db.query(Framework).filter(Framework.name == meta.name)
            ).first()
            meta_id = existing_framework.id  # type: ignore

        db_bridge = DocumentFramework(
            framework_id=meta_id,
            document_id=db_document.id,
        )
        db.add(db_bridge)

    for meta in document_with_metadata.keywords:
        insert_stmt = insert(Keyword).values(
            name=meta.name,
            description=meta.description,
        )
        do_nothing_stmt = insert_stmt.on_conflict_do_nothing()
        return_value = db.execute(do_nothing_stmt)
        if return_value and return_value.inserted_primary_key:
            meta_id = return_value.inserted_primary_key[0]
        else:
            # This is guaranteed to exist
            existing_keyword = (
                db.query(Keyword).filter(Keyword.name == meta.name)
            ).first()
            meta_id = existing_keyword.id  # type: ignore

        db_bridge = DocumentKeyword(
            keyword_id=meta_id,
            document_id=db_document.id,
        )
        db.add(db_bridge)
