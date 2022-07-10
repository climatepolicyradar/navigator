import os
import random
import re
import string
from pathlib import Path
from typing import Union
from urllib.parse import urlsplit


CDN_URL: str = os.getenv("CDN_URL", "https://cdn.climatepolicyradar.org")
# TODO: remove & replace with proper content-type handling through pipeline
CONTENT_TYPE_MAP = {
    ".pdf": "application/pdf",
    ".html": "text/html",
    ".htm": "text/html",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}
# Mappings sources from: https://github.com/GeorgePhillips/node-s3-url-encode/blob/master/index.js
S3_URL_REQUIRED_ENCODINGS = {
    "+": "%2B",
    "!": "%21",
    '"': "%22",
    "#": "%23",
    "$": "%24",
    "&": "%26",
    "'": "%27",
    "(": "%28",
    ")": "%29",
    "*": "%2A",
    ",": "%2C",
    ":": "%3A",
    ";": "%3B",
    "=": "%3D",
    "?": "%3F",
    "@": "%40",
}
S3_REPLACE_REGEX = regex = re.compile(
    "(%s)" % "|".join(map(re.escape, S3_URL_REQUIRED_ENCODINGS.keys()))
)


def _encode_characters(s3_url: str) -> str:
    """
    Encode special characters in S3 URL to fix broken CDN links.

    :param s3_url: The s3 URL in which to fix encodings
    :returns: A URL containing encoded characters
    """
    for character, replacement in S3_URL_REQUIRED_ENCODINGS.items():
        s3_url = s3_url.replace(character, replacement)
    return s3_url


def s3_to_cdn_url(s3_url: str) -> str:
    """Convert a URL to a PDF in our s3 bucket to a URL to a PDF in our CDN.

    Args:
        s3_url (str): URL to a PDF in our s3 bucket.

    Returns:
        str: URL to the PDF via our CDN domain.
    """
    converted_cdn_url = re.sub(r"https:\/\/.*\.s3\..*\.amazonaws.com", CDN_URL, s3_url)
    split_url = urlsplit(converted_cdn_url)
    new_path = _encode_characters(split_url.path)
    # CDN URL should include only scheme, host & modified path
    return f"{split_url.scheme}://{split_url.hostname}{new_path}"


def content_type_from_path(path: Union[Path, str]) -> str:
    """Convert a path/URL to its corresponsing content type based on suffix"""
    suffix = Path(path).suffix
    return CONTENT_TYPE_MAP.get(suffix, "unknown")


def random_string(length=12):
    return "".join(random.choice(string.ascii_lowercase) for i in range(length))
