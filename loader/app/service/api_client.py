"""An API client.

The loader previously used lookups from the backend API,
but as it now has it's own database, use app.service.lookups instead.
Then delete this later.
"""

import os
from functools import lru_cache
from typing import Callable

import requests


def get_type_id(type_name):
    def get_types_lookup():
        return _get_lookup("document_type", "value")

    return _get_attribute(type_name, get_types_lookup, "id")


def get_geography_id(country_code):
    def get_geographies_lookup():
        return _get_lookup("geographies", "value")

    return _get_attribute(country_code, get_geographies_lookup, "id")


def get_country_code_from_geography_id(geography_id):
    def get_geographies_lookup():
        return _get_lookup("geographies", "id")

    return _get_attribute(geography_id, get_geographies_lookup, "value")


def get_language_id(language_code):
    def get_language_lookup():
        return _get_lookup("languages", "language_code")

    return _get_attribute(language_code, get_language_lookup, "id")


def get_language_id_by_part1_code(part1_code):
    def get_language_lookup():
        return _get_lookup("languages", "part1_code")

    return _get_attribute(part1_code, get_language_lookup, "id")


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
def _get_lookup(model, lookup_key):
    """Returns a lookup from the API as a keyed dictionary.

    E.g. fetches all of "geographies", then turns that list into a dictionary keyed by `lookup_key`.
    """
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

    json_data = response.json()
    lookup = {}
    for datum in json_data:
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


def upload_document(source_url: str, file_name_without_suffix: str) -> str:
    """Upload a document to the cloud, and returns the cloud URL.

    The remote document will have the specified file_name_without_suffix,
    and the suffix will be determined from the content type.

    TODO stream the download/upload instead of downloading all-at-once first.
    """

    # download the document
    download_response = requests.get(source_url)
    content_type = download_response.headers["Content-Type"]
    file_content = download_response.content

    # determine the remote file name, including folder structure
    file_suffix = content_type.split("/")[1]
    file_name = f"{file_name_without_suffix}.{file_suffix}"

    parts = file_name.split("-")
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
    response = requests.post(
        f"{api_host}/api/v1/document",
        headers=headers,
        files={"file": (full_path, file_content, content_type)},
    )
    return response.json()["url"]
