"""Index data into a running Opensearch index."""

import os
from pathlib import Path
from typing import Generator, Dict

import pandas as pd
import numpy as np
import click

from navigator.core.log import get_logger
from app.db import PostgresConnector
from app.index import OpenSearchIndex
from app.load_data import create_dataset

logger = get_logger(__name__)


def get_document_generator(
    main_dataset: pd.DataFrame,
    text_and_ids_data: pd.DataFrame,
    embeddings: np.ndarray,
    description_embeddings_dict: Dict[str, np.ndarray],
) -> Generator[dict, None, None]:
    """Get generator of documents to index in Opensearch.

    An Opensearch document is created for each text block in each document. For each document, an
    Opensearch document is also created for its title and description.

    Args:
        main_dataset (pd.DataFrame): dataframe returned by `create_dataset` function.
        text_and_ids_data (pd.DataFrame): dataframe returned by `load_text_and_ids_csv` function.
        embeddings (np.ndarray): numpy array returned by `load_embeddings` function.
        description_embeddings_dict (Dict[str, np.ndarray]): dictionary of description IDs and embeddings.

    Yields:
        Generator[dict, None, None]: generator of dictionaries per text passage to index.
    """

    # DATA TRANSFORMATION STEPS. We may want to put these in another method.
    # Create name_and_id field to group by and sort on in Elasticsearch aggregation.
    # TODO: this needs to be a combination of document name and document ID when we remove
    # the concept of actions.
    main_dataset["action_name_and_id"] = (
        main_dataset["action_name"] + " " + main_dataset["document_id"].astype(str)
    )

    main_dataset["action_date"] = main_dataset["action_date"].apply(
        lambda i: i.strftime("%d/%m/%Y")
    )
    main_dataset["action_description"] = main_dataset["action_description"].str.strip()

    # --------------------------------------------------------------------------------------------

    metadata_columns = [
        "document_id",
        "document_language_id",
        "document_name",
        "action_id",
        "action_date",
        "action_name",
        "action_description",
        "action_name_and_id",
        "action_country_code",
        "action_geography_english_shortname",
        "action_source_name",
        "action_type_name",
    ]

    # These columns are used to create one Opensearch document per CPR document, so that they're
    # searchable over as well as the text. Methods for these to be searched should be defined in
    # the index mapping.
    extra_text_columns = [
        "action_name",
        "action_description",
    ]

    for document_id, document_df in text_and_ids_data.groupby("document_id"):

        doc_metadata = main_dataset.loc[
            main_dataset["prototype_filename_stem"] == document_id
        ]
        if len(doc_metadata) == 0:
            logger.warning(
                f"Skipping document {document_id} as not in the Navigator database."
            )
            continue

        doc_metadata_dict = doc_metadata[metadata_columns].iloc[0].to_dict()
        doc_metadata_dict = {
            k: v for k, v in doc_metadata_dict.items() if v and str(v) != "nan"
        }

        doc_description_embedding = description_embeddings_dict.get(document_id)
        if doc_description_embedding is None:
            logger.warning(
                f"No description embedding has been generated for document {document_id}. Skipping adding the embedding to Opensearch, which will likely result in unexpected search results."
            )

        # We add the `for_search_` prefix to extra text fields we want made available to search,
        # as some of these will also be repeated over documents so they can be aggregated on.
        for text_col_name in extra_text_columns:
            text_col_dict = {
                f"for_search_{text_col_name}": doc_metadata.iloc[
                    0, doc_metadata.columns.get_loc(text_col_name)
                ]
            }

            if (text_col_name == "action_description") and (
                doc_description_embedding is not None
            ):
                text_col_dict[
                    "action_description_embedding"
                ] = doc_description_embedding.tolist()

            yield dict(doc_metadata_dict, **text_col_dict)

        for idx, row in document_df.iterrows():
            text_block_dict = {
                "text_block_id": row.text_block_id,
                "text": row.text,
                "text_embedding": embeddings[idx, :].tolist(),
                "text_block_coords": row.coords,
                "text_block_page": row.page_num,
            }

            yield dict(doc_metadata_dict, **text_block_dict)


def load_text_and_ids_json(ids_path: Path) -> pd.DataFrame:
    """Load JSON file containing text and IDs that's produced alongside the embeddings.

    Args:
        ids_path (Path): path to JSON file.

    Returns:
        pd.DataFrame: contains columns 'text', 'text_block_id' and 'document_id'
    """

    data = pd.read_json(ids_path, orient="records")

    if isinstance(data, pd.DataFrame):
        return data

    else:
        raise ValueError("Expected dataframe")  # Won't happen due to our data format


def load_embeddings(embs_path: Path, embedding_dim: int) -> np.ndarray:
    """Load embeddings from memmap file.

    Args:
        embs_path (Path): path to memmap file.
        embedding_dim (int): dimension of embeddings.

    Returns:
        np.ndarray
    """
    return np.memmap(embs_path, dtype="float32", mode="r").reshape((-1, embedding_dim))


def load_description_embeddings_and_metadata(
    embs_path: Path, ids_path: Path, embedding_dim: int
) -> Dict[str, np.ndarray]:
    """Load description embeddings and metadata from memmap and CSV files outputted by the text2embeddings CLI.

    Args:
        embs_path (Path): path to memmap file containing description embeddings.
        ids_path (Path): path to CSV file containing a document ID for each description.
        embedding_dim (int): embedding dimension.

    Returns:
        Dict[str, np.ndarray]: {'document_id': [embeddings], ...}
    """

    embs = load_embeddings(embs_path, embedding_dim)
    metadata = pd.read_csv(ids_path, header=None, names=["document_id"])

    output_dict = dict()

    for idx, doc_id in metadata["document_id"].items():
        output_dict[doc_id] = embs[idx, :]

    return output_dict


@click.command()
@click.option("--text-ids-path", type=click.Path(exists=True), required=True)
@click.option("--embeddings-path", type=click.Path(exists=True), required=True)
@click.option("--desc-ids-path", type=click.Path(exists=True), required=True)
@click.option("--desc-embeddings-path", type=click.Path(exists=True), required=True)
@click.option("--embedding-dim", "-d", type=int, required=True)
def run_cli(
    text_ids_path: Path,
    embeddings_path: Path,
    desc_ids_path: Path,
    desc_embeddings_path: Path,
    embedding_dim: int,
) -> None:
    """Index text and embeddings stores at `text-ids-path` and `embeddings-path` into Opensearch.

    Args:
        text_ids_path (Path): path to JSON file containing text and IDs.
        embeddings_path (Path): path to memmap file containing embeddings.
        desc_ids_path (Path): path to CSV file containing a document ID for each description.
        desc_embeddings_path (Path): path to memmap file containing description embeddings.
        embedding_dim (int): embedding dimension.
    """
    postgres_connector = PostgresConnector(os.environ["DATABASE_URL"])
    main_dataset = create_dataset(postgres_connector)

    ids_table = load_text_and_ids_json(text_ids_path)
    embs = load_embeddings(embeddings_path, embedding_dim=embedding_dim)
    description_embs_dict = load_description_embeddings_and_metadata(
        desc_embeddings_path, desc_ids_path, embedding_dim=embedding_dim
    )
    doc_generator = get_document_generator(
        main_dataset, ids_table, embs, description_embs_dict
    )

    opensearch = OpenSearchIndex(
        url=os.environ["OPENSEARCH_URL"],
        username=os.environ["OPENSEARCH_USER"],
        password=os.environ["OPENSEARCH_PASSWORD"],
        index_name=os.environ["OPENSEARCH_INDEX"],
        # TODO: convert to env variables?
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
