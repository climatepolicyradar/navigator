from sqlalchemy.orm import Session

from app.db.models import (
    Document,
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
    DocumentLanguage,
    Keyword,
    DocumentKeyword,
)
from app.service.api_client import post_document


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
    keywords = (
        db.query(Keyword)
        .join(DocumentKeyword)
        .filter(
            (Keyword.id == DocumentKeyword.keyword_id)
            & (DocumentKeyword.document_id == doc.id)
        )
        .all()
    )
    document_languages = (
        db.query(DocumentLanguage).filter(DocumentLanguage.document_id == doc.id).all()
    )

    payload = {
        "document": {
            "loaded_ts": doc.loaded_ts.isoformat(),
            "name": doc.name,
            "description": doc.description,
            "source_url": doc.source_url,
            "url": doc.url or "",
            "md5_sum": doc.md5_sum or "",
            "type_id": doc.type_id,  # this is from backend API lookup, so will exist remotely.
            "source_id": doc.source_id,
            "geography_id": doc.geography_id,  # this is from backend API lookup, so will exist remotely.
            "category_id": doc.category_id,  # this is from backend API lookup, so will exist remotely.
            "publication_ts": doc.publication_ts.isoformat(),
        },
        "source_id": doc.source_id,
        "events": [it.as_dict() for it in events],
        "sectors": [it.as_dict() for it in sectors],
        "instruments": [it.as_dict() for it in instruments],
        "frameworks": [it.as_dict() for it in frameworks],
        "responses": [it.as_dict() for it in responses],
        "hazards": [it.as_dict() for it in hazards],
        "keywords": [it.as_dict() for it in keywords],
        "language_ids": [it.language_id for it in document_languages],
    }

    response = post_document(payload)
    return response.json()
