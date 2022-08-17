import json
import logging
import logging.config
import os
import sys
from csv import DictReader
from typing import List, Optional, TextIO

import requests

ADMIN_EMAIL_ENV = "SUPERUSER_EMAIL"
ADMIN_PASSWORD_ENV = "SUPERUSER_PASSWORD"
ADMIN_TOKEN_ENV = "SUPERUSER_TOKEN"


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

REQUIRED_USER_CSV_FIELDS = {
    "name",
    "email",
}
EXPECTED_USER_CSV_FIELDS = {
    "organisation",
    "affiliation_type",
    "other_affiliation",
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
    "job_role",
    "location",
}


def validate_open_csv(csv: TextIO) -> DictReader:
    """Validate that the given CSV file is valid & return a CSVReader object."""
    csv_reader = DictReader(csv)
    csv_fieldnames = set(csv_reader.fieldnames or [])

    # If any required fields are missing (or fields not in CSV) exit immediately
    if not csv_fieldnames.issuperset(REQUIRED_USER_CSV_FIELDS):
        missing_fields = REQUIRED_USER_CSV_FIELDS - csv_fieldnames
        logger.error(f"Required CSV Fields missing: '{missing_fields}'")
        sys.exit(10)

    # Expected fields can be used to add extra user detail, but are not required
    missing_fields = EXPECTED_USER_CSV_FIELDS - csv_fieldnames
    if missing_fields:
        error = (
            "User CSV does not contain all possible user detail information."
            f" The following fields were missing: {missing_fields}."
        )
        logger.error(error)

    # Unexpected fields will not be used, simply ignored
    all_supported_fields = REQUIRED_USER_CSV_FIELDS | EXPECTED_USER_CSV_FIELDS
    unexpected_fields = csv_fieldnames - all_supported_fields
    if unexpected_fields:
        error = (
            "User CSV contains fields that will not be used during user creation."
            f" The following fields were not expected: {unexpected_fields}"
        )
        logger.error(error)

    return csv_reader


def _log_response(response: requests.Response) -> None:
    if response.status_code >= 400:
        logger.error(
            f"There was an error during a request to {response.url}. "
            f"STATUS: {response.status_code}, BODY:{response.content!r}"
        )

    logger.debug(f"STATUS: {response.status_code}, BODY:{response.content!r}")


def get_admin_token() -> str:
    """Go through the login flow & create access token for requests."""
    admin_user = os.getenv(ADMIN_EMAIL_ENV)
    admin_password = os.getenv(ADMIN_PASSWORD_ENV)

    if admin_user is None or admin_password is None:
        raise RuntimeError("Admin username & password env vars must be set")

    response = requests.post(
        get_request_url("/api/tokens"),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"username": admin_user, "password": admin_password},
    )
    _log_response(response=response)

    token: str = response.json()["access_token"]
    return token


def get_admin_auth_headers():
    """Create the required auth headers for requests."""
    if (admin_user_token := os.getenv(ADMIN_TOKEN_ENV)) is None:
        admin_user_token = get_admin_token()
        os.environ[ADMIN_TOKEN_ENV] = admin_user_token

    return {
        "Authorization": "Bearer {}".format(admin_user_token),
        "Accept": "application/json",
    }


def get_request_url(endpoint):
    api_host = os.getenv("API_HOST", "http://backend:8888").rstrip("/")
    return f"{api_host}/{endpoint}"


def post_user(payload):
    response = requests.post(
        get_request_url("/api/v1/admin/users"),
        headers=get_admin_auth_headers(),
        json=payload,
    )
    return response


class RowParseException(Exception):
    """Row parsing failed for the given reason."""

    pass


def _make_list_if_necessary(input: Optional[str]) -> Optional[List[str]]:
    """Make list from string if necessary."""
    if input is None or not input:
        return None

    if input.strip().startswith("["):
        try:
            return json.loads(input)
        except json.JSONDecodeError:
            logger.error(f"Failed to decode input that appears to be a list: {input}")
            raise RowParseException(f"Failed to decode input: {input}")

    # input is just a string, so return it in a list
    return [input]


def _make_str_from_maybe_list(input: Optional[str]) -> Optional[str]:
    """Remove unnecessary lists."""
    if input is None or not input:
        return None

    if input.strip().startswith("["):
        try:
            input_list = json.loads(input)
        except json.JSONDecodeError:
            logger.error(f"Failed to decode input that appears to be a list: {input}")
            raise RowParseException(f"Failed to decode input: {input}")

        if input_list:
            if len(input_list) > 1:
                raise RowParseException(f"Input should have max 1 element: {input}")
            return input_list[0]

        return None

    # input must be a non-empty string no starting with '[']
    return input


def main(users_csv_path):
    """Initial loader for alpha users.

    Load users into the backend API database from CSV.

    :return: None
    """
    with open(users_csv_path, "r") as users_csv:
        csv_reader = validate_open_csv(users_csv)
        emails = []
        for row in csv_reader:
            try:
                email = _make_str_from_maybe_list(row["email"])
                if not email:
                    logger.error(f"Row includes an empty email address: {row}")
                    continue

                name = _make_str_from_maybe_list(row["name"])
                if not name:
                    logger.error(f"Row includes an empty name: {row}")
                    continue

                payload = {
                    "email": email.lower(),
                    "names": name,
                    "job_role": row.get("job_role"),
                    "location": row.get("location"),
                    "affiliation_organisation": _make_str_from_maybe_list(
                        row.get("organisation")
                    ),
                    "affiliation_type": _make_list_if_necessary(
                        row.get("affiliation_type")
                    ),
                    "policy_type_of_interest": _make_list_if_necessary(
                        row.get("policy_data_types")
                    ),
                    "geographies_of_interest": _make_list_if_necessary(
                        row.get("geographical_scope")
                    ),
                    "data_focus_of_interest": _make_list_if_necessary(
                        row.get("data_focus")
                    ),
                    "is_active": False,
                    "is_superuser": False,
                }
                add_user_response = post_user(payload=payload)
                _log_response(response=add_user_response)

                if add_user_response.status_code == 200:
                    logger.info(f"Successfully Added User: '{name}' 'email.lower()'")
                    emails.append(email.lower())
            except RowParseException:
                logger.error(f"Failed to parse row content, skipping entry for: {row}")

        if emails:
            print(f"Successfully added {len(emails)} new users.")
            print(f"The following email addresses were added: {emails}.")
        else:
            print("No new users were added.")


if __name__ == "__main__":
    users_csv = sys.argv[1]

    if os.getenv("ENV") != "production":
        # for running locally (outside docker)
        from dotenv import load_dotenv

        load_dotenv("../../.env")
        load_dotenv("../../.env.local")

    main(users_csv)
