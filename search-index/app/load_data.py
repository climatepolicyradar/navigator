"""Functions to load data from database."""


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
        doc.md5_sum as md5_sum,
        doc.url AS document_url,
        doc.source_url AS document_source_url,
        source.name as document_source_name,
        doc.id as document_id,
        doc.name as document_name,
        doc.description as document_description,
        kwd.name as document_keyword,
        doc_cat.name as document_category,
        doc_cat.description as document_category_description,
        doc_type.name as document_type,
        doc_type.description as document_type_description,
        event.created_ts as document_date,
        doc_instr.instrument_id,
        doc_instr.parent_id as document_instrument_parent,
        doc_instr.name as document_instrument_name,
        doc_instr.description as instrument_description,
        doc_sect.sector_id,
        doc_sect.parent_id as sector_parent,
        doc_sect.name as document_sector_name,
        doc_sect.description as sector_description,
        doc_frmwrk.framework_id,
        doc_frmwrk.name as document_framework_name,
        doc_frmwrk.description as framework_description,
        doc_hzrd.hazard_id,
        doc_hzrd.name as document_hazard_name,
        doc_hzrd.description as hazard_description,
        doc_rspnse.response_id,
        doc_rspnse.name as document_response_name,
        doc_rspnse.description as response_description,
        geog_country.parent_id as geog_parent,
        geog_country.type as geog_type,
        geog_country.display_value as document_country_english_shortname,
        geog_country.value as document_country_code,
        geog_region.display_value as document_region_english_shortname,
        geog_region.value as document_region_code,
        doc_lang.name as document_language
      FROM
        DOCUMENT doc
        LEFT JOIN event ON (doc.id = event.document_id)
        LEFT join source ON (source.id = doc.source_id)
        LEFT JOIN document_type doc_type ON doc.type_id = doc_type.id
        LEFT JOIN category doc_cat ON doc.category_id = doc_cat.id
        LEFT JOIN document_keyword doc_keyword ON doc.id = doc_keyword.document_id
        LEFT JOIN keyword kwd ON doc_keyword.keyword_id = kwd.id
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
            document_language
            LEFT JOIN (
              SELECT
                *
              FROM
                language
            ) lang ON (lang.id = document_language.language_id)
        ) doc_lang ON (doc.id = doc_lang.document_id)
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
            document_response
            LEFT JOIN (
              SELECT
                *
              FROM
                response
            ) response ON (response.id = document_response.response_id)
        ) doc_rspnse ON (doc.id = doc_rspnse.document_id)
        LEFT JOIN (
          SELECT
            *
          FROM
            geography
          WHERE
            type = 'ISO-3166'
        ) geog_country ON doc.geography_id = geog_country.id
        LEFT JOIN (
          SELECT
            *
          FROM
            geography
          WHERE
            type = 'World Bank Region'
        ) geog_region ON geog_country.parent_id = geog_region.id
      WHERE
        event.description = 'The publication date' AND url IS NOT NULL
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
