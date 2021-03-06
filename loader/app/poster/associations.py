import logging
from typing import List

from app.db.crud import get_all_associations, get_all_api_documents
from app.db.schema import AssociationSchema
from app.service.api_client import post_association
from app.service.context import Context

logger = logging.getLogger(__file__)


def post_associations(associations: List[AssociationSchema]):
    for association in associations:
        post_association(association)


def post_associations_to_backend(ctx: Context):
    associations = get_associations(ctx)
    post_associations(associations)


def get_associations(ctx: Context) -> List[AssociationSchema]:
    associations = get_all_associations(ctx.db)
    remote_docs = get_all_api_documents(ctx.db)

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
            # the docs might not exist remotely because their URLs had issues (valid=false)
            logger.warning(
                f"Local association does not have a remote doc: "
                f"local doc id 'from' = {doc_id_from}, "
                f"local doc id 'to' = {doc_id_to}"
            )
            continue

        remote_association = AssociationSchema(
            document_id_from=remote_doc_id_from,
            document_id_to=remote_doc_id_to,
            name=association.name,
            type=association.type,
        )

        remote_associations.append(remote_association)

    return remote_associations
