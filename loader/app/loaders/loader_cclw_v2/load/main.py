import asyncio
import logging
from datetime import datetime
from typing import List, Type

from sqlalchemy.orm import Session

from app.db.crud import get_document_by_unique_constraint
from app.db.models import (
    Association,
    Document,
    Event,
    Sector,
    DocumentSector,
    Instrument,
    DocumentInstrument,
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
from app.mapping import DEFAULT_DESCRIPTION
from app.model import PolicyLookup, Event as SourceEvent, Key, PolicyData
from app.service.api_client import (
    get_type_id,
    get_geography_id,
    get_category_id,
    get_language_id_by_name,
)
from app.service.context import Context
from app.service.validation import get_document_validity

logger = logging.getLogger(__file__)


document_source_id = 1  # always CCLW (for alpha)


async def load(ctx: Context, policies: PolicyLookup):
    """Loads policy data into local database."""

    tasks = []
    for key, policy_data in policies.items():
        task = asyncio.ensure_future(save_action(ctx, key, policy_data))
        tasks.append(task)

        # # -- for debugging
        # if len(tasks) > 1:
        #     break

    doc_counts = await asyncio.gather(
        *tasks,
        # return_exceptions=True,
    )

    doc_count = sum(doc_counts)
    logger.info(f"Done, imported {doc_count} docs from {len(policies.items())} actions")


def warmup_local_caches():
    get_type_id("dummy-call-to-warm-up-cache")
    get_geography_id("dummy-call-to-warm-up-cache")
    get_category_id("dummy-call-to-warm-up-cache")
    get_language_id_by_name("dummy-call-to-warm-up-cache")


async def save_action(ctx: Context, key: Key, policy_data: PolicyData) -> int:
    # look up geography from API
    country_code = key.country_code
    geography_id = get_geography_id(country_code)
    if not geography_id:
        logger.warning(f"No geography found in lookup for country code {country_code}")
        # continue
        return 0

    # this was the loader before the change to own-db:
    # https://github.com/climatepolicyradar/navigator/blob/17491aceaf9a5a852e0a6d51a1e8f88b07675801/backend/app/api/api_v1/routers/actions.py

    # If a policy has multiple docs,
    # during doc looping, we set a main_doc if it hasn't been set,
    # then use it for associating with subsequent docs.
    main_doc = None
    doc_count = 0
    for doc in policy_data.docs:

        document_date: datetime = doc.publication_date
        if document_date is None:
            logger.warning(f"Date is null for document {doc.doc_name}")

        # look up document category from API
        document_category = doc.document_category
        category_id = get_category_id(document_category)
        if not category_id:
            logger.warning(
                f"No document category found in lookup for document category {document_category}"
            )
            continue

        # TODO name/geography_id/type_id/source_id is not unique, but the
        # addition of url makes it unique. Fetch any existing docs by
        # name/geography_id/type_id/source_id and then set up any associations
        # in case we have a new doc.
        # (This to-do does not apply for alpha, as we load data from scratch every time.)

        # look up language from API
        # TODO multi-language support for docs imminent with CSV reformat
        language_id = get_language_id_by_name(doc.doc_languages[0] or "English")

        # look up document type from API
        document_type_id = get_type_id(doc.document_type)
        if not document_type_id:
            logger.warning(
                f"No document type found in lookup for policy type {doc.document_type} (document url: {doc.doc_url})"
            )
            continue

        # Optimisation: As the get_document_validity_sync check can take long,
        # check if the document already exists in the DB, and skip if it does
        # (as per the unique constraint)
        maybe_existing_doc = get_document_by_unique_constraint(
            ctx.db,
            doc.doc_name,
            geography_id,
            document_type_id,
            document_source_id,
            doc.doc_url,
        )
        if maybe_existing_doc:
            logger.warning(
                f"Skipping existing doc, name={key.policy_name}, "
                f"geography_id={geography_id}, "
                f"type_id={document_type_id}, "
                f"source_id={document_source_id}, "
                f"url={doc.doc_url}"
            )
            continue

        # check doc validity
        is_valid = True

        invalid_reason = await get_document_validity(ctx.client, doc.doc_url)

        if invalid_reason:
            is_valid = False
            logger.warning(
                f"Invalid document, name={key.policy_name}, reason={invalid_reason} "
                f"url={doc.doc_url}"
            )

        # TODO for S3, see
        # https://github.com/climatepolicyradar/navigator/blob/3ca2eda8de691288a66a1722908f32dd52c178f9/backend/app/api/api_v1/routers/actions.py#L81
        document_db = Document(
            name=doc.doc_name,
            description=doc.doc_description,
            source_url=doc.doc_url,
            source_id=document_source_id,
            # url=None,  # TODO: upload to S3
            is_valid=is_valid,
            invalid_reason=invalid_reason,
            geography_id=geography_id,
            type_id=document_type_id,
            category_id=category_id,
            publication_ts=document_date,
        )
        ctx.db.add(document_db)
        ctx.db.flush()
        ctx.db.refresh(document_db)

        # Association
        if len(policy_data.docs) > 1:
            if not main_doc:
                main_doc = document_db
            else:
                association = Association(
                    document_id_from=document_db.id,
                    document_id_to=main_doc.id,
                    type="related",
                    name="related",
                )
                ctx.db.add(association)

        # Metadata - events
        event_db = Event(
            document_id=document_db.id,
            name="Publication",
            description="The publication date",
            created_ts=doc.publication_date,
        )
        ctx.db.add(event_db)

        add_events(ctx.db, document_db.id, doc.events)

        # Metadata - all the rest
        add_metadata(
            ctx.db,
            doc.sectors,
            document_db.id,
            document_source_id,
            Sector,
            DocumentSector,
            "sector_id",
        )
        add_metadata(
            ctx.db,
            doc.instruments,
            document_db.id,
            document_source_id,
            Instrument,
            DocumentInstrument,
            "instrument_id",
        )
        add_metadata(
            ctx.db,
            doc.frameworks,
            document_db.id,
            document_source_id,
            Framework,
            DocumentFramework,
            "framework_id",
        )
        add_metadata(
            ctx.db,
            doc.responses,
            document_db.id,
            document_source_id,
            Response,
            DocumentResponse,
            "response_id",
        )
        add_metadata(
            ctx.db,
            doc.hazards,
            document_db.id,
            document_source_id,
            Hazard,
            DocumentHazard,
            "hazard_id",
        )
        add_metadata(
            ctx.db,
            doc.keywords,
            document_db.id,
            document_source_id,
            Keyword,
            DocumentKeyword,
            "keyword_id",
        )

        # doc language
        document_language_db = DocumentLanguage(
            language_id=language_id,
            document_id=document_db.id,
        )
        ctx.db.add(document_language_db)

        # commit for each doc, not each policy
        ctx.db.commit()
        logger.info(
            f"Saved document, name={key.policy_name}, "
            f"geography_id={geography_id}, "
            f"type_id={document_type_id}, "
            f"source_id={document_source_id}"
            f"url={doc.doc_url}"
        )
        doc_count += 1
    return doc_count


def add_metadata(
    db: Session,
    metadata: List[str],
    doc_id: int,
    source_id: int,
    MetaType: Type,
    DocumentMetaType: Type,
    fk_column_name: str,
):
    """Add metadata to DB relating to a document.

    Turns this:
        for sector in doc.sectors:
            sector_db = Sector(
                name=sector,
                description=DEFAULT_DESCRIPTION,
                source_id=source_id,
            )
            ctx.db.add(sector_db)
            ctx.db.flush()
            ctx.db.refresh(sector_db)
            document_sector_db = DocumentSector(
                document_id=document_db.id,
                sector_id=sector_ctx.db.id,
            )
            ctx.db.add(document_sector_db)
            ctx.db.commit()

    Into this:

        for metadatum in metadata:
            meta_db = MetaType(
                name=metadatum,
                description=DEFAULT_DESCRIPTION,
                source_id=source_id,
            )
            ctx.db.add(meta_db)
            ctx.db.flush()
            ctx.db.refresh(meta_db)
            document_meta_db = DocumentMetaType(
                document_id=doc_id,
            )
            setattr(document_meta_db, fk_column_name, meta_ctx.db.id)
            ctx.db.add(document_meta_db)

    Where:
        metadata = doc.sectors
        MetaType = Sector
        DocumentMetaType = DocumentSector
        sector_id = fk_column_name

    """
    for metadatum in metadata:
        # TODO check if metadata already exists, and re-use the FK
        meta_db = MetaType(
            name=metadatum,
            description=DEFAULT_DESCRIPTION,
            # source_id=source_id,
        )
        if hasattr(meta_db, "source_id"):
            setattr(meta_db, "source_id", source_id)

        db.add(meta_db)
        db.flush()
        db.refresh(meta_db)
        document_meta_db = DocumentMetaType(
            document_id=doc_id,
        )
        setattr(document_meta_db, fk_column_name, meta_db.id)
        db.add(document_meta_db)


def add_events(db: Session, doc_id: int, events: List[SourceEvent]):
    """Adds source events to database."""
    for event in events:
        event_db = Event(
            document_id=doc_id,
            name=event.name,
            description=DEFAULT_DESCRIPTION,
            created_ts=event.date,
        )
        db.add(event_db)
