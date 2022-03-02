import logging
from datetime import datetime

import pandas
from pandas import DataFrame

from app.load.util import get_geography_id, get_type_id, post_action, policy_repr
from app.mapping import CCLWActionType

logger = logging.getLogger(__file__)


def load(policies: DataFrame):
    for idx, policy in policies.iterrows():
        country_code = policy["country_code"]
        geography_id = get_geography_id(country_code)
        if not geography_id:
            logger.warning(f"No geography found in lookup for country code {country_code}")
            continue

        policy_type = policy["policy_type"]
        mapped_policy_type = CCLWActionType[policy_type].value
        action_type_id = get_type_id(mapped_policy_type)
        if not action_type_id:
            logger.warning(f"No action type found in lookup for policy type {policy_type}")
            continue

        if pandas.isnull(policy['policy_date']):
            logger.warning("Date is null for policy", policy)

        policy_date: datetime = policy['policy_date']

        action_payload = {
            "name": policy["policy_name"],
            "description": policy["description"],
            "year": policy_date.year,
            "month": policy_date.month,
            "day": policy_date.day,
            "geography_id": geography_id,
            "type_id": action_type_id,
            "source_id": 1,  # CCLW is source_id 1
            "documents": [],
        }

        response = post_action(action_payload)
        if response.status_code < 400:
            name = response.json()["name"]
            logger.info(f"Added action to database: {name}")
        else:
            logger.warning(f"Duplicate action: {policy_repr(policy)}", )
    logger.info("Done, %s policies imported" % [len(policies)])
