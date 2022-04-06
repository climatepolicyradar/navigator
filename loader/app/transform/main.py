import logging

from pandas import DataFrame

from app.model import PolicyLookup
from app.transform.util import get_policy_data

logger = logging.getLogger(__file__)


def transform(cclw_policy_fe_df: DataFrame) -> PolicyLookup:
    # Drop entries with no policy document list
    cclw_policy_fe_df.dropna(subset=["document_list"], inplace=True)

    policies: PolicyLookup = {}

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
