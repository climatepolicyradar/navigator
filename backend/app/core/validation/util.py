import json
import logging
from datetime import datetime
from io import BytesIO
from typing import Any, Collection, Mapping, Optional, Sequence

from sqlalchemy.orm import Session

from app.api.api_v1.routers.lookups.util import get_metadata
from app.api.api_v1.schemas.document import DocumentParserInput
from app.core.aws import S3Client
from app.core.validation import PIPELINE_BUCKET

_LOGGER = logging.getLogger(__file__)

# TODO: This should be config
INGEST_TRIGGER_ROOT = "input"


def _flatten_maybe_tree(
    maybe_tree: Sequence[Mapping[str, Any]],
    values: Optional[list[str]] = None,
) -> Collection[str]:
    def is_tree_node(maybe_node: Mapping[str, Any]) -> bool:
        return set(maybe_node.keys()) == {"node", "children"}

    def get_value(data_node: Mapping[str, str]) -> str:
        value = data_node.get("name") or data_node.get("value")
        if value is None:
            raise Exception(f"No value found in '{data_node}'")
        return value

    values = values or []

    for maybe_node in maybe_tree:
        if is_tree_node(maybe_node):
            values.append(get_value(maybe_node["node"]))
            _flatten_maybe_tree(maybe_node["children"], values=values)
        else:
            values.append(get_value(maybe_node))

    return values


def _prune_nodes_and_children(
    maybe_tree: Sequence[Mapping[str, Any]],
) -> list[Mapping[str, Any]]:
    def is_tree_node(maybe_node: Mapping[str, Any]) -> bool:
        return set(maybe_node.keys()) == {"node", "children"}

    rows = []
    for maybe_node in maybe_tree:
        if is_tree_node(maybe_node):
            rows.append(maybe_node["node"])
            for row in _prune_nodes_and_children(maybe_node["children"]):
                rows.append(row)
        else:
            rows.append(maybe_node)

    return rows


def get_valid_metadata(
    db: Session,
) -> Mapping[str, Mapping[str, Collection[str]]]:
    """
    Make a request to the backend to collect valid metadata values

    :param requests.Session session: The session used for making the request.
    :return Mapping[str, Sequence[str]]: _description_
    """
    _LOGGER.info("Retrieving valid metadata values from database")

    raw_metadata = get_metadata(db)["metadata"]

    return {
        source: {
            meta: _flatten_maybe_tree(raw_metadata[source][meta])
            for meta in raw_metadata[source]
        }
        for source in raw_metadata
    }


def get_valid_metadata_for_db_hints(
    db: Session,
) -> Mapping[str, Mapping[str, Collection[Mapping[str, Any]]]]:
    """
    Make a request to the backend to collect valid metadata values

    :param requests.Session session: The session used for making the request.
    :return Mapping[str, Sequence[str]]: _description_
    """
    _LOGGER.info("Retrieving valid metadata values from database")

    raw_metadata = get_metadata(db)["metadata"]

    return {
        source: {
            meta: _prune_nodes_and_children(raw_metadata[source][meta])
            for meta in raw_metadata[source]
        }
        for source in raw_metadata
    }


def write_documents_to_s3(
    s3_client: S3Client, documents: Sequence[DocumentParserInput]
):
    """
    Write document specifications successfully created during a bulk import to S3

    :param S3Client s3_client: an S3 client to use to write data
    :param Sequence[DocumentCreateRequest] documents: a sequence of document
        specifications to write to S3
    """
    json_content = json.dumps([d.to_json() for d in documents], indent=2)
    bytes_content = BytesIO(json_content.encode("utf8"))
    current_datetime = datetime.now().isoformat().replace(":", ".")
    documents_object_key = f"{INGEST_TRIGGER_ROOT}/{current_datetime}/documents.json"

    s3_client.upload_fileobj(
        bucket=PIPELINE_BUCKET,
        key=documents_object_key,
        content_type="application/json",
        fileobj=bytes_content,
    )
