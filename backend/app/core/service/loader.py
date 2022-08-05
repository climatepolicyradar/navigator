import logging

from fastapi import (
    HTTPException,
)
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


class UnknownMetadataError(Exception):
    """Base class for metadata lookup errors."""

    pass


class UnknownSectorError(UnknownMetadataError):
    """Error raised when a sector cannot be found in the database."""

    def __init__(self, sector: str) -> None:
        super().__init__(f"The sector '{sector}' could not be found in the database")


class UnknownInstrumentError(UnknownMetadataError):
    """Error raised when an instrument cannot be found in the database."""

    def __init__(self, instrument: str) -> None:
        super().__init__(
            f"The instrument '{instrument}' could not be found in the database"
        )


class UnknownHazardError(UnknownMetadataError):
    """Error raised when a hazard cannot be found in the database."""

    def __init__(self, hazard: str) -> None:
        super().__init__(f"The hazard '{hazard}' could not be found in the database")


class UnknownResponseError(UnknownMetadataError):
    """Error raised when a response cannot be found in the database."""

    def __init__(self, response: str) -> None:
        super().__init__(
            f"The response '{response}' could not be found in the database"
        )


class UnknownFrameworkError(UnknownMetadataError):
    """Error raised when a framework cannot be found in the database."""

    def __init__(self, framework: str) -> None:
        super().__init__(
            f"The framework '{framework}' could not be found in the database"
        )


class UnknownKeywordError(UnknownMetadataError):
    """Error raised when a keyword cannot be found in the database."""

    def __init__(self, keyword: str) -> None:
        super().__init__(f"The  '{keyword}' could not be found in the database")


def persist_document_and_metadata(
    db: Session,
    document_with_metadata: DocumentCreateWithMetadata,
    creator_id: int,
):
    try:
        # Create a savepoint & start a transaction if necessary
        with db.begin_nested():
            db_document = create_document(
                db, document_with_metadata.document, creator_id
            )
            write_metadata(db, db_document, document_with_metadata)

        return db_document
    except Exception as e:
        logger.error(
            f"Error saving document {document_with_metadata.document}", exc_info=e
        )
        if isinstance(e, IntegrityError):
            raise HTTPException(409, detail="Document already exists")
        raise e


def write_metadata(
    db,
    db_document: Document,
    document_with_metadata: DocumentCreateWithMetadata,
):
    # doc language
    for language_id in document_with_metadata.language_ids:
        doc_language = DocumentLanguage(
            language_id=language_id,
            document_id=db_document.id,
        )
        db.add(doc_language)

    # events
    for event in document_with_metadata.events:
        db_event = Event(
            document_id=db_document.id,
            name=event.name,
            description=event.description,
            created_ts=event.created_ts,
        )
        db.add(db_event)

    # TODO: are source IDs really necessary on metadata? Perhaps we really do
    #       want to keep metadata limited to values from the same source as the
    #       document, but we should validate this assumption.

    # sectors
    for sector in document_with_metadata.sectors:
        # A sector should already exist, so fail if we cannot find it
        existing_sector = (
            db.query(Sector)
            .filter(Sector.name == sector.name)
            .filter(Sector.source_id == db_document.source_id)
        ).first()
        if existing_sector is None:
            raise UnknownSectorError(sector.name)

        sector_id = existing_sector.id  # type: ignore
        doc_sector = DocumentSector(
            sector_id=sector_id,
            document_id=db_document.id,
        )
        db.add(doc_sector)

    # instruments
    for instrument in document_with_metadata.instruments:
        # An instrument should already exist, so fail if we cannot find it
        existing_instrument = (
            db.query(Instrument)
            .filter(Instrument.name == instrument.name)
            .filter(Instrument.source_id == db_document.source_id)
        ).first()
        if existing_instrument is None:
            raise UnknownInstrumentError(instrument.name)

        instrument_id = existing_instrument.id  # type: ignore
        doc_instrument = DocumentInstrument(
            instrument_id=instrument_id,
            document_id=db_document.id,
        )
        db.add(doc_instrument)

    # hazards
    for hazard in document_with_metadata.hazards:
        # A hazard should already exist, so fail if we cannot find it
        existing_hazard = (db.query(Hazard).filter(Hazard.name == hazard.name)).first()
        if existing_hazard is None:
            raise UnknownHazardError(hazard.name)

        hazard_id = existing_hazard.id  # type: ignore
        doc_hazard = DocumentHazard(
            hazard_id=hazard_id,
            document_id=db_document.id,
        )
        db.add(doc_hazard)

    # responses
    for response in document_with_metadata.responses:
        # A response should already exist, so fail if we cannot find it
        existing_response = (
            db.query(Response).filter(Response.name == response.name)
        ).first()
        if existing_response is None:
            raise UnknownResponseError(response.name)

        response_id = existing_response.id  # type: ignore
        doc_response = DocumentResponse(
            response_id=response_id,
            document_id=db_document.id,
        )
        db.add(doc_response)

    # frameworks
    for framework in document_with_metadata.frameworks:
        # A framework should already exist, so fail if we cannot find it
        existing_framework = (
            db.query(Framework).filter(Framework.name == framework.name)
        ).first()
        if existing_framework is None:
            raise UnknownFrameworkError(framework.name)

        framework_id = existing_framework.id  # type: ignore
        doc_framework = DocumentFramework(
            framework_id=framework_id,
            document_id=db_document.id,
        )
        db.add(doc_framework)

    # keywords
    for keyword in document_with_metadata.keywords:
        # A keyword should already exist, so fail if we cannot find it
        existing_keyword = (
            db.query(Keyword).filter(Keyword.name == keyword.name)
        ).first()
        if existing_keyword is None:
            raise UnknownKeywordError(keyword.name)

        keyword_id = existing_keyword.id  # type: ignore
        doc_keyword = DocumentKeyword(
            keyword_id=keyword_id,
            document_id=db_document.id,
        )
        db.add(doc_keyword)
