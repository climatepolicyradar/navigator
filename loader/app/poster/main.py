import logging

from sqlalchemy.orm import Session

from app.db.models import (
    Document,
    APIDocument,
    Event,
    Instrument,
    DocumentInstrument,
    Sector,
    DocumentSector,
    Framework,
    DocumentFramework,
    Response,
    DocumentResponse,
    Hazard,
    DocumentHazard,
)
from app.service.api_client import post_document

logger = logging.getLogger(__file__)


def post_all_to_backend_api(db: Session):
    """Posts everything in the local database to the remote backend API."""
    debug_count = 0
    for doc in db.query(Document).all():
        debug_count += 1
        if debug_count > 10:
            print("done for testing purposes")
            break
        # optimisation: check if we've uploaded already
        # read from api_document
        try:
            response = post_doc(db, doc)
            if "id" in response:
                remote_document_id = response["id"]
                apidoc = APIDocument(
                    document_id=doc.id,
                    remote_document_id=remote_document_id,
                )
                db.add(apidoc)
                db.commit()
                logger.info(
                    f"Document uploaded to API, doc.id={doc.id}, remote doc.id={remote_document_id}"
                )
            else:
                detail = response["detail"]
                logger.warning(
                    f"Document could not be posted to API, doc.id={doc.id}, error={detail}"
                )
        except Exception as e:
            logger.error(
                f"Document could not be posted to API, doc.id={doc.id}", exc_info=e
            )


def post_doc(db: Session, doc: Document) -> dict:
    """Post a doc to the API backend.

    Also fetches related metadata, and posts that too.

    TODO: optimise, as the queries are currently being run separately.
    """

    # get all metadata associated with this doc, and post it too
    events = db.query(Event).filter(Event.document_id == doc.id).all()
    sectors = (
        db.query(Sector)
        .join(DocumentSector)
        .filter(
            (Sector.id == DocumentSector.sector_id)
            & (DocumentSector.document_id == doc.id)
        )
        .all()
    )
    instruments = (
        db.query(Instrument)
        .join(DocumentInstrument)
        .filter(
            (Instrument.id == DocumentInstrument.instrument_id)
            & (DocumentInstrument.document_id == doc.id)
        )
        .all()
    )
    frameworks = (
        db.query(Framework)
        .join(DocumentFramework)
        .filter(
            (Framework.id == DocumentFramework.framework_id)
            & (DocumentFramework.document_id == doc.id)
        )
        .all()
    )
    responses = (
        db.query(Response)
        .join(DocumentResponse)
        .filter(
            (Response.id == DocumentResponse.response_id)
            & (DocumentResponse.document_id == doc.id)
        )
        .all()
    )
    hazards = (
        db.query(Hazard)
        .join(DocumentHazard)
        .filter(
            (Hazard.id == DocumentHazard.hazard_id)
            & (DocumentHazard.document_id == doc.id)
        )
        .all()
    )

    payload = {
        "document": {
            "loaded_ts": doc.loaded_ts.isoformat(),
            "name": doc.name,
            "source_url": doc.source_url,
            "url": doc.url,
            "type_id": doc.type_id,  # this is from backend API lookup, so will exist remotely.
        },
        "source_id": doc.source_id,
        "events": [it.name for it in events],
        "sectors": [it.name for it in sectors],
        "instruments": [it.name for it in instruments],
        "frameworks": [it.name for it in frameworks],
        "responses": [it.name for it in responses],
        "hazards": [it.name for it in hazards],
        # "language_codes": [],  # TODO
    }
    response = post_document(payload)
    return response.json()
