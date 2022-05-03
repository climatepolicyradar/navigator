import logging
import logging.config
import os
import sys
from csv import DictReader
from typing import List, Optional, TextIO, Union

import requests


DEFAULT_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Default is stderr
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["default"],
            "level": "INFO",
        },
        "__main__": {  # if __name__ == '__main__'
            "handlers": ["default"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

logging.config.dictConfig(DEFAULT_LOGGING)
logger = logging.getLogger(__file__)

EXPECTED_USER_CSV_FIELDS = {
    "name",
    "organisation",
    "affiliation_type",
    "other_affiliation",
    "email",
    "policy_data_types",
    "geographical_scope",
    "data_focus",
    "policy_databases",
    "challenges",
    "referral",
    "interview",
    "ip",
    "user_agent",
    "referrer",
    "created_at",
}


def validate_open_csv(csv: TextIO) -> DictReader:
    csv_reader = DictReader(csv)

    csv_fieldnames = set(csv_reader.fieldnames or [])
    if not csv_fieldnames:
        error = "Invalid User CSV; No headers found"
        logger.error(error)
        raise RuntimeError(error)

    if csv_fieldnames != EXPECTED_USER_CSV_FIELDS:
        error = "Invalid User CSV supplied."

        missing_fields = EXPECTED_USER_CSV_FIELDS - csv_fieldnames
        if missing_fields:
            error += f" The following fields were missing: {missing_fields}."

        unexpected_fields = csv_fieldnames - EXPECTED_USER_CSV_FIELDS
        if unexpected_fields:
            error += f" The following fields were not expected: {unexpected_fields}"

        logger.error(error)
        raise RuntimeError(error)

    return csv_reader


def get_admin_token():
    admin_user = os.getenv("ADMIN_USER")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if admin_user is None or admin_password is None:
        raise RuntimeError("Admin username & password env vars must be set")

    url = get_request_url("/api/tokens")
    response = requests.post(url)
    token: str = response.json()
    return token


def get_admin_auth_headers():
    if (admin_user_token := os.getenv("ADMIN_USER_TOKEN")) is None:
        admin_user_token = get_admin_token()
        os.environ["ADMIN_USER_TOKEN"] = admin_user_token

    return {
        "Authorization": "Bearer {}".format(admin_user_token),
        "Accept": "application/json",
    }


def get_request_url(endpoint):
    api_host = os.getenv("API_HOST", "http://backend:8888").rstrip("/")
    return f"{api_host}/{endpoint}"


def post_user(payload):
    url = get_request_url("/api/v1/admin/users")
    headers = get_admin_auth_headers()
    response = requests.post(
        f"{url}",
        headers=headers,
        json=payload,
    )
    return response


def _make_list_if_necessary(
    input: Optional[Union[str, List[str]]]
) -> Optional[List[str]]:
    """Make list from string if necessary."""
    if input is None or not input:
        return None

    if isinstance(input, str):
        return [input]

    return input


def _make_str_from_maybe_list(input: Optional[Union[str, List[str]]]) -> Optional[str]:
    """Remove unnecessary lists."""
    if input is None or not input:
        return None

    if isinstance(input, list):
        return input[0]

    return input


def main(users_csv_path):
    """Initial loader for alpha users.

    Load users into the backend API database from CSV.

    :return: None
    """
    with open(users_csv_path, "r") as users_csv:
        csv_reader = validate_open_csv(users_csv)
        for row in csv_reader:
            payload = {
                "email": _make_str_from_maybe_list(row["email"]),
                "names": _make_str_from_maybe_list(row["name"]),
                "is_active": False,
                "is_superuser": False,
                "job_role": None,
                "location": None,
                "affiliation_organisation": _make_str_from_maybe_list(
                    row["organisation"]
                ),
                "affiliation_type": _make_str_from_maybe_list(row["affiliation_type"]),
                "policy_type_of_interest": _make_list_if_necessary(
                    row["policy_data_types"]
                ),
                "geographies_of_interest": _make_list_if_necessary(
                    row["geographical_scope"]
                ),
                "data_focus_of_interest": _make_list_if_necessary(row["data_focus"]),
            }
            post_user(payload=payload)


if __name__ == "__main__":
    users_csv = sys.argv[1]

    if os.getenv("ENV") != "production":
        # for running locally (outside docker)
        from dotenv import load_dotenv

        load_dotenv("../../.env")
        load_dotenv("../../.env.local")

    main(users_csv)
