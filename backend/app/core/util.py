import os
import random
import re
import string
from pathlib import Path
from typing import Any, Union
from urllib.parse import quote_plus, urlsplit

from sqlalchemy.orm import Session

from app.db.session import Base


CDN_URL: str = os.getenv("CDN_URL", "https://cdn.climatepolicyradar.org")
# TODO: remove & replace with proper content-type handling through pipeline
CONTENT_TYPE_MAP = {
    ".pdf": "application/pdf",
    ".html": "text/html",
    ".htm": "text/html",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


def _encode_characters_in_path(s3_path: str) -> str:
    """
    Encode special characters in S3 URL path component to fix broken CDN links.

    :param s3_path: The s3 URL path component in which to fix encodings
    :returns: A URL path component containing encoded characters
    """
    encoded_path = "/".join([quote_plus(c) for c in s3_path.split("/")])
    return encoded_path


def s3_to_cdn_url(s3_url: str) -> str:
    """Convert a URL to a PDF in our s3 bucket to a URL to a PDF in our CDN.

    Args:
        s3_url (str): URL to a PDF in our s3 bucket.

    Returns:
        str: URL to the PDF via our CDN domain.
    """
    converted_cdn_url = re.sub(r"https:\/\/.*\.s3\..*\.amazonaws.com", CDN_URL, s3_url)
    split_url = urlsplit(converted_cdn_url)
    new_path = _encode_characters_in_path(split_url.path)
    # CDN URL should include only scheme, host & modified path
    return f"{split_url.scheme}://{split_url.hostname}{new_path}"


def content_type_from_path(path: Union[Path, str]) -> str:
    """Convert a path/URL to its corresponsing content type based on suffix"""
    suffix = Path(path).suffix
    return CONTENT_TYPE_MAP.get(suffix, "unknown")


def random_string(length=12):
    return "".join(random.choice(string.ascii_lowercase) for i in range(length))


def table_to_json(
    table: Base,
    db: Session,
) -> list[dict]:
    json_out = []

    for row in db.query(table).all():
        row_object = {col.name: getattr(row, col.name) for col in row.__table__.columns}
        json_out.append(row_object)

    return json_out


def tree_table_to_json(
    table: Base,
    db: Session,
) -> list[dict]:
    json_out = []
    child_list_map: dict[int, Any] = {}

    for row in db.query(table).all():
        row_object = {col.name: getattr(row, col.name) for col in row.__table__.columns}
        row_children: list[dict[str, Any]] = []
        child_list_map[row_object["id"]] = row_children

        # No parent indicates a top level element
        node_row_object = {"node": row_object, "children": row_children}
        node_id = row_object["parent_id"]
        if node_id is None:
            json_out.append(node_row_object)
        else:
            append_list = child_list_map.get(node_id)
            if append_list is None:
                raise RuntimeError(f"Could not locate parent node with id {node_id}")
            append_list.append(node_row_object)

    return json_out
