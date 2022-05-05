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
SELECT
  source.name as action_source_name,
  doc.*,
  doc.id as document_id,
  doc.name as document_name,
  event.created_ts as action_date,
  doc_instr.instrument_id,
  doc_instr.parent_id as instrument_parent,
  doc_instr.name as instrument_name,
  doc_instr.description as instrument_description,
  doc_sect.sector_id,
  doc_sect.parent_id as sector_parent,
  doc_sect.name as sector_name,
  doc_sect.description as sector_description,
  doc_frmwrk.framework_id,
  doc_frmwrk.name as framework_name,
  doc_frmwrk.description as framework_description,
  doc_hzrd.hazard_id,
  doc_hzrd.name as hazard_name,
  doc_hzrd.description as hazard_description,
  geog.parent_id as geog_parent,
  geog.type as geog_type,
  geog.display_value as geog_display_value,
  geog.value as geography_code --world bank region not a 3 letter code.
FROM
  DOCUMENT doc
  LEFT JOIN event ON (doc.id = event.document_id)
  LEFT join source ON (source.id=doc.source_id)
  LEFT JOIN (
    SELECT
      *
    FROM
      document_instrument
      LEFT JOIN (
        SELECT
          *
        FROM
          instrument
      ) instrument ON (instrument.id = document_instrument.instrument_id)
  ) doc_instr ON (doc.id = doc_instr.document_id)
  LEFT JOIN (
    SELECT
      *
    FROM
      document_sector
      LEFT JOIN (
        SELECT
          *
        FROM
          sector
      ) sector ON (sector.id = document_sector.sector_id)
  ) doc_sect ON (doc.id = doc_sect.document_id)
  LEFT JOIN (
    SELECT
      *
    FROM
      document_framework
      LEFT JOIN (
        SELECT
          *
        FROM
          framework
      ) framework ON (framework.id = document_framework.framework_id)
  ) doc_frmwrk ON (doc.id = doc_frmwrk.document_id)
  LEFT JOIN (
    SELECT
      *
    FROM
      document_hazard
      LEFT JOIN (
        SELECT
          *
        FROM
          hazard
      ) hazard ON (hazard.id = document_hazard.hazard_id)
  ) doc_hzrd ON (doc.id = doc_hzrd.document_id)
  LEFT JOIN (
    SELECT
      *
    FROM
      geography
  ) geog ON doc.geography_id = geog.id
  LEFT JOIN (
    SELECT
      *
    FROM
      document_type
  ) document_type ON doc.type_id = document_type.id -- language not present? No foreign key.
WHERE
  event.description = 'The publication date'
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
