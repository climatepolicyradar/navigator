from os import PathLike
from typing import Union

import pandas as pd
from pandas import DataFrame

csv_column_map = {
    "Id": "policy_id",  # for grouping related documents
    "Title": "document_name",
    "Geography ISO": "country_code",
    "Documents": "document_url",  # column is plural, but it will be only one document URL
    "Category": "category",
    # metadata
    "Events": "events",
    "Sectors": "sectors",
    "Instruments": "instruments",
    "Frameworks": "frameworks",
    "Responses": "responses",
    "Natural Hazards": "hazards",
    "Document Type": "document_type",
    "Year": "document_year",
    "Language": "document_language",
    "Keywords": "keywords",
    "policy_description": "description",
}


def extract(csv_file: Union[str, PathLike]) -> DataFrame:
    """Loads a CCLW frontend-exported CSV.

    Also rename. some columns.

    :return: CSV data
    """

    cclw_policy_fe_df = pd.read_csv(
        csv_file, usecols=csv_column_map.keys(), index_col=False
    )

    # rename the CSV columns as per the provided mappings
    cclw_policy_fe_df.rename(columns=csv_column_map, inplace=True)

    return cclw_policy_fe_df
