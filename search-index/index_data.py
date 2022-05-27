"""Index data into a running Opensearch index."""

import os
import re
from pathlib import Path
from typing import Generator, Dict

import pandas as pd
import numpy as np
import click

from navigator.core.log import get_logger
from app.db import PostgresConnector
from app.index import OpenSearchIndex
from app.load_data import get_data_from_navigator_tables

logger = get_logger(__name__)

CDN_URL: str = os.getenv("CDN_URL", "https://cdn.climatepolicyradar.org")


def s3_to_cdn_url(s3_url: str) -> str:
    """Convert a URL to a PDF in our s3 bucket to a URL to a PDF in our CDN.

    Args:
        s3_url (str): URL to a PDF in our s3 bucket.

    Returns:
        str: URL to a PDF in our CDN bucket.
    """

    return re.sub(r"https:\/\/.*\.s3\..*\.amazonaws.com", CDN_URL, s3_url)


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
    main_dataset["document_name_and_id"] = (
        main_dataset["document_name"] + " " + main_dataset["document_id"].astype(str)
    )

    main_dataset["document_date"] = main_dataset["document_date"].apply(
        lambda i: i.strftime("%d/%m/%Y")
    )
    main_dataset["document_description"] = main_dataset[
        "document_description"
    ].str.strip()

    main_dataset["document_url"] = main_dataset["document_url"].apply(s3_to_cdn_url)
    # --------------------------------------------------------------------------------------------

    metadata_columns = [
        "md5_sum",
        "document_url",
        "document_source_url",
        "document_id",
        "document_name",
        "document_date",
        "document_description",
        "document_category",
        "document_type",
        "document_keyword",
        "document_sector_name",
        "document_hazard_name",
        "document_instrument_name",
        "document_language",
        "document_instrument_parent",
        "document_framework_name",
        "document_response_name",
        "document_category",
        "document_name_and_id",
        "document_type",
        "document_country_code",
        "document_country_english_shortname",
        "document_region_english_shortname",
        "document_region_code",
        "document_source_name",
    ]

    # These columns are used to create one Opensearch document per CPR document, so that they're
    # searchable over as well as the text. Methods for these to be searched should be defined in
    # the index mapping.
    extra_text_columns = [
        "document_name",
        "document_description",
    ]

    for document_hash, description_embedding in description_embeddings_dict.items():
        doc_metadata_by_md5_hash = main_dataset.loc[
            main_dataset["md5_sum"] == document_hash
        ]

        if len(doc_metadata_by_md5_hash["document_id"].unique()) > 1:
            logger.warning(
                f"Found multiple documents with the same md5 sum: {document_hash}. Each will be processed separately, but these duplicates should be resolved manually.",
            )

        if len(doc_metadata_by_md5_hash) == 0:
            logger.warning(
                f"Skipping document {document_hash} as not in the Navigator database."
            )
            continue

        # We loop over multiple document IDs per md5 hash to accommodate for multiple documents in the database
        # that have the same md5 sum.
        for document_id, doc_metadata_by_id in doc_metadata_by_md5_hash.groupby(
            "document_id"
        ):
            doc_metadata_dict = {}

            for col in metadata_columns:
                metadata_values = doc_metadata_by_id[col].unique().tolist()
                metadata_values = [v for v in metadata_values if v and str(v) != "nan"]

                if len(metadata_values) == 1:
                    doc_metadata_dict[col] = metadata_values[0]
                else:
                    doc_metadata_dict[col] = metadata_values

            # We add the `for_search_` prefix to extra text fields we want made available to search,
            # as some of these will also be repeated over documents so they can be aggregated on.
            for text_col_name in extra_text_columns:
                text_col_dict = {
                    f"for_search_{text_col_name}": doc_metadata_by_id.iloc[
                        0, doc_metadata_by_id.columns.get_loc(text_col_name)
                    ]
                }

                if text_col_name == "document_description":
                    text_col_dict[
                        "document_description_embedding"
                    ] = description_embedding.tolist()

                yield dict(doc_metadata_dict, **text_col_dict)

            if document_hash in text_and_ids_data["document_md5_hash"].unique():
                text_and_ids_for_document = text_and_ids_data.loc[
                    text_and_ids_data["document_md5_hash"] == document_hash
                ]

                # TODO: we drop duplicates on text block ID here because the text extraction and embeddings generation produces
                # duplicate text and embeddings when there are multiple PDFs with the same MD5 hash. We should ideally handle this
                # earlier on in the pipeline.
                for idx, row in text_and_ids_for_document.drop_duplicates(
                    subset="text_block_id"
                ).iterrows():
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
        pd.DataFrame: contains columns 'text', 'text_block_id' and 'document_md5_hash'
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
@click.option("--index-no-replicas", "-r", type=int, default=2)
def run_cli(
    text_ids_path: Path,
    embeddings_path: Path,
    desc_ids_path: Path,
    desc_embeddings_path: Path,
    embedding_dim: int,
    index_no_replicas: int,
) -> None:
    """Index text and embeddings stores at `text-ids-path` and `embeddings-path` into Opensearch.

    Args:
        text_ids_path (Path): path to JSON file containing text and IDs.
        embeddings_path (Path): path to memmap file containing embeddings.
        desc_ids_path (Path): path to CSV file containing a document ID for each description.
        desc_embeddings_path (Path): path to memmap file containing description embeddings.
        embedding_dim (int): embedding dimension.
        index_no_replicas (int): number of replicas to create when indexing. Defaults to 2, which is a sensible number for a
        production three-node cluster: each primary shard has a replica on both other nodes.
    """
    postgres_connector = PostgresConnector(os.environ["BACKEND_DATABASE_URL"])
    main_dataset = get_data_from_navigator_tables(postgres_connector)

    ids_table = load_text_and_ids_json(text_ids_path)
    embs = load_embeddings(embeddings_path, embedding_dim=embedding_dim)
    description_embs_dict = load_description_embeddings_and_metadata(
        desc_embeddings_path, desc_ids_path, embedding_dim=embedding_dim
    )
    doc_generator = get_document_generator(
        main_dataset, ids_table, embs, description_embs_dict
    )

    def _convert_to_bool(x):
        if x.lower() == "true":
            return True
        elif x.lower() == "false":
            return False

    opensearch = OpenSearchIndex(
        url=os.environ["OPENSEARCH_URL"],
        username=os.environ["OPENSEARCH_USER"],
        password=os.environ["OPENSEARCH_PASSWORD"],
        index_name=os.environ["OPENSEARCH_INDEX"],
        # TODO: convert to env variables?
        opensearch_connector_kwargs={
            "use_ssl": _convert_to_bool(os.environ["OPENSEARCH_USE_SSL"]),
            "verify_certs": _convert_to_bool(os.environ["OPENSEARCH_VERIFY_CERTS"]),
            "ssl_show_warn": _convert_to_bool(os.environ["OPENSEARCH_SSL_WARNINGS"]),
        },
        embedding_dim=int(os.environ["OPENSEARCH_INDEX_EMBEDDING_DIM"]),
    )
    opensearch.delete_and_create_index(n_replicas=index_no_replicas)
    # We disable index refreshes during indexing to speed up the indexing process,
    # and to ensure only 1 segment is created per shard. This also speeds up KNN
    # queries and aggregations according to the Opensearch and Elasticsearch docs.
    opensearch.set_index_refresh_interval(-1, timeout=60)
    opensearch.bulk_index(actions=doc_generator)

    # TODO: we wrap this in a try/except block because for now because sometimes it times out
    # and we don't want the whole >1hr indexing process to fail if this happens.
    # We should stop doing this when we care what the refresh interval is, i.e. when we plan
    # on incrementally adding data to the index.
    try:
        # 1 second refresh interval is the Opensearch default
        opensearch.set_index_refresh_interval(1, timeout=60)
    except Exception as e:
        logger.info(f"Failed to set index refresh interval after indexing: {e}")

    opensearch.warmup_knn()


if __name__ == "__main__":
    run_cli()
