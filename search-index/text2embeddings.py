"""CLI to convert JSON documents outputted by the PDF parsing pipeline to embeddings."""

from pathlib import Path
import glob
import json
from typing import List, Optional, Dict, Union
import os
import re

from tqdm.auto import tqdm
import numpy as np
import click

from app.ml import SBERTEncoder, SentenceEncoder
from app.utils import paginate_list
from app.load_data import create_dataset
from app.db import PostgresConnector
from navigator.core.log import get_logger
from navigator.core.utils import get_timestamp

logger = get_logger(__name__)


def get_text_from_document_dict(
    document: dict,
) -> List[Dict[str, Union[str, int, List[List[float]]]]]:
    """Get the text and ID from each text block in a .json file created from a `Document` object.

    A string is created for a text block by newline-joining its list of text.

    Args:
        document (dict): dict created from a `Document` object, e.g. imported from a JSON file.

    Returns:
        List[Dict[str, Union[str, int, List[List[float]]]]]: dicts have keys 'text', 'text_block_id', 'coords', 'page_num'.
    """

    text_output = []

    for page in document["pages"]:
        for text_block in page["text_blocks"]:
            text_output.append(
                {
                    "text": "\n".join(text_block["text"]).strip(),
                    "text_block_id": text_block["text_block_id"],
                    "coords": text_block["coords"],
                    "page_num": int(
                        re.findall(r"p(\d+)_.*", text_block["text_block_id"])[0]
                    ),
                }
            )

    return text_output


def get_text_from_json_files(filepaths: List[str]) -> List[Dict[str, str]]:
    """Extract text, text block IDs and document IDs from JSON files created by the PDF parsing pipeline.

    Args:
        filepaths (List[str]): list of paths to JSON files outputted by the pdf2text CLI.

    Returns:
        List[Dict[str, str]]: dicts are {"text": "", "text_block_id": "", "document_id": ""}.
    """
    text_by_document = []

    for filepath in tqdm(filepaths):
        with open(filepath, "r") as f:
            document = json.load(f)

        document_text_and_ids = get_text_from_document_dict(document)

        for text_and_id in document_text_and_ids:
            text_and_id.update({"document_id": document["filename"]})
            text_by_document.append(text_and_id)

    return text_by_document


def encode_text_to_memmap(
    text_list: List[str],
    encoder: SentenceEncoder,
    batch_size: int,
    memmap_path: Path,
):
    """Encode list of text strings to a memmap file using a SentenceEncoder, in batches of `batch_size`.

    Args:
        text_list (List[str]): list of strings to encode.
        encoder (SentenceEncoder): sentence encoder.
        batch_size (int): size of batches to encode text in.
        memmap_path (Path): path to memmap file to write text embeddings to.
    """
    text_list_batched = paginate_list(text_list, batch_size)

    fp = np.memmap(
        memmap_path,
        dtype="float32",
        mode="w+",
        shape=(len(text_list), encoder.dimension),
    )

    for idx, batch in tqdm(
        enumerate(text_list_batched), unit="batch", total=len(text_list_batched)
    ):
        fp[idx * batch_size : (idx + 1) * batch_size, :] = encoder.encode_batch(
            batch, batch_size
        )

    fp.flush()


@click.command()
@click.option(
    "--input-dir",
    "-i",
    type=click.Path(exists=True, path_type=Path),
    required=True,
    help="Directory containing JSON files.",
)
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(exists=True, path_type=Path),
    required=True,
    help="Directory to save embeddings and IDs to.",
)
@click.option(
    "--model-name", "-m", type=str, help="Name of the sentence-BERT model to use."
)
@click.option("--batch-size", type=int, default=32, help="Batch size for encoding.")
@click.option(
    "--limit",
    type=int,
    default=None,
    help="Optionally limit the number of text samples to process. Useful for debugging.",
)
def run_cli(
    input_dir: Path,
    output_dir: Path,
    model_name: str,
    batch_size: int,
    limit: Optional[int],
):
    """Run CLI to produce embeddings from pdf2text JSON outputs. Encoding will automatically run on the GPU if one is available.

    Args:
        input_dir (Path): Directory containing JSON files
        output_dir (Path): Directory to save embeddings and IDs to
        model_name (str): Name of the sentence-BERT model to use. See https://www.sbert.net/docs/pretrained_models.html.
        batch_size (int): Batch size for encoding.
        limit (Optional[int]): Optionally limit the number of text samples to process. Useful for debugging.
    """
    logger.info(f"Getting text from JSONs in {input_dir}")
    curr_time = get_timestamp()
    json_filepaths = glob.glob(str(input_dir / "*.json"))

    text_and_ids = get_text_from_json_files(json_filepaths)
    if limit:
        text_and_ids = text_and_ids[:limit]

    logger.info(f"Loading sentence-transformer model {model_name}")
    encoder = SBERTEncoder(model_name)

    logger.info(f"Encoding text in batches of {batch_size}")
    text_by_document = [i["text"] for i in text_and_ids]
    # Export embeddings to numpy memmap file
    embs_output_path = (
        output_dir
        / f"embeddings_dim_{encoder.dimension}_{model_name}_{curr_time}.memmap"
    )
    encode_text_to_memmap(text_by_document, encoder, batch_size, embs_output_path)

    # Save text, text block IDs and document IDs to JSON file
    with open(output_dir / f"ids_{model_name}_{curr_time}.json", "w") as f:
        json.dump(text_and_ids, f)

    # Encode action descriptions
    postgres_connector = PostgresConnector(os.environ["DATABASE_URL"])
    navigator_dataset = create_dataset(postgres_connector)
    document_ids_processed = set([i["document_id"] for i in text_and_ids])
    description_data_to_encode = navigator_dataset.loc[
        navigator_dataset["prototype_filename_stem"].isin(document_ids_processed)
    ]

    logger.info(
        f"Encoding {len(description_data_to_encode)} descriptions in batches of {batch_size}"
    )
    description_embs_output_path = (
        output_dir
        / f"description_embs_dim_{encoder.dimension}_{model_name}_{curr_time}.memmap"
    )
    encode_text_to_memmap(
        description_data_to_encode["description"].tolist(),
        encoder,
        batch_size,
        description_embs_output_path,
    )

    description_ids_output_path = (
        output_dir / f"description_ids_{model_name}_{curr_time}.csv"
    )
    description_data_to_encode["prototype_filename_stem"].to_csv(
        description_ids_output_path, sep="\t", index=False, header=False
    )

    logger.info(f"Saved embeddings and IDs for text and descriptions to {output_dir}")


if __name__ == "__main__":
    run_cli()
