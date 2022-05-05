from os import PathLike
from typing import Union

import pandas as pd
from pandas import DataFrame

policy_fe_column_map = {
    "Title": "policy_name",
    "Geography ISO": "country_code",
    "Documents": "document_list",
    "Description": "policy_description",
    "Type": "policy_category",
    # metadata
    "Events": "events",
    "Sectors": "sectors",
    "Instruments": "instruments",
    "Frameworks": "frameworks",
    "Responses": "responses",
    "Natural Hazards": "hazards",
    "Document Types": "document_type",
}


def extract(csv_file: Union[str, PathLike]) -> DataFrame:
    """Loads a CCLW frontend-exported CSV.

    Also rename. some columns.

    :return: CSV data
    """

    cclw_policy_fe_df = pd.read_csv(
        csv_file, usecols=policy_fe_column_map.keys(), index_col=False
    )

    # rename the CSV columns as per the provided mappings
    cclw_policy_fe_df.rename(columns=policy_fe_column_map, inplace=True)

    return cclw_policy_fe_df
