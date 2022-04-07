import asyncio
import logging
import ssl
from datetime import datetime
from typing import Optional

import httpx

from app.db.models import Document
from app.db.models import DocumentInvalidReason
from app.db.session import get_db
from app.load.api_client import get_type_id, get_geography_id
from app.model import PolicyLookup

logger = logging.getLogger(__file__)


def load(policies: PolicyLookup):
    db = get_db()

    imported_count = 0
    for key, policy_data in policies.items():

        country_code = key.country_code
        geography_id = get_geography_id(country_code)
        if not geography_id:
            logger.warning(
                f"No geography found in lookup for country code {country_code}"
            )
            continue

        policy_type = key.policy_type
        action_type_id = get_type_id(policy_type)
        if not action_type_id:
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

            # TODO async one day
            # invalid_reason = await get_document_validity(document_create.source_url)
            invalid_reason = asyncio.run(get_document_validity(doc.doc_url))

            if invalid_reason:
                is_valid = False
                logger.warning(
                    f"Invalid document, name={key.policy_name}, reason={invalid_reason} "
                    f"url={doc.doc_url}"
                )

            db_user = Document(
                loaded_ts=datetime.utcnow(),
                name=key.policy_name,
                source_url=doc.doc_url,
                source_id=1,
                # url=None,  # TODO: upload to S3
                is_valid=is_valid,
                invalid_reason=invalid_reason,
                geography_id=1,  # TODO
                type_id=1,  # TODO
            )
            db.add(db_user)
            db.commit()

    logger.info(
        f"Done, {imported_count} policies imported out of {len(policies.items())} total"
    )


transport = httpx.AsyncHTTPTransport(retries=3)
supported_content_types = ["application/pdf", "text/html"]


async def get_document_validity(source_url: str) -> Optional[DocumentInvalidReason]:
    try:
        async with httpx.AsyncClient(transport=transport, timeout=10) as client:
            response = await client.head(source_url, follow_redirects=True)
            content_type = response.headers.get("content-type")
            if content_type not in supported_content_types:
                return DocumentInvalidReason.unsupported_content_type
            else:
                return None  # no reason needed

    except (ssl.SSLCertVerificationError, ssl.SSLError):
        # we do not want to download insecurely
        return DocumentInvalidReason.net_ssl_error
    except (httpx.ConnectError, httpx.ConnectTimeout):
        # not sure if this is worth retrying, as there's probably nothing listening on the other side
        return DocumentInvalidReason.net_connection_error
    except (httpx.ReadError, httpx.ReadTimeout):
        return DocumentInvalidReason.net_read_error
    except httpx.TooManyRedirects:
        return DocumentInvalidReason.net_too_many_redirects
