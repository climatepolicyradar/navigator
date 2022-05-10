"""An API client.

The loader previously used lookups from the backend API,
but as it now has it's own database, use app.service.lookups instead.
Then delete this later.
"""

import os
from functools import lru_cache
from typing import Callable, Tuple
import hashlib

import httpx
import requests

from app.service.tree_parser import get_unique_from_tree_by_type

transport = httpx.AsyncHTTPTransport(retries=3)


def get_type_id(type_name):
    def get_types_lookup():
        return _get_keyed_lookup("document_types", "name")

    return _get_attribute(type_name, get_types_lookup, "id")


def get_category_id(category_name):
    def get_categories_lookup():
        return _get_keyed_lookup("categories", "name")

    return _get_attribute(category_name, get_categories_lookup, "id")


def get_geography_id(country_code):
    def get_geographies_lookup():
        return _get_tree_lookup("geographies", "ISO-3166", "value")

    return _get_attribute(country_code, get_geographies_lookup, "id")


def get_country_code_from_geography_id(geography_id):
    def get_geographies_lookup():
        return _get_tree_lookup("geographies", "ISO-3166", "id")

    return _get_attribute(geography_id, get_geographies_lookup, "value")


def get_language_id(language_code):
    def get_language_lookup():
        return _get_keyed_lookup("languages", "language_code")

    return _get_attribute(language_code, get_language_lookup, "id")


def get_language_id_by_part1_code(part1_code):
    def get_language_lookup():
        return _get_keyed_lookup("languages", "part1_code")

    return _get_attribute(part1_code, get_language_lookup, "id")


def get_language_id_by_name(name):
    def get_language_lookup():
        return _get_keyed_lookup("languages", "name")

    return _get_attribute(name, get_language_lookup, "id")


def _get_attribute(lookup_key: str, lookup_fn: Callable, attribute_key: str):
    """Gets an attribute from a lookup by key.

    lookup_fn gets the entire dataset (e.g. all "geographies") from the backend API,
    but as a keyed dictionary (as per `_get_lookup`), so it can be easily used for lookup.
    Once we have the lookup (e.g. "geographies"), find a matching record by lookup_key (e.g. country_code like "KOR")
    Once we have the matching record, return just the component we're interested in,
    as per attribute_key (e.g. "geography_id")
    """
    lookup = lookup_fn()
    match = lookup.get(lookup_key)
    if match:
        return match[attribute_key]
    else:
        return None


@lru_cache()
def _get_lookup_from_api(model):
    """Returns a lookup from the API and caches the result."""

    machine_user_token = os.getenv("MACHINE_USER_LOADER_JWT")

    api_host = os.getenv("API_HOST", "http://backend:8888")
    if api_host.endswith("/"):
        api_host = api_host[:-1]  # strip trailing slash

    headers = {"Authorization": "Bearer {}".format(machine_user_token)}
    response = requests.get(f"{api_host}/api/v1/{model}", headers=headers)

    if response.status_code >= 400:
        raise Exception(
            "Backend error. Check migrations ran, or base data is imported (e.g. geographies)"
        )

    return response.json()


@lru_cache()
def _get_keyed_lookup(model, lookup_key):
    """Returns a lookup from the API as a keyed dictionary, and caches the result.

    E.g. fetches all of "geographies", then turns that list into a dictionary keyed by `lookup_key`.
    """

    json_data = _get_lookup_from_api(model)
    return _keyed(json_data, lookup_key)


@lru_cache()
def _get_tree_lookup(model, node_type, lookup_key):
    tree = _get_lookup_from_api(model)
    all_nodes = get_unique_from_tree_by_type(tree, node_type)
    return _keyed(all_nodes, lookup_key)


def _keyed(data, lookup_key):
    """Returns a map of data keyed by lookup_key.

    E.g. given data:
    [{a:1,b:'foo'}, {a:2,b:'bar'}]
    And lookup_key 'b'
    Return
    {
        'foo': {a:1,b:'foo'},
        'bar': {a:2,b:'bar'}
    }
    """
    lookup = {}
    for datum in data:
        lookup[datum[lookup_key]] = datum
    return lookup


def post_document(payload):
    machine_user_token = os.getenv("MACHINE_USER_LOADER_JWT")

    api_host = os.getenv("API_HOST", "http://backend:8888")
    if api_host.endswith("/"):
        api_host = api_host[:-1]  # strip trailing slash

    headers = {
        "Authorization": "Bearer {}".format(machine_user_token),
        "Accept": "application/json",
    }
    response = requests.post(
        f"{api_host}/api/v1/documents", headers=headers, json=payload
    )
    return response


async def upload_document(
    source_url: str, file_name_without_suffix: str
) -> Tuple[str, str]:
    """Upload a document to the cloud, and returns the cloud URL.

    The remote document will have the specified file_name_without_suffix_{md5_hash},
    where md5_hash is the hash of the file and the suffix is determined from the content type.
    `file_name_without_suffix` will be trimmed if the total path length exceeds 1024 bytes,
    which is the S3 maximum path length.

    TODO stream the download/upload instead of downloading all-at-once first.

    :returns the remote URL and the md5_sum of its contents
    """

    # download the document
    async with httpx.AsyncClient(transport=transport, timeout=10) as client:
        download_response = await client.get(source_url, follow_redirects=True)

        content_type = download_response.headers["Content-Type"]
        file_content = download_response.content
        file_content_hash = hashlib.md5(file_content).hexdigest()

        # determine the remote file name, including folder structure
        parts = file_name_without_suffix.split("-")
        folder_path = parts[0] + "/" + parts[1] + "/"
        file_suffix = content_type.split("/")[1]

        # s3 can only handle paths of up to 1024 bytes. To ensure we don't exceed that,
        # we trim the filename if it's too long
        filename_max_len = (
            1024
            - len(folder_path)
            - len(file_suffix)
            - len(file_content_hash)
            - len("_.")
        )
        file_name_without_suffix_trimmed = file_name_without_suffix[:filename_max_len]

        file_name = (
            f"{file_name_without_suffix_trimmed}_{file_content_hash}.{file_suffix}"
        )

        # puts docs in folder <country_code>/<publication_year>/<file_name>
        full_path = parts[0] + "/" + parts[1] + "/" + file_name

        machine_user_token = os.getenv("MACHINE_USER_LOADER_JWT")

        api_host = os.getenv("API_HOST", "http://backend:8888")
        if api_host.endswith("/"):
            api_host = api_host[:-1]  # strip trailing slash

        headers = {
            "Authorization": "Bearer {}".format(machine_user_token),
            "Accept": "application/json",
        }
        response = await client.post(
            f"{api_host}/api/v1/document",
            headers=headers,
            files={"file": (full_path, file_content, content_type)},
        )
        return response.json()["url"], file_content_hash
