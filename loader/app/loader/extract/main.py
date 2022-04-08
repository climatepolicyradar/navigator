import os
from os import PathLike

import pandas as pd
from pandas import DataFrame

policy_fe_column_map = {
    "Title": "policy_name",
    "Geography ISO": "country_code",
    "Documents": "document_list",
    "Description": "policy_description",
    "Events": "events",
    "Type": "policy_type",
}


def extract(data_dir: PathLike) -> DataFrame:
    """Loads a CCLW frontend-exported CSV.

    Also rename. some columns.

    :return: CSV data
    """

    # find the un-processed CSV in the provided data folder
    csv_file = None
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            csv_file = os.path.join(root, file)
            break

    if not csv_file:
        raise Exception(f"CSV not found at path {data_dir}")

    cclw_policy_fe_df = pd.read_csv(
        csv_file, usecols=policy_fe_column_map.keys(), index_col=False
    )

    # rename the CSV columns as per the provided mappings
    cclw_policy_fe_df.rename(columns=policy_fe_column_map, inplace=True)

    return cclw_policy_fe_df
