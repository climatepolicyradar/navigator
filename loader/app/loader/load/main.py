import logging
from datetime import datetime
from typing import List, Type

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
)
from sqlalchemy.orm import Session
from app.model import PolicyLookup
from app.service.lookups import get_type_id, get_geography_id
from app.service.validation import get_document_validity_sync

logger = logging.getLogger(__file__)


def load(db: Session, policies: PolicyLookup):
    """Loads policy data into local database."""

    document_source_id = 1  # always CCLW (for alpha)

    imported_count = 0
    debug_count = 0
    for key, policy_data in policies.items():
        # TODO delete this once dev complete
        debug_count += 1
        if debug_count > 10:
            return

        country_code = key.country_code
        geography_id = get_geography_id(db, country_code)
        if not geography_id:
            logger.warning(
                f"No geography found in lookup for country code {country_code}"
            )
            continue

        policy_type = key.policy_type
        document_type_id = get_type_id(db, policy_type)
        if not document_type_id:
            logger.warning(
                f"No action type found in lookup for policy type {policy_type}"
            )
            continue

        policy_date: datetime = key.policy_date
        if policy_date is None:
            logger.warning("Date is null for policy", key)

        # this was the loader before the change to own-db:
        # https://github.com/climatepolicyradar/navigator/blob/17491aceaf9a5a852e0a6d51a1e8f88b07675801/backend/app/api/api_v1/routers/actions.py
        main_doc = None
        for doc in policy_data.docs:

            # TODO name/geography_id/type_id/source_id is not unique, but the
            # addition of url makes it unique. Fetch any existing docs by
            # name/geography_id/type_id/source_id and then set up any associations
            # in case we have a new doc.

            # Optimisation: As the get_document_validity_sync check can take long,
            # check if the document already exists in the DB, and skip if it does
            # (as per the unique constraint)
            maybe_existing_doc = get_document_by_unique_constraint(
                db,
                key.policy_name,
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
                    f"source_id={document_source_id}"
                    f"url={doc.doc_url}"
                )
                continue

            # check doc validity
            is_valid = True

            # TODO async
            # invalid_reason = await get_document_validity(document_create.source_url)
            invalid_reason = get_document_validity_sync(doc.doc_url)

            if invalid_reason:
                is_valid = False
                logger.warning(
                    f"Invalid document, name={key.policy_name}, reason={invalid_reason} "
                    f"url={doc.doc_url}"
                )

            # TODO for S3, see
            # https://github.com/climatepolicyradar/navigator/blob/3ca2eda8de691288a66a1722908f32dd52c178f9/backend/app/api/api_v1/routers/actions.py#L81
            document_db = Document(
                name=key.policy_name,
                source_url=doc.doc_url,
                source_id=document_source_id,
                # url=None,  # TODO: upload to S3
                is_valid=is_valid,
                invalid_reason=invalid_reason,
                geography_id=geography_id,
                type_id=document_type_id,
            )
            db.add(document_db)
            db.flush()
            db.refresh(document_db)

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
                    db.add(association)

            # Metadata - events
            event_db = Event(
                document_id=document_db.id,
                name="Publication",
                description="The publication date",
                created_ts=key.policy_date,
            )
            db.add(event_db)

            # TODO doc.events might have more events, other than publication date

            # Metadata - all the rest
            add_metadata(
                db,
                doc.sectors,
                document_db.id,
                document_source_id,
                Sector,
                DocumentSector,
                "sector_id",
            )
            add_metadata(
                db,
                doc.instruments,
                document_db.id,
                document_source_id,
                Instrument,
                DocumentInstrument,
                "instrument_id",
            )
            add_metadata(
                db,
                doc.frameworks,
                document_db.id,
                document_source_id,
                Framework,
                DocumentFramework,
                "framework_id",
            )
            add_metadata(
                db,
                doc.responses,
                document_db.id,
                document_source_id,
                Response,
                DocumentResponse,
                "response_id",
            )
            add_metadata(
                db,
                doc.hazards,
                document_db.id,
                document_source_id,
                Hazard,
                DocumentHazard,
                "hazard_id",
            )

            # commit for each doc, not each policy
            db.commit()
            imported_count += 1

        main_doc = None

    logger.info(
        f"Done, {imported_count} policies imported out of {len(policies.items())} total"
    )


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
                description="Imported by CPR loader",
                source_id=source_id,
            )
            db.add(sector_db)
            db.flush()
            db.refresh(sector_db)
            document_sector_db = DocumentSector(
                document_id=document_db.id,
                sector_id=sector_db.id,
            )
            db.add(document_sector_db)
            db.commit()

    Into this:

        for metadatum in metadata:
            meta_db = MetaType(
                name=metadatum,
                description="Imported by CPR loader",
                source_id=source_id,
            )
            db.add(meta_db)
            db.flush()
            db.refresh(meta_db)
            document_meta_db = DocumentMetaType(
                document_id=doc_id,
            )
            setattr(document_meta_db, fk_column_name, meta_db.id)
            db.add(document_meta_db)

    Where:
        metadata = doc.sectors
        MetaType = Sector
        DocumentMetaType = DocumentSector
        sector_id = fk_column_name

    """
    for metadatum in metadata:
        meta_db = MetaType(
            name=metadatum,
            description="Imported by CPR loader",
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
