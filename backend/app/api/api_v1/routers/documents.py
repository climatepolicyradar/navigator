import logging
import os
from datetime import datetime
from http.client import (
    INTERNAL_SERVER_ERROR,
    UNPROCESSABLE_ENTITY,
    UNSUPPORTED_MEDIA_TYPE,
)
from pathlib import Path
from typing import List, Mapping, Union, cast

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Request,
    UploadFile,
)

from app.core.auth import (
    get_current_active_superuser,
    get_current_active_user,
    get_current_active_db_superuser,
)
from app.core.aws import get_s3_client
from app.core.service.loader import UnknownMetadataError, persist_document_and_metadata
from app.core.util import CONTENT_TYPE_MAP, content_type_from_path, s3_to_cdn_url
from app.db.models import (
    Association,
    Category,
    Document,
    DocumentFramework,
    DocumentHazard,
    DocumentInstrument,
    DocumentKeyword,
    DocumentLanguage,
    DocumentResponse,
    DocumentSector,
    DocumentType,
    Event,
    Framework,
    Geography,
    Hazard,
    Instrument,
    Keyword,
    Language,
    Response,
    Sector,
    Source,
)
from app.db.schemas.document import (
    DocumentCreateWithMetadata,
    DocumentInDB,
    DocumentDetailResponse,
    DocumentBrowseResponse,
    RelatedDocumentResponse,
    DocumentAssociationInDB,
    DocumentAssociation,
)
from app.db.schemas.metadata import (
    Category as CategorySchema,
    DocumentType as DocumentTypeSchema,
    Event as EventSchema,
    Framework as FrameworkSchema,
    Geography as GeographySchema,
    Hazard as HazardSchema,
    Instrument as InstrumentSchema,
    Keyword as KeywordSchema,
    Language as LanguageSchema,
    Sector as SectorSchema,
    Source as SourceSchema,
    Topic as TopicSchema,
)
from app.db.session import get_db

_LOGGER = logging.getLogger(__file__)

documents_router = APIRouter()


document_respoonses: Mapping[int, Mapping] = {
    404: {"description": "Cannot find a document that matches the filter criteria."}
}

documents_router.add_api_route


