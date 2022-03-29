"""CLI to convert JSON documents outputted by the PDF parsing pipeline to embeddings."""

from pathlib import Path
import glob
import json
from typing import List, Tuple, Optional

from tqdm.auto import tqdm
import numpy as np
import pandas as pd
import click

from app.ml import SBERTEncoder, SentenceEncoder
from app.utils import paginate_list
from navigator.core.log import get_logger
from navigator.core.utils import get_timestamp

logger = get_logger(__name__)


def get_text_from_document_dict(document: dict) -> List[Tuple[str, str]]:
    """Get the text and ID from each text block in a .json file created from a `Document` object.

    A string is created for a text block by newline-joining its list of text.

    Args:
        document (dict): dict created from a `Document` object, e.g. imported from a JSON file.

    Returns:
        List[Tuple[str, str]]: list of (text, text_block_id) tuples.
    """

    text_output = []

    for page in document["pages"]:
        for text_block in page["text_blocks"]:
            text_output.append(
                ("\n".join(text_block["text"]).strip(), text_block["text_block_id"])
            )

    return text_output


def get_text_from_json_files(filepaths: List[str]) -> List[Tuple[str, str, str]]:
    """Extract text, text block IDs and document IDs from JSON files created by the PDF parsing pipeline.

    Args:
        filepaths (List[str]): list of paths to JSON files outputted by the pdf2text CLI.

    Returns:
        List[Tuple[str, str, str]]: tuples of (text, text_id, document_filename).
    """
    text_by_document = []

    for filepath in tqdm(filepaths):
        with open(filepath, "r") as f:
            document = json.load(f)

        document_text_and_ids = get_text_from_document_dict(document)
        document_filename = document["filename"]
        for text, _id in document_text_and_ids:
            text_by_document.append((text, _id, document_filename))

    return text_by_document


def encode_text(
    text_list: List[str], encoder: SentenceEncoder, batch_size: int
) -> np.ndarray:
    """Encode list of text strings using a SentenceEncoder, in batches of `batch_size`

    Args:
        text_list (List[str]): list of strings to encode.
        encoder (SentenceEncoder): sentence encoder.
        batch_size (int): size of batches to encode text in.

    Returns:
        np.ndarray: each row of the array corresponds to the embedding of a string in `text_list`
    """
    text_list_batched = paginate_list(text_list, batch_size)

    emb_list = []

    for batch in tqdm(text_list_batched, unit="batch"):
        embeddings = encoder.encode_batch(batch, batch_size)
        emb_list.append(embeddings)

    return np.vstack(emb_list)


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
    text_by_document = [i[0] for i in text_and_ids]
    embs = encode_text(text_by_document, encoder, batch_size=batch_size)

    # Export embeddings to numpy memmap file
    embs_output_path = (
        output_dir / f"embeddings_dim_{embs.shape[1]}_{model_name}_{curr_time}.memmap"
    )
    fp = np.memmap(embs_output_path, dtype="float32", mode="w+", shape=embs.shape)
    fp[:] = embs[:]
    fp.flush()

    # Save text, text block IDs and document IDs to CSV
    # TODO: is there a better way to save text than in a CSV?
    pd.DataFrame(text_and_ids).to_csv(
        output_dir / f"ids_{model_name}_{curr_time}.csv",
        sep=",",
        header=False,
        index=False,
    )
    logger.info(f"Saved embeddings and IDs to {output_dir}")


if __name__ == "__main__":
    run_cli()
