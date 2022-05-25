import os
import random
import re
import string
from pathlib import Path
from typing import Union


CDN_URL: str = os.getenv("CDN_URL", "https://cdn.climatepolicyradar.org")
# TODO: remove & replace with proper content-type handling through pipeline
CONTENT_TYPE_MAP = {
    ".pdf": "application/pdf",
    ".html": "text/html",
    ".htm": "text/html",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


def s3_to_cdn_url(s3_url: str) -> str:
    """Convert a URL to a PDF in our s3 bucket to a URL to a PDF in our CDN.

    Args:
        s3_url (str): URL to a PDF in our s3 bucket.

    Returns:
        str: URL to the PDF via our CDN domain.
    """

    return re.sub(r"https:\/\/.*\.s3\..*\.amazonaws.com", CDN_URL, s3_url)


def content_type_from_path(path: Union[Path, str]) -> str:
    """Convert a path/URL to its corresponsing content type based on suffix"""
    suffix = Path(path).suffix
    return CONTENT_TYPE_MAP.get(suffix, "unknown")


def random_string(length=12):
    return "".join(random.choice(string.ascii_lowercase) for i in range(length))
