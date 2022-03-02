import logging
from datetime import datetime
from json import JSONDecodeError

from app.load.api_client import get_type_id, get_geography_id, post_action
from app.load.language import get_language_id_for_doc
from app.model import PolicyLookup

logger = logging.getLogger(__file__)


def load(policies: PolicyLookup):
    imported_count = 0
    for key, policy_data in policies.items():

        country_code = key.country_code
        geography_id = get_geography_id(country_code)
        if not geography_id:
            logger.warning(
                f"No geography found in lookup for country code {country_code}"
            )
            continue

        policy_type = key.policy_type
        action_type_id = get_type_id(policy_type)
        if not action_type_id:
            logger.warning(
                f"No action type found in lookup for policy type {policy_type}"
            )
            continue

        policy_date: datetime = key.policy_date
        if policy_date is None:
            logger.warning("Date is null for policy", key)

        action_payload = {
            "name": key.policy_name,
            "description": policy_data.policy_description,
            "year": policy_date.year,
            "month": policy_date.month,
            "day": policy_date.day,
            "geography_id": geography_id,
            "type_id": action_type_id,
            "source_id": 1,  # CCLW is source_id 1
            "documents": [
                {
                    "name": doc.doc_name,
                    "language_id": get_language_id_for_doc(doc),
                    "source_url": doc.doc_url,
                    "s3_url": None,  # TODO is this supposed to be doc.doc_url?
                    # This defaults to action date for now, as it's not in the CSV.
                    # In future, we parse the date out of the doc, and update accordingly
                    # Marcus: I think for cases with only one document per action (most cases),
                    # taking the action date as the document date will be a pretty reliable approach.
                    "year": policy_date.year,
                    "month": policy_date.month,
                    "day": policy_date.day,
                }
                for doc in policy_data.docs
            ],
        }

        response = post_action(action_payload)
        if response.status_code < 400:
            imported_count += 1
            name = response.json()["name"]
            logger.info(f"Added action to database: {name}")
        else:
            message = "Unknown error"
            try:
                message = str(response.json())
            except JSONDecodeError:
                message = str(response.content)
            finally:
                if "already exists" in message:
                    logger.warning(f"Skipping duplicate item, policy={key}")
                elif "unsupported mimetype" in message:
                    logger.warning(
                        f"Skipping unsupported/unfetchable doc, policy={key}"
                    )
                elif "date of the action provided is in the future" in message:
                    logger.warning(f"Skipping future action, policy={key}")
                else:
                    logger.error(
                        f"Error importing action and document(s) for policy={policy_data}, error={message}"
                    )
                    return

    logger.info(
        f"Done, {imported_count} policies imported out of {len(policies.items())} total"
    )