@documents_router.get(
    "/documents",
    response_model=List[DocumentBrowseResponse],
    summary="Get a list of documents",
    responses=document_respoonses,
)
async def document_browse(
    country_code: Union[str, None] = None,
    q: Union[str, None] = None,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Filter all documents"""
    query = (
        db.query(
            Document.name,
            Document.description,
            Document.publication_ts,
            Geography.display_value.label("country_name"),
            Geography.value.label("country_code"),
        )
        .join(Geography, Document.geography_id == Geography.id)
        .join(DocumentType, Document.type_id == DocumentType.id)
    )

    if country_code is not None:
        query = query.filter(Geography.value == country_code)

    def row_to_response(row):
        return DocumentBrowseResponse(
            name=row["name"],
            description=row["description"],
            country_code=row["country_code"],
            country_name=row["country_name"],
            publication_ts=row["publication_ts"],
        )

    found = query.all()

    return [*map(row_to_response, found)]


@documents_router.get(
    "/documents/{document_id}",
    response_model=DocumentDetailResponse,
    response_model_exclude_none=True,
)
async def get_document_detail(
    document_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Get details of the document with the given ID."""

    document_data = (
        db.query(Document, Geography, DocumentType, Category, Source)
        .filter(Document.id == document_id)
        .filter(Document.geography_id == Geography.id)
        .filter(Document.type_id == DocumentType.id)
        .filter(Document.category_id == Category.id)
        .filter(Document.source_id == Source.id)
    )
    if document_data.count() < 1:
        raise HTTPException(404, f"Document with id {document_id} could not be found.")
    if document_data.count() > 1:
        raise HTTPException(
            500, f"Query returned multiple results for id {document_id}"
        )

    # Retrieve all events associated with this document
    events = db.query(Event).filter(Event.document_id == document_id).all()
    events = sorted(events, key=lambda e: e.created_ts)

    # Retrieve all metadata associated with this document via join tables
    languages = (
        db.query(DocumentLanguage, Language)
        .filter(DocumentLanguage.document_id == document_id)
        .join(Language)
    ).all()
    sectors = (
        db.query(DocumentSector, Sector, Source)
        .filter(DocumentSector.document_id == document_id)
        .join(Sector, DocumentSector.sector_id == Sector.id)
        .join(Source, Sector.source_id == Source.id)
    ).all()
    instruments = (
        db.query(DocumentInstrument, Instrument, Source)
        .filter(DocumentInstrument.document_id == document_id)
        .join(Instrument, DocumentInstrument.instrument_id == Instrument.id)
        .join(Source, Instrument.source_id == Source.id)
    ).all()
    frameworks = (
        db.query(DocumentFramework, Framework)
        .filter(DocumentFramework.document_id == document_id)
        .join(Framework)
    ).all()
    responses = (
        db.query(DocumentResponse, Response)
        .filter(DocumentResponse.document_id == document_id)
        .join(Response)
    ).all()
    hazards = (
        db.query(DocumentHazard, Hazard)
        .filter(DocumentHazard.document_id == document_id)
        .join(Hazard)
    ).all()
    keywords = (
        db.query(DocumentKeyword, Keyword)
        .filter(DocumentKeyword.document_id == document_id)
        .join(Keyword)
    ).all()

    # Get all associated documents
    # start with all documents with a reference from this document_id
    related_documents_to = set(
        RelatedDocumentResponse(
            related_id=d.id,
            name=d.name,
            description=d.description,
            country_code=g.value,
            country_name=g.display_value,
            publication_ts=d.publication_ts,
        )
        for _, d, g in (
            db.query(Association, Document, Geography)
            .filter(Association.document_id_from == document_id)
            .join(Document, Association.document_id_to == Document.id)
            .join(Geography, Document.geography_id == Geography.id)
        ).all()
    )
    # if the above query has results, it contains a "master doc" for a group,
    # so collect all children
    related_to_master_documents = set()
    # for alpha this list should have at most one entry
    for related_doc in related_documents_to:
        related_to_master_documents |= set(
            RelatedDocumentResponse(
                related_id=d.id,
                name=d.name,
                description=d.description,
                country_code=g.value,
                country_name=g.display_value,
                publication_ts=d.publication_ts,
            )
            for _, d, g in (
                db.query(Association, Document, Geography)
                .filter(Association.document_id_to == related_doc.related_id)
                .filter(Association.document_id_from != document_id)
                .join(Document, Association.document_id_from == Document.id)
                .join(Geography, Document.geography_id == Geography.id)
            ).all()
        )
    # finally find all (child) documents that refer to this document_id
    related_documents_from = set(
        RelatedDocumentResponse(
            related_id=d.id,
            name=d.name,
            description=d.description,
            country_code=g.value,
            country_name=g.display_value,
            publication_ts=d.publication_ts,
        )
        for _, d, g in (
            db.query(Association, Document, Geography)
            .filter(Association.document_id_to == document_id)
            .join(Document, Association.document_id_from == Document.id)
            .join(Geography, Document.geography_id == Geography.id)
        ).all()
    )
    related_docs = (
        related_documents_to | related_to_master_documents | related_documents_from
    )

    # Now build the required response object
    document, geography, doc_type, category, source = document_data.first()
    return DocumentDetailResponse(
        id=document_id,
        loaded_ts=cast(datetime, document.loaded_ts),
        name=cast(str, document.name),
        description=cast(str, document.description),
        publication_ts=document.publication_ts,
        source_url=cast(str, document.source_url),
        url=s3_to_cdn_url(document.url),
        # TODO: replace with proper content type handling
        content_type=content_type_from_path(document.url),
        geography=GeographySchema(
            display_value=cast(str, geography.display_value),
            value=cast(str, geography.value),
            type=cast(str, geography.type),
        ),
        type=DocumentTypeSchema(
            name=cast(str, doc_type.name),
            description=cast(str, doc_type.description),
        ),
        category=CategorySchema(
            name=cast(str, category.name),
            description=cast(str, category.description),
        ),
        source=SourceSchema(
            name=cast(str, source.name),
        ),
        languages=[
            LanguageSchema(
                language_code=l.language_code,
                part1_code=l.part1_code,
                part2_code=l.part2_code,
                name=l.name,
            )
            for _, l in languages
        ],
        events=[
            EventSchema(name=e.name, description=e.description, created_ts=e.created_ts)
            for e in events
        ],
        frameworks=[
            FrameworkSchema(name=f.name, description=f.description)
            for _, f in frameworks
        ],
        hazards=[
            HazardSchema(name=h.name, description=h.description) for _, h in hazards
        ],
        instruments=[
            InstrumentSchema(
                name=i.name, description=i.description, source=SourceSchema(name=s.name)
            )
            for _, i, s in instruments
        ],
        keywords=[
            KeywordSchema(name=k.name, description=k.description) for _, k in keywords
        ],
        sectors=[
            SectorSchema(
                name=s.name,
                description=s.description,
                source=SourceSchema(name=src.name),
            )
            for _, s, src in sectors
        ],
        topics=[
            TopicSchema(name=t.name, description=t.description) for _, t in responses
        ],
        related_documents=list(related_docs),
    )


@documents_router.post("/documents", response_model=DocumentInDB)
async def post_document(
    request: Request,
    document_with_metadata: DocumentCreateWithMetadata,
    db=Depends(get_db),
    current_user=Depends(get_current_active_db_superuser),
):
    """Create a document, with associated metadata."""

    try:
        db_document = persist_document_and_metadata(
            db, document_with_metadata, current_user.id
        )
    except UnknownMetadataError as e:
        _LOGGER.exception(f"Could not create document for {document_with_metadata}")
        raise HTTPException(
            UNPROCESSABLE_ENTITY, f"Creating the requested document failed: {str(e)}"
        )

    return DocumentInDB.from_orm(db_document)


@documents_router.post(
    "/document",
)
def document_upload(
    request: Request,
    file: UploadFile = File(...),
    current_user=Depends(get_current_active_superuser),
    s3_client=Depends(get_s3_client),
):
    """Upload a document to the queue bucket."""
    bucket = os.environ.get("DOCUMENT_BUCKET", "cpr-document-queue")
    _LOGGER.info(f"Attempting to upload {file.filename} to {bucket}")

    file_path = Path(file.filename)

    # TODO: proper content-type validation
    if file_path.suffix.lower() not in CONTENT_TYPE_MAP:
        raise HTTPException(
            UNSUPPORTED_MEDIA_TYPE, "Unsupported Media Type: must be PDF or HTML."
        )

    try:
        s3_document = s3_client.upload_fileobj(
            fileobj=file.file,
            bucket=bucket,
            key=str(file_path),
            content_type=file.content_type,
        )
    except Exception:
        raise HTTPException(
            INTERNAL_SERVER_ERROR,
            "Internal Server Error: upload error.",
        )

    # If the above function returns False, then the upload has failed.
    if not s3_document:
        raise HTTPException(
            INTERNAL_SERVER_ERROR,
            "Internal Server Error: upload failed.",
        )

    _LOGGER.info(f"Document uploaded to cloud at {s3_document.url}")
    return {
        "url": s3_document.url,
    }


@documents_router.post("/associations", response_model=DocumentAssociationInDB)
async def post_association(
    request: Request,
    document_association: DocumentAssociation,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """Create a document, with associated metadata."""

    db_association = Association(
        document_id_from=document_association.document_id_from,
        document_id_to=document_association.document_id_to,
        name=document_association.name,
        type=document_association.type,
    )
    db.add(db_association)
    db.commit()

    return DocumentAssociationInDB.from_orm(db_association)
