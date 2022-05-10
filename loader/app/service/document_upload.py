import logging

from app.db.models import Document, Event
from app.service.api_client import upload_document, get_country_code_from_geography_id
from app.service.context import Context

logger = logging.getLogger(__file__)


async def upload_all_documents(ctx: Context):
    """Upload all source_url docs to cloud.

    The remote filename follows the template on
    https://www.notion.so/climatepolicyradar/Document-names-on-S3-6f3cd748c96141d3b714a95b42842aeb

    """

    for document_db in ctx.db.query(Document).filter(Document.is_valid).all():
        # fetch metadata required for naming the remote doc
        event: Event = (
            ctx.db.query(Event)
            .filter(
                (Event.document_id == document_db.id) & (Event.name == "Publication")
            )
            .first()
        )
        country_code = get_country_code_from_geography_id(document_db.geography_id)
        publication_date = event.created_ts.date().isoformat()

        logger.debug(f"Uploading {document_db.source_url} to {document_db.url}")
        # TODO: make document upload more resilient
        try:
            await _upload_document(ctx, document_db, country_code, publication_date)
        except Exception as e:
            logger.error(
                f"Uploading document with URL {document_db.source_url} failed",
                exc_info=e,
            )


async def _upload_document(
    ctx: Context, document_db: Document, country_code: str, publication_date_iso: str
):
    """Upload a single doc."""

    # TODO this depends on the new CSV layout for multi-doc actions,
    # but in the meantime, we just use "<doc name> <doc id>"
    # We replace forward slashes with underscores because S3 recognises them as directory splitters
    doc_name = f"{document_db.name}-{document_db.id}".replace("/", "_")

    file_name = f"{country_code}-{publication_date_iso}-{doc_name}"

    cloud_url, md5_sum = await upload_document(ctx, document_db.source_url, file_name)
    document_db.url = cloud_url
    document_db.md5_sum = md5_sum
    ctx.db.add(document_db)
    ctx.db.commit()
