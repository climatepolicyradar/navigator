import pandas as pd
from pandas import DataFrame

from app.transform.datafixes import add_missing_dates
from app.transform.util import get_urls, extract_date


def transform(cclw_policy_fe_df: DataFrame) -> DataFrame:
    # Drop entries with no policy document list
    cclw_policy_fe_df.dropna(subset=['document_list'], inplace=True)

    all_docs = []
    for d_ix, d in cclw_policy_fe_df.iterrows():
        all_docs += get_urls(d, sep=';', sub_sep='|')

    policies = pd.DataFrame(all_docs)

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
