import logging
from datetime import datetime
from typing import Sequence, Union, cast

from fastapi import (
    HTTPException,
)
from sqlalchemy import extract
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.api_v1.schemas.document import (
    DocumentAssociationCreateResponse,
    DocumentCreateRequest,
    DocumentDetailResponse,
    DocumentOverviewResponse,
)
from app.api.api_v1.schemas.metadata import (
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
from app.core.util import content_type_from_path, s3_to_cdn_url
from app.db.models import (
    Association,
    Document,
    DocumentFramework,
    DocumentHazard,
    DocumentInstrument,
    DocumentKeyword,
    DocumentLanguage,
    DocumentResponse,
    DocumentSector,
    Category,
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
    DocumentType,
)

_LOGGER = logging.getLogger(__file__)


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


class UnknownTopicError(UnknownMetadataError):
    """Error raised when a topic cannot be found in the database."""

    def __init__(self, topic: str) -> None:
        super().__init__(f"The topic '{topic}' could not be found in the database")


class UnknownFrameworkError(UnknownMetadataError):
    """Error raised when a framework cannot be found in the database."""

    def __init__(self, framework: str) -> None:
        super().__init__(
            f"The framework '{framework}' could not be found in the database"
        )


class UnknownKeywordError(UnknownMetadataError):
    """Error raised when a keyword cannot be found in the database."""

    def __init__(self, keyword: str) -> None:
        super().__init__(f"The keyword '{keyword}' could not be found in the database")


class UnknownLanguageError(UnknownMetadataError):
    """Error raised when a langauge cannot be found in the database."""

    def __init__(self, language: str) -> None:
        super().__init__(
            f"The language '{language}' could not be found in the database"
        )


class UnknownGeographyError(UnknownMetadataError):
    """Error raised when a language cannot be found in the database."""

    def __init__(self, geography: str) -> None:
        super().__init__(
            f"The geography '{geography}' could not be found in the database"
        )


class UnknownSourceError(UnknownMetadataError):
    """Error raised when a source cannot be found in the database."""

    def __init__(self, source: str) -> None:
        super().__init__(f"The source '{source}' could not be found in the database")


class UnknownDocumentTypeError(UnknownMetadataError):
    """Error raised when a document type cannot be found in the database."""

    def __init__(self, type: str) -> None:
        super().__init__(
            f"The document type '{type}' could not be found in the database"
        )


class UnknownCategoryError(UnknownMetadataError):
    """Error raised when a category cannot be found in the database."""

    def __init__(self, category: str) -> None:
        super().__init__(
            f"The category '{category}' could not be found in the database"
        )


def create_document(
    db: Session,
    document_create_request: DocumentCreateRequest,
    creator_id: int,
) -> Document:
    existing_geography_id = (
        db.query(Geography.id).filter(
            Geography.display_value == document_create_request.geography
        )
    ).scalar()
    if existing_geography_id is None:
        raise UnknownGeographyError(document_create_request.geography)

    existing_source_id = (
        db.query(Source.id).filter(Source.name == document_create_request.source)
    ).scalar()
    if existing_source_id is None:
        raise UnknownSourceError(document_create_request.source)

    existing_type_id = (
        db.query(DocumentType.id).filter(
            DocumentType.name == document_create_request.type
        )
    ).scalar()
    if existing_type_id is None:
        raise UnknownDocumentTypeError(document_create_request.type)

    existing_category_id = (
        db.query(Category.id).filter(Category.name == document_create_request.category)
    ).scalar()
    if existing_category_id is None:
        raise UnknownCategoryError(document_create_request.category)

    new_document = Document(
        name=document_create_request.name,
        description=document_create_request.description,
        source_url=document_create_request.source_url,
        created_by=creator_id,
        loaded_ts=document_create_request.loaded_ts,
        source_id=existing_source_id,
        url=document_create_request.url,
        md5_sum=document_create_request.md5_sum,
        geography_id=existing_geography_id,
        type_id=existing_type_id,
        category_id=existing_category_id,
        publication_ts=document_create_request.publication_ts,
    )
    db.add(new_document)
    db.flush()
    db.refresh(new_document)

    return new_document


def get_document_overviews(
    db: Session,
    country_code: Union[str, None] = None,
    start_year: Union[int, None] = None,
    end_year: Union[int, None] = None,
) -> Sequence[DocumentOverviewResponse]:
    """Get document overviews for matches"""
    query = (
        db.query(
            Document.id.label("document_id"),
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

    if start_year is not None:
        query = query.filter(extract("year", Document.publication_ts) >= start_year)

    if end_year is not None:
        query = query.filter(extract("year", Document.publication_ts) <= end_year)

    query = query.order_by(Document.publication_ts.desc())

    return [DocumentOverviewResponse(**dict(row)) for row in query.all()]


def get_document(db, document_id: int) -> Document:
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=404,
            detail=f"Document not found with ID {document_id}",
        )

    return document


def get_document_detail(db, document_id) -> DocumentDetailResponse:
    """Get detailed information about a document."""

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
        DocumentOverviewResponse(
            document_id=d.id,
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
            DocumentOverviewResponse(
                document_id=d.id,
                name=d.name,
                description=d.description,
                country_code=g.value,
                country_name=g.display_value,
                publication_ts=d.publication_ts,
            )
            for _, d, g in (
                db.query(Association, Document, Geography)
                .filter(Association.document_id_to == related_doc.document_id)
                .filter(Association.document_id_from != document_id)
                .join(Document, Association.document_id_from == Document.id)
                .join(Geography, Document.geography_id == Geography.id)
            ).all()
        )
    # finally find all (child) documents that refer to this document_id
    related_documents_from = set(
        DocumentOverviewResponse(
            document_id=d.id,
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


def persist_document_and_metadata(
    db: Session,
    document_create_request: DocumentCreateRequest,
    creator_id: int,
) -> DocumentDetailResponse:
    try:
        # Create a savepoint & start a transaction if necessary
        with db.begin_nested():
            new_document = create_document(db, document_create_request, creator_id)
            write_metadata(db, new_document, document_create_request)

        return get_document_detail(db, new_document.id)
    except Exception as e:
        _LOGGER.exception(f"Error saving document {document_create_request}")
        if isinstance(e, IntegrityError):
            raise HTTPException(409, detail="Document already exists")
        raise e


def write_metadata(
    db: Session,
    new_document: Document,
    document_create_request: DocumentCreateRequest,
) -> None:
    # doc languages
    for language in document_create_request.languages:
        # Lookup language by language code as a preference
        existing_language_id = (
            db.query(Language.id).filter(Language.language_code == language)
        ).scalar()
        if existing_language_id is None:
            # If the language code returned no results, attempt a lookup by name
            existing_language_id = (
                db.query(Language.id).filter(Language.name == language)
            ).scalar()
        if existing_language_id is None:
            raise UnknownLanguageError(language)

        # TODO: Need to ensure uniqueness for metadata links, especially for future
        #       update paths.
        doc_language = DocumentLanguage(
            language_id=existing_language_id,
            document_id=new_document.id,
        )
        db.add(doc_language)

    # events
    for event in document_create_request.events:
        new_event = Event(
            document_id=new_document.id,
            name=event.name,
            description=event.description,
            created_ts=event.created_ts,
        )
        db.add(new_event)

    # TODO: are source IDs really necessary on metadata? Perhaps we really do
    #       want to keep metadata limited to values from the same source as the
    #       document, but we should validate this assumption.

    # sectors
    for sector in document_create_request.sectors:
        # A sector should already exist, so fail if we cannot find it
        existing_sector_id = (
            db.query(Sector.id)
            .filter(Sector.name == sector)
            .filter(Sector.source_id == new_document.source_id)
        ).scalar()
        if existing_sector_id is None:
            raise UnknownSectorError(sector)

        doc_sector = DocumentSector(
            sector_id=existing_sector_id,
            document_id=new_document.id,
        )
        db.add(doc_sector)

    # instruments
    for instrument in document_create_request.instruments:
        # An instrument should already exist, so fail if we cannot find it
        existing_instrument_id = (
            db.query(Instrument.id)
            .filter(Instrument.name == instrument)
            .filter(Instrument.source_id == new_document.source_id)
        ).scalar()
        if existing_instrument_id is None:
            raise UnknownInstrumentError(instrument)

        doc_instrument = DocumentInstrument(
            instrument_id=existing_instrument_id,
            document_id=new_document.id,
        )
        db.add(doc_instrument)

    # hazards
    for hazard in document_create_request.hazards:
        # A hazard should already exist, so fail if we cannot find it
        existing_hazard_id = (
            db.query(Hazard.id).filter(Hazard.name == hazard)
        ).scalar()
        if existing_hazard_id is None:
            raise UnknownHazardError(hazard)

        doc_hazard = DocumentHazard(
            hazard_id=existing_hazard_id,
            document_id=new_document.id,
        )
        db.add(doc_hazard)

    # responses/topics
    for topic in document_create_request.topics:
        # A response should already exist, so fail if we cannot find it
        existing_response_id = (
            db.query(Response.id).filter(Response.name == topic)
        ).scalar()
        if existing_response_id is None:
            raise UnknownTopicError(topic)

        doc_response = DocumentResponse(
            response_id=existing_response_id,
            document_id=new_document.id,
        )
        db.add(doc_response)

    # frameworks
    for framework in document_create_request.frameworks:
        # A framework should already exist, so fail if we cannot find it
        existing_framework_id = (
            db.query(Framework.id).filter(Framework.name == framework)
        ).scalar()
        if existing_framework_id is None:
            raise UnknownFrameworkError(framework)

        doc_framework = DocumentFramework(
            framework_id=existing_framework_id,
            document_id=new_document.id,
        )
        db.add(doc_framework)

    # keywords
    for keyword in document_create_request.keywords:
        # A keyword should already exist, so fail if we cannot find it
        existing_keyword_id = (
            db.query(Keyword.id).filter(Keyword.name == keyword)
        ).scalar()
        if existing_keyword_id is None:
            raise UnknownKeywordError(keyword)

        doc_keyword = DocumentKeyword(
            keyword_id=existing_keyword_id,
            document_id=new_document.id,
        )
        db.add(doc_keyword)


def create_document_association(
    db: Session,
    document_id_from: int,
    document_id_to: int,
    name: str,
    type: str,
) -> DocumentAssociationCreateResponse:
    new_association = Association(
        document_id_from=document_id_from,
        document_id_to=document_id_to,
        name=name,
        type=type,
    )
    db.add(new_association)
    db.commit()

    return DocumentAssociationCreateResponse.from_orm(new_association)
