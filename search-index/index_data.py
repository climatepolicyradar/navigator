"""Index data into a running Opensearch index."""

import os
from pathlib import Path
from typing import Generator

import pandas as pd
import numpy as np
import click

from navigator.core.log import get_logger
from app.db import PostgresConnector
from app.index import OpenSearchIndex

logger = get_logger(__name__)

DATABASE_URL = os.environ["DATABASE_URL"]
postgres_connector = PostgresConnector(DATABASE_URL)


def get_data_from_navigator_tables() -> pd.DataFrame:
    """Get data from Navigator tables. Includes documents, actions, countries, languages, action sources and action types.

    Returns:
        pd.DataFrame: one row per document.
    """
    query = """
        SELECT document_id, source_url, s3_url, document.language_id as document_language_id, document.name AS document_name, action.*, language.language_id, language.language_code, language.name as language_name, \
        geography.*, source.source_id, source.name as action_source_name, action_type.action_type_id, action_type.type_name as action_type_name
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


def create_dataset() -> pd.DataFrame:
    """Create a dataset which joins data from Navigator tables with filenames from the prototype.

    # TODO: once PDFs are hosted somewhere, we can refactor this pipeline to remove its dependency on the processed_policies.csv file.

    Returns:
        pd.DataFrame: _description_
    """

    navigator_data = get_data_from_navigator_tables()
    prototype_url_join = make_url_filename_join_table_from_prototype_data()

    return pd.merge(
        left=navigator_data,
        right=prototype_url_join,
        how="left",
        left_on="source_url",
        right_on="url",
    )


def get_document_generator(
    main_dataset: pd.DataFrame, text_and_ids_data: pd.DataFrame, embeddings: np.ndarray
) -> Generator[dict, None, None]:
    """Get generator of documents to index in Opensearch.

    Args:
        main_dataset (pd.DataFrame): dataframe returned by `create_dataset` function.
        text_and_ids_data (pd.DataFrame): dataframe returned by `load_text_and_ids_csv` function.
        embeddings (np.ndarray): numpy array returned by `load_embeddings` function.

    Yields:
        Generator[dict, None, None]: generator of dictionaries per text passage to index.
    """

    metadata_columns = [
        "document_id",
        "document_language_id",
        "document_name",
        "action_id",
        "name",
        "description",
        "action_date",
        "country_code",
        "action_source_name",
        "action_type_name",
    ]

    for document_id, document_df in text_and_ids_data.groupby("document_id"):
        doc_metadata = main_dataset.loc[
            main_dataset["prototype_filename_stem"] == document_id
        ]
        doc_metadata_dict = doc_metadata[metadata_columns].iloc[0].to_dict()
        doc_metadata_dict = {
            k: v for k, v in doc_metadata_dict.items() if v and str(v) != "nan"
        }
        doc_metadata_dict["action_date"] = doc_metadata_dict["action_date"].strftime(
            "%d/%m/%Y"
        )

        for idx, row in document_df.iterrows():
            text_block_dict = {
                "text_block_id": row.text_block_id,
                "text": row.text,
                "text_embedding": embeddings[idx, :].tolist(),
            }

            yield dict(doc_metadata_dict, **text_block_dict)


def load_text_and_ids_csv(ids_path: Path) -> pd.DataFrame:
    """Load CSV file containing text and IDs that's produced alongside the embeddings.

    Args:
        ids_path (Path): path to CSV file.

    Returns:
        pd.DataFrame: contains columns 'text', 'text_block_id' and 'document_id'
    """
    return pd.read_csv(
        ids_path, header=None, names=["text", "text_block_id", "document_id"]
    )


def load_embeddings(embs_path: Path, embedding_dim: int) -> np.ndarray:
    """Load embeddings from memmap file.

    Args:
        embs_path (Path): path to memmap file.
        embedding_dim (int): dimension of embeddings.

    Returns:
        np.ndarray
    """
    return np.memmap(embs_path, dtype="float32", mode="r").reshape((-1, embedding_dim))


@click.command()
@click.option("--text-ids-path", type=click.Path(exists=True), required=True)
@click.option("--embeddings-path", type=click.Path(exists=True), required=True)
@click.option("--embedding-dim", "-d", type=int, required=True)
def run_cli(text_ids_path: Path, embeddings_path: Path, embedding_dim: int) -> None:
    main_dataset = create_dataset()

    ids_table = load_text_and_ids_csv(text_ids_path)
    embs = load_embeddings(embeddings_path, embedding_dim=embedding_dim)
    doc_generator = get_document_generator(main_dataset, ids_table, embs)

    opensearch = OpenSearchIndex(
        # TODO: convert to env variables
        url="http://localhost:9200",
        username="admin",
        password="admin",
        index_name="navigator",
        opensearch_connector_kwargs={
            "use_ssl": False,
            "verify_certs": False,
            "ssl_show_warn": False,
        },
        embedding_dim=embedding_dim,
    )

    opensearch.delete_and_create_index()
    opensearch.bulk_index(actions=doc_generator)


if __name__ == "__main__":
    run_cli()
