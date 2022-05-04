import logging

from pandas import DataFrame
import numpy as np
from app.model import PolicyLookup
from app.loaders.loader.transform.util import get_policy_data

logger = logging.getLogger(__file__)


def transform(cclw_policy_fe_df: DataFrame) -> PolicyLookup:
    # Drop entries with no policy document list
    cclw_policy_fe_df.dropna(subset=["document_list"], inplace=True)

    policies: PolicyLookup = {}

    cclw_policy_fe_df = cclw_policy_fe_df.replace({np.nan: ""})

    for d_ix, d in cclw_policy_fe_df.iterrows():
        result = get_policy_data(d, sep=";", sub_sep="|")
        if result is None:
            continue
        key, policy_data = result
        if key in policies:
            logger.warning(f"Already have data for policy {key}")
        else:
            policies[key] = policy_data

    return policies
