import logging
import os
from functools import lru_cache
from typing import Callable

import requests

logger = logging.getLogger(__file__)


def get_type_id(type_name):
    return get_id(type_name, get_types_lookup, "action_type_id")


def get_types_lookup():
    return get_lookup("action_types", "type_name")


def get_geography_id(country_code):
    return get_id(country_code, get_geographies_lookup, "geography_id")


def get_geographies_lookup():
    return get_lookup("geographies", "country_code")


def get_id(lookup_key: str, lookup_fn: Callable, id_key: str):
    lookup = lookup_fn()
    match = lookup.get(lookup_key)
    if match:
        return match[id_key]
    else:
        return None


@lru_cache()
def get_lookup(model, lookup_key):
    machine_user_token = os.getenv("MACHINE_USER_LOADER_JWT")

    api_host = os.getenv("API_HOST", "http://backend:8888")
    if api_host.endswith("/"):
        api_host = api_host[:-1]  # strip trailing slash

    headers = {'Authorization': 'Bearer {}'.format(machine_user_token)}
    response = requests.get(f'{api_host}/api/v1/{model}', headers=headers)
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

    headers = {'Authorization': 'Bearer {}'.format(machine_user_token)}
    response = requests.post(f'{api_host}/api/v1/action', headers=headers, json=action_payload)
    return response


def policy_repr(policy):
    """Return a string representation of a policy dataframe row.

    Matches the unique constraint on the backend:
    'name', 'action_date', 'geography_id', 'action_type_id', 'action_source_id' (the latter always 1 for alpha)

    :param policy:
    :return: a string representation
    """
    return "name=[%s], date=[%s], country=[%s], type=[%s]" % (
        policy['policy_name'], policy['policy_date'], policy['country_code'], policy["policy_type"])
