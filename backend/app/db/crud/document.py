import logging
from hashlib import md5
from typing import Mapping, Sequence, Set, Tuple, Union, cast

from fastapi import (
    HTTPException,
)
from slugify import slugify
from sqlalchemy import extract
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.api_v1.schemas.document import (
    DocumentCreateRequest,
    DocumentDetailResponse,
    DocumentOverviewResponse,
    DocumentParserInput,
    RelationshipEntityResponse,
    RelationshipGetResponse,
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
from app.core.aws import S3Client
from app.core.util import to_cdn_url
from app.core.validation import IMPORT_ID_MATCHER
from app.core.validation.util import write_documents_to_s3
from app.db.models import (
    Document,
    DocumentFramework,
    DocumentHazard,
    DocumentInstrument,
    DocumentKeyword,
    DocumentLanguage,
    DocumentRelationship,
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
    Relationship,
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
    """Error raised when a language cannot be found in the database."""

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


def _create_document_slug(
    document_create_request: DocumentCreateRequest,
    geography: Geography,
) -> str:
    return "_".join(
        [
            slugify(f"{geography.display_value}", separator="-"),
            f"{document_create_request.publication_ts.year}",
            # no science here, just limit the slug to a reasonable length
            slugify(document_create_request.name, separator="-")[:768],
        ]
        + slugify(document_create_request.import_id).split("-")[-2:]
    )


def _write_metadata(
    db: Session,
    new_document: Document,
    document_create_request: DocumentCreateRequest,
) -> None:
    # doc languages
    for language in document_create_request.languages:
        existing_language = _get_language_by_code_or_name(db, language)

        # TODO: Need to ensure uniqueness for metadata links, especially for future
        #       update paths.
        doc_language = DocumentLanguage(
            language_id=existing_language.id,
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


def create_document(
    db: Session,
    document_create_request: DocumentCreateRequest,
) -> Document:
    with db.begin_nested():
        existing_geography = _get_geography_by_slug_or_display_or_value(
            db,
            document_create_request.geography,
        )

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
            db.query(Category.id).filter(
                Category.name == document_create_request.category
            )
        ).scalar()
        if existing_category_id is None:
            raise UnknownCategoryError(document_create_request.category)

        document_slug = _create_document_slug(
            document_create_request,
            geography=existing_geography,
        )

        new_document = Document(
            name=document_create_request.name,
            description=document_create_request.description,
            source_url=document_create_request.source_url,
            source_id=existing_source_id,
            slug=document_slug,
            url=None,  # Added by processing pipeline
            md5_sum=None,  # Added by processing pipeline
            cdn_object=None,  # Added by processing pipeline
            import_id=document_create_request.import_id,
            geography_id=existing_geography.id,
            type_id=existing_type_id,
            category_id=existing_category_id,
            publication_ts=document_create_request.publication_ts,
            postfix=document_create_request.postfix,
        )
        db.add(new_document)
        db.flush()
        db.refresh(new_document)

        _write_metadata(
            db=db,
            new_document=new_document,
            document_create_request=document_create_request,
        )
        _LOGGER.info(f"Created Metadata: {document_create_request.import_id}")

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
            Document.import_id,
            Document.slug,
            Document.name,
            Document.postfix,
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


def get_document_ids(db: Session) -> Tuple[str, Sequence[str]]:
    """Returns hash of and the entire list of document ids

    Args:
        db (Session): Database connection

    Returns:
        Tuple[str, Sequence[str]]: Tuple of the hash and the id list
    """
    # This query is ordered so that the return is deterministic
    query = db.query(Document.id).order_by(Document.publication_ts.desc())

    id_list = [str(row[0]) for row in query.all()]
    hash = md5("".join(id_list).encode()).hexdigest()
    return (hash, id_list)


def get_document(db, document_id: int) -> Document:
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=404,
            detail=f"Document not found with ID {document_id}",
        )

    return document


def get_document_detail(db, import_id_or_slug) -> DocumentDetailResponse:
    """Get detailed information about a document."""

    document_data = (
        db.query(Document, Geography, DocumentType, Category, Source)
        .filter(Document.geography_id == Geography.id)
        .filter(Document.type_id == DocumentType.id)
        .filter(Document.category_id == Category.id)
        .filter(Document.source_id == Source.id)
    )

    # Determine if slug or id
    if IMPORT_ID_MATCHER.match(import_id_or_slug) is not None:
        document_data = document_data.filter(Document.import_id == import_id_or_slug)
    else:
        document_data = document_data.filter(Document.slug == import_id_or_slug)

    if document_data.count() < 1:
        raise HTTPException(
            404, f"Document with id {import_id_or_slug} could not be found."
        )
    if document_data.count() > 1:
        raise HTTPException(
            500, f"Query returned multiple results for id {import_id_or_slug}"
        )

    document_id = document_data.first()[0].id
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

    related_docs = _get_related_documents(db, document_id)

    # Now build the required response object
    document, geography, doc_type, category, source = document_data.first()

    return DocumentDetailResponse(
        id=document_id,
        name=cast(str, document.name),
        description=cast(str, document.description),
        publication_ts=document.publication_ts,
        postfix=document.postfix,
        source_url=document.source_url,
        url=to_cdn_url(document.cdn_object),
        slug=document.slug,
        import_id=document.import_id,
        content_type=document.content_type or "unknown",
        md5_sum=document.md5_sum,
        geography=GeographySchema(
            display_value=cast(str, geography.display_value),
            slug=cast(str, geography.slug),
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


def _get_geography_by_slug_or_display_or_value(
    db: Session,
    display_or_value_or_slug: str,
) -> Geography:
    # Lookup geography by display_value or value
    existing_geography = (
        db.query(Geography).filter(Geography.slug == display_or_value_or_slug)
    ).first()
    if existing_geography is None:
        # If the slug returned no results, attempt a lookup by display_value
        existing_geography = (
            db.query(Geography).filter(
                Geography.display_value == display_or_value_or_slug
            )
        ).first()
    if existing_geography is None:
        # If the slug and display_value returned no results, attempt a lookup by value
        # (this is the least reliable and not guaranteed to be unique)
        existing_geography = (
            db.query(Geography).filter(Geography.value == display_or_value_or_slug)
        ).first()
    if existing_geography is None:
        raise UnknownGeographyError(display_or_value_or_slug)
    return existing_geography


def _get_language_by_code_or_name(db: Session, code_or_name: str) -> Language:
    # Lookup language by language_code as a preference
    existing_language = (
        db.query(Language).filter(Language.language_code == code_or_name)
    ).first()
    if existing_language is None:
        # If the language_code returned no results, attempt a lookup by name
        # (this is the least reliable and not guaranteed to be unique)
        existing_language = (
            db.query(Language).filter(Language.name == code_or_name)
        ).first()
    if existing_language is None:
        raise UnknownLanguageError(code_or_name)
    return existing_language


def start_import(
    db: Session,
    s3_client: S3Client,
    document_create_objects: Sequence[DocumentCreateRequest],
):
    document_parser_inputs: list[DocumentParserInput] = []
    try:
        # Create a savepoint & start a transaction if necessary
        with db.begin_nested():
            for dco in document_create_objects:
                _LOGGER.info(f"Importing: {dco.import_id}")
                existing_document = (
                    db.query(Document)
                    .filter(Document.import_id == dco.import_id)
                    .scalar()
                )
                if existing_document is None:
                    new_document = create_document(db, dco)
                    _LOGGER.info(f"Created Document: {dco.import_id}")

                    document_parser_inputs.append(
                        DocumentParserInput(
                            slug=cast(str, new_document.slug),
                            **dco.dict(),
                        )
                    )

        # This commit is necessary after completing the nested transaction
        _LOGGER.info("Importing performing final commit.")
        db.commit()
    except Exception as e:
        _LOGGER.exception("Unexpected error creating document entries")
        if isinstance(e, IntegrityError):
            raise HTTPException(409, detail="Document already exists")
        raise e

    write_documents_to_s3(s3_client=s3_client, documents=document_parser_inputs)


def _get_related_documents(
    db: Session, document_id: int
) -> Set[DocumentOverviewResponse]:
    """Gets all the other documents this document is related to."""
    query_all_relationships_of_document = db.query(
        DocumentRelationship.relationship_id
    ).filter(DocumentRelationship.document_id == document_id)

    return set(
        DocumentOverviewResponse(
            document_id=d.id,
            name=d.name,
            postfix=d.postfix,
            import_id=d.import_id,
            slug=d.slug,
            description=d.description,
            country_code=g.value,
            country_name=g.display_value,
            publication_ts=d.publication_ts,
        )
        for _, d, g in (
            db.query(DocumentRelationship, Document, Geography)
            .join(Geography, Document.geography_id == Geography.id)
            .join(DocumentRelationship, DocumentRelationship.document_id == Document.id)
            .filter(
                DocumentRelationship.relationship_id.in_(
                    query_all_relationships_of_document
                )
            )
            .filter(Document.id != document_id)
        ).all()
    )


def create_relationship(
    db: Session,
    name: str,
    type: str,
    description: str,
) -> RelationshipEntityResponse:
    new_rel = Relationship(name=name, type=type, description=description)
    db.add(new_rel)
    db.commit()

    return RelationshipEntityResponse.from_orm(new_rel)


def get_relationships(db: Session) -> RelationshipGetResponse:
    return RelationshipGetResponse(
        relationships=[
            RelationshipEntityResponse.from_orm(r) for r in db.query(Relationship).all()
        ]
    )


def get_relationship_by_id(
    db: Session, relationship_id: int
) -> RelationshipEntityResponse:
    return RelationshipEntityResponse.from_orm(
        db.query(Relationship).get(relationship_id)
    )


def get_documents_in_relationship(db: Session, relationship_id: int):
    """Gets all the other documents this document is related to.

    TODO: return this as structured, as at the moment we return a flat list
    """

    return list(
        DocumentOverviewResponse(
            document_id=d.id,
            name=d.name,
            postfix=d.postfix,
            import_id=d.import_id,
            slug=d.slug,
            description=d.description,
            country_code=g.value,
            country_name=g.display_value,
            publication_ts=d.publication_ts,
        )
        for _, d, g in (
            db.query(DocumentRelationship, Document, Geography)
            .join(Geography, Document.geography_id == Geography.id)
            .join(DocumentRelationship, DocumentRelationship.document_id == Document.id)
            .filter(DocumentRelationship.relationship_id == relationship_id)
        ).all()
    )


def create_document_relationship(
    db: Session, document_id: int, relationship_id: int
) -> None:
    new_doc_rel = DocumentRelationship(
        document_id=document_id, relationship_id=relationship_id
    )
    try:
        with db.begin_nested():
            db.add(new_doc_rel)

        # The call to db.commit() must exist outside the nested transaction
        db.commit()
    except IntegrityError:
        # ensure its idempotent
        raise HTTPException(
            200, detail="Document-Relationship already exists - Nothing to do"
        )


def remove_document_relationship(
    db: Session, document_id: int, relationship_id: int
) -> None:
    obj = (
        db.query(DocumentRelationship)
        .filter(DocumentRelationship.document_id == document_id)
        .filter(DocumentRelationship.relationship_id == relationship_id)
        .one()
    )
    db.delete(obj)
    db.commit()


def get_postfix_map(db: Session, doc_ids: list[str]) -> Mapping[str, str]:

    postfix_map = {
        doc_id: postfix if postfix else ""
        for doc_id, postfix in db.query(Document.import_id, Document.postfix).filter(
            Document.import_id.in_(doc_ids)
        )
    }

    if len(postfix_map) != len(doc_ids):
        missing_ids = set(doc_ids).difference(postfix_map.keys())
        _LOGGER.error(
            "Document ids missing", extra={"props": {"missing_ids": missing_ids}}
        )
        postfix_map.update({missing_id: "" for missing_id in missing_ids})

    return postfix_map
