"""
From https://github.com/climatepolicyradar/cpr/blob/master/nbs/policy-etl.ipynb

This module assumes the presence of CCLW CSVs in a known local location.

The CSVs contain hints (URLs) where actions and documents can be found.
These hints would normally

"""
import pandas as pd
from pandas import DataFrame

from app.model import IngestData
from app.transform.datafixes import add_missing_dates
from app.transform.util import get_urls, extract_date


def transform(data: IngestData) -> DataFrame:
    cclw_policy_fe_df = data.policies_fe

    # Drop entries with no policy document list
    cclw_policy_fe_df.dropna(subset=['document_list'], inplace=True)

    all_docs = []
    for d_ix, d in cclw_policy_fe_df.iterrows():
        all_docs += get_urls(d, sep=';', sub_sep='|')

    cclw_doc_urls = pd.DataFrame(all_docs)

    # Merge policy and document datasets
    policies = pd.merge(
        data.policies,
        cclw_doc_urls,
        left_on=['country_code', 'policy_name'],
        right_on=['country_code', 'policy_name'],
        how='left'
    )

    # Drop nulls
    policies.dropna(subset=['doc_url'], inplace=True)

    # Drop policies referencing the same url
    policies.drop_duplicates(subset='doc_url', inplace=True)

    # get the date when the policy was approved (or law passed)
    policies['events'] = policies['events'].map(extract_date)
    policies.rename(columns={'events': 'policy_date'}, inplace=True)

    add_missing_dates(policies)

    # Reindex policies to make sure we have a unique id for each document
    policies.index = range(0, len(policies))

    return policies
