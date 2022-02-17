"""
An data module which knows where and how to get action URLs (e.g. CSVs of URLs).
These URLs are then passed onto a downloader which will fetch the actions.
"""
from os import PathLike
import pandas as pd

from app.model import IngestData

policy_fe_column_map = {
    'Title': 'policy_name',
    'Geography ISO': 'country_code',
    'Documents': 'document_list',
    'Description': 'policy_description',
    'Events': 'events',
}

policy_column_map = {
    'Id': 'source_policy_id',
    'Title': 'policy_name',
    'Legislation type': 'policy_type',
    'Geography iso': 'country_code',
    'Sectors': 'sector_list',
    'Keywords': 'keyword_list',
    'Document types': 'document_type_list',
}

doc_column_map = {
    'Id': 'document_id',
    'Documentable id': 'source_policy_id',
    'Name': 'document_name',
    'External url': 'document_url',
    'Language': 'document_language',
}

targets_column_map ={
    'Id': 'target_id',
    'Legislation ids': 'policy_id',
    'Target type': 'target_type',
    'Source': 'target_policy_type',
    'Description': 'target_description',
    'Ghg target': 'is_ghg_target',
    'Year': 'target_year',
    'Base year period': 'target_base_year',
    'Single year': 'target_single_year',
    'Geography iso': 'target_country_code',
    'Sector': 'target_sector',
    'Scopes': 'target_scope_list',
}


def extract(data_dir: PathLike) -> IngestData:
    """
    Loads a related collection of CCLW CSVs, and does initial transformation:
    - rename some columns
    - drop entries without URLs

    :return: CSV data
    """
    

    # the backend CSV is normalised
    cclw_policy_df = pd.read_csv(
        data_dir / 'cclw' / '2022-02' / 'legislations-16_02_2022.csv',
        usecols=policy_column_map.keys(),
        index_col=False
    )

    cclw_doc_df = pd.read_csv(
        data_dir / 'cclw' / '2022-02' / 'documents-16_02_2022.csv',
        usecols=doc_column_map.keys(),
        index_col=False
    )

    cclw_target_df = pd.read_csv(
        data_dir / 'cclw' / '2022-02' / 'targets-16_02_2022.csv',
        usecols=targets_column_map,
        index_col=False
    )

    # Unfortunately, we also need to another cclw dataset which has been exported from the user
    # front end. This is because the "documents" dataset only includes documents linked on
    # external websites, and not documents stored in cclw blob storage! This dataset also does not
    # include the internal policy id, so we will need to match these datasets by policy title :/

    cclw_policy_fe_df = pd.read_csv(
        data_dir / 'cclw' / '2022-02' / 'laws_and_policies_16022022.csv',
        usecols=policy_fe_column_map.keys(),
        index_col=False
    )

    # rename the CSV columns as per the provided mappings
    cclw_policy_fe_df.rename(columns=policy_fe_column_map, inplace=True)
    cclw_policy_df.rename(columns=policy_column_map, inplace=True)
    cclw_doc_df.rename(columns=doc_column_map, inplace=True)
    cclw_target_df.rename(columns=targets_column_map, inplace=True)

    data = IngestData(
        policies=cclw_policy_df,
        docs=cclw_doc_df,
        targets=cclw_target_df,
        policies_fe=cclw_policy_fe_df,
    )
    return data
