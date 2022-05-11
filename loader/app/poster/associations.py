import logging

from app.db.models import Association, APIDocument
from app.service.api_client import post_associations
from app.service.context import Context


logger = logging.getLogger(__file__)


def post_associations_to_backend(ctx: Context):
    associations = get_associations(ctx)
    post_associations(associations)


def get_associations(ctx: Context):
    associations = ctx.db.query(Association).all()
    remote_docs = ctx.db.query(APIDocument).all()

    # key remote IDs by loader doc ID
    doc_id_map = {}
    for remote_doc in remote_docs:
        doc_id_map[remote_doc.document_id] = remote_doc.remote_document_id

    remote_associations = []
    for association in associations:
        doc_id_from = association.document_id_from
        doc_id_to = association.document_id_to

        try:
            remote_doc_id_from = doc_id_map[doc_id_from]
            remote_doc_id_to = doc_id_map[doc_id_to]
        except KeyError:
            logger.warning(
                f"Local association does not have a remote doc: "
                f"local doc id 'from' = {doc_id_from}, "
                f"local doc id 'to' = {doc_id_to}"
            )
            continue

        remote_pair = [
            remote_doc_id_from,
            remote_doc_id_to,
        ]

        remote_associations.append(remote_pair)

    print(2)
