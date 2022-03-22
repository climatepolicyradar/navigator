import os
from functools import lru_cache
from typing import Callable

import requests


def get_type_id(type_name):
    def get_types_lookup():
        return _get_lookup("action_types", "type_name")

    return _get_id(type_name, get_types_lookup, "action_type_id")


def get_geography_id(country_code):
    def get_geographies_lookup():
        return _get_lookup("geographies", "country_code")

    return _get_id(country_code, get_geographies_lookup, "geography_id")


def get_language_id(language_code):
    def get_language_lookup():
        return _get_lookup("languages", "language_code")

    return _get_id(language_code, get_language_lookup, "language_id")


def get_language_id_by_part1_code(part1_code):
    def get_language_lookup():
        return _get_lookup("languages", "part1_code")

    return _get_id(part1_code, get_language_lookup, "language_id")


def _get_id(lookup_key: str, lookup_fn: Callable, id_key: str):
    """Gets an ID from a lookup by key.

    lookup_fn gets the entire dataset (e.g. all "geographies") from the backend API,
    but as a keyed dictionary (as per `_get_lookup`), so it can be easily used for lookup.
    Once we have the lookup (e.g. "geographies"), find a matching record by lookup_key (e.g. country_code like "KOR")
    Once we have the matching record, return just the component we're interested in, by id_key (e.g. "geography_id")
    """
    lookup = lookup_fn()
    match = lookup.get(lookup_key)
    if match:
        return match[id_key]
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


def post_action(action_payload):
    machine_user_token = os.getenv("MACHINE_USER_LOADER_JWT")

    api_host = os.getenv("API_HOST", "http://backend:8888")
    if api_host.endswith("/"):
        api_host = api_host[:-1]  # strip trailing slash

    headers = {
        "Authorization": "Bearer {}".format(machine_user_token),
        "Accept": "application/json",
    }
    response = requests.post(
        f"{api_host}/api/v1/actions", headers=headers, json=action_payload
    )
    return response
