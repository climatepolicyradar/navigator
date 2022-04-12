import logging
from datetime import datetime

from app.db.models import Document, Event
from sqlalchemy.orm import Session
from app.model import PolicyLookup
from app.service.lookups import get_type_id, get_geography_id
from app.service.validation import get_document_validity_sync

logger = logging.getLogger(__file__)


def load(db: Session, policies: PolicyLookup):

    imported_count = 0
    for key, policy_data in policies.items():

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
        for doc in policy_data.docs:

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

            with db.begin():
                doc = Document(
                    name=key.policy_name,
                    source_url=doc.doc_url,
                    source_id=1,
                    # url=None,  # TODO: upload to S3
                    is_valid=is_valid,
                    invalid_reason=invalid_reason,
                    geography_id=geography_id,
                    type_id=document_type_id,
                )
                db.add(doc)

                event = Event(
                    document_id=doc.id,
                    name="Publication",
                    description="The publication date",
                    created_ts=key.policy_date,
                )
                db.add(event)

                # TODO persist doc association
                imported_count += 1

    logger.info(
        f"Done, {imported_count} policies imported out of {len(policies.items())} total"
    )
