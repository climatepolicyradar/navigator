"""Functions to load data from database."""

from pathlib import Path

import pandas as pd

from app.db import PostgresConnector


def get_data_from_navigator_tables(
    postgres_connector: PostgresConnector,
) -> pd.DataFrame:
    """Get data from Navigator tables. Includes documents, actions, countries, languages, action sources and action types.

    Returns:
        pd.DataFrame: one row per document.
    """
    query = """
        SELECT document_id, source_url, s3_url, document.language_id as document_language_id, document.name AS document_name, action.*, language.language_id, language.language_code, language.name as language_name, \
        geography.*, source.source_id, source.name as action_source_name, action_type.action_type_id, action_type.type_name as action_type_name, action.name as action_name, action.description as action_description, \
        geography.country_code as action_country_code, geography.english_shortname as action_geography_english_shortname
        FROM document
        INNER JOIN action ON (document.action_id = action.action_id)
        LEFT JOIN language on (document.language_id = language.language_id)
        LEFT JOIN geography on (action.geography_id = geography.geography_id)
        LEFT JOIN source on (action.action_source_id = source.source_id)
        LEFT JOIN action_type on (action.action_type_id = action_type.action_type_id);
        """

    return postgres_connector.run_query(query)


def ensure_safe(url: str) -> str:
    """Ensure a URL is safe.

    Some documents use http, not https. Instead of just ignoring those,
    we'll try download a doc securely, if possible.

    # TODO: this function is also used in the loader. We use it here to repeat that transformation for a successful join. Do we care that it's copy & pasted?
    """
    if "https://" not in url:
        url = url.replace("http://", "https://")
    return url


def make_url_filename_join_table_from_prototype_data() -> pd.DataFrame:
    """Make a join table which joins document URLs in the navigator database with filenames used in the prototype.

    # TODO: this is temporary and should be removed once the PDFs are hosted somewhere.

    Returns:
        pd.DataFrame: join table
    """

    url_old_id_join = (
        pd.read_csv(
            "./data/processed_policies.csv",
            index_col=0,
            usecols=["policy_content_file", "url"],
        )
        .reset_index()
        .dropna()
    )
    url_old_id_join["prototype_filename_stem"] = url_old_id_join[
        "policy_content_file"
    ].apply(lambda filename: Path(filename).stem)
    url_old_id_join = url_old_id_join.drop(columns=["policy_content_file"])
    url_old_id_join = url_old_id_join.loc[
        url_old_id_join["prototype_filename_stem"].str.startswith("cclw"), :
    ]
    # Convert http URLs to https, as this is what the loader does
    url_old_id_join["url"] = url_old_id_join["url"].apply(ensure_safe)

    return url_old_id_join


def create_dataset(postgres_connector: PostgresConnector) -> pd.DataFrame:
    """Create a dataset which joins data from Navigator tables with filenames from the prototype.

    # TODO: once PDFs are hosted somewhere, we can refactor this pipeline to remove its dependency on the processed_policies.csv file.

    Returns:
        pd.DataFrame
    """

    navigator_data = get_data_from_navigator_tables(postgres_connector)
    prototype_url_join = make_url_filename_join_table_from_prototype_data()

    return pd.merge(
        left=navigator_data,
        right=prototype_url_join,
        how="left",
        left_on="source_url",
        right_on="url",
    )
