import asyncio
import logging
import ssl
from typing import Optional

import httpx
import tenacity

from app.db.models import DocumentInvalidReason


SINGLE_FILE_CONTENT_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}
ADDITIONAL_SUPPORTED_CONTENT_TYPES = {"text/html"}
SUPPORTED_CONTENT_TYPES = SINGLE_FILE_CONTENT_TYPES | ADDITIONAL_SUPPORTED_CONTENT_TYPES


logger = logging.getLogger(__file__)


def get_document_validity_sync(
    client: httpx.AsyncClient, source_url: str
) -> Optional[DocumentInvalidReason]:
    return asyncio.run(get_document_validity(client, source_url))


async def get_document_validity(
    client: httpx.AsyncClient, source_url: str
) -> Optional[DocumentInvalidReason]:
    if not source_url.strip():
        logger.info("Skipping validity check for empty source URL")
        return DocumentInvalidReason.empty_source

    logger.debug(f"Checking document validity for '{source_url}'")
    try:
        response = await make_head_request(client, source_url)
        content_type = response.headers.get("content-type")
        if content_type not in SUPPORTED_CONTENT_TYPES:
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
    except httpx.RemoteProtocolError:
        return DocumentInvalidReason.net_remote_protocol_error
    except Exception:
        logger.exception("Unexpected error occurred")
        return DocumentInvalidReason.unexpected_failure


@tenacity.retry(
    retry=tenacity.retry_if_not_exception_type(
        (httpx.ConnectError, httpx.ConnectTimeout)
    ),
    stop=tenacity.stop_after_attempt(5),
    wait=tenacity.wait_exponential(max=10),
    reraise=True,
)
async def make_head_request(client: httpx.AsyncClient, api_call: str) -> httpx.Response:
    response: httpx.Response = await client.head(api_call, follow_redirects=True)
    response.raise_for_status()
    return response
