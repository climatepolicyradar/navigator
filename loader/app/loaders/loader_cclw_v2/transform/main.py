import logging

import numpy as np
from pandas import DataFrame

from app.loaders.loader_cclw_v2.transform.util import get_policy_data
from app.model import PolicyLookup

logger = logging.getLogger(__file__)


def transform(cclw_policy_fe_df: DataFrame) -> PolicyLookup:
    policies: PolicyLookup = {}

    cclw_policy_fe_df = cclw_policy_fe_df.replace({np.nan: ""})

    for policy_id, groupby_df in cclw_policy_fe_df.groupby("policy_id"):

        result = get_policy_data(policy_id, groupby_df)

        if result is None:
            continue
        key, policy_data = result
        if key in policies:
            logger.warning(f"Already have data for policy {key}")
        else:
            policies[key] = policy_data

    return policies
