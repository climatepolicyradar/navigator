import asyncio
import ssl
from typing import Optional

import httpx

from app.db.models import DocumentInvalidReason

transport = httpx.AsyncHTTPTransport(retries=3)
supported_content_types = ["application/pdf", "text/html"]


def get_document_validity_sync(source_url: str) -> Optional[DocumentInvalidReason]:
    return asyncio.run(get_document_validity(source_url))


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
    except httpx.RemoteProtocolError:
        return DocumentInvalidReason.net_remote_protocol_error
