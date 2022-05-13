import logging

from app.db.crud import get_all_valid_documents
from app.db.models import (
    APIDocument,
    Document,
)
from app.poster.associations import post_associations_to_backend
from app.poster.post import post_doc
from app.service.context import Context

logger = logging.getLogger(__file__)


def post_all_to_backend_api(ctx: Context):
    """Posts everything in the local database to the remote backend API."""
    for doc in get_all_valid_documents(ctx.db):
        # TODO: optimisation: check if we've uploaded already? (via APIDocument)
        try:
            post_doc_to_backend_api(ctx, doc)
        except Exception as e:
            logger.error(
                f"Loader error: Document could not be posted to API, doc.id={doc.id}",
                exc_info=e,
            )

    post_associations_to_backend(ctx)


def post_doc_to_backend_api(ctx: Context, doc: Document):
    response = post_doc(ctx.db, doc)

    # once we've uploaded, make a note of it.
    if "id" in response:
        remote_document_id = response["id"]
        apidoc = APIDocument(
            document_id=doc.id,
            remote_document_id=remote_document_id,
        )
        ctx.db.add(apidoc)
        ctx.db.commit()
        logger.info(
            f"Document uploaded to API, doc.id={doc.id}, remote doc.id={remote_document_id}"
        )
    else:
        detail = response["detail"]
        logger.warning(
            f"Backend error: Document could not be posted to API, doc.id={doc.id}, error={detail}"
        )
