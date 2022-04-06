"""CLI to convert JSON documents outputted by the PDF parsing pipeline to embeddings."""

from pathlib import Path
import glob
import json
from typing import List, Tuple, Optional

from tqdm.auto import tqdm
import numpy as np
import pandas as pd
import click
import re

from app.ml import SBERTEncoder, SentenceEncoder
from app.utils import paginate_list
from navigator.core.log import get_logger
from navigator.core.utils import get_timestamp

logger = get_logger(__name__)


def get_text_from_list(text_block: dict, prev_processed_text_block: dict) -> str:
    """
    Format a list text block and prepend it to the previous text block, assuming it is the context of the list.
    This is a fairly strong assumption, but works most of the time. Code to handle more complex cases has been started.

    Args:
        text_block (dict): text block dict.
        prev_processed_text_block (dict): previous text block dict.

    Returns:
        str: Formatted list text block that is useful for indexing semantics.
    """
    text = text_block["custom_attributes"]["pretty_list_string"]
    # Note, it was decided to leave most of the formatting and use custom analysers in elasticsearch to handle
    # formatting. This makes this function unnecessary, but I've left it here in case we want something more later.
    text = text.strip()
    # Always append previous text block as context. This is a fairly strong assumption, and the code to make this
    # better has been started, in postprocessor.py, but is not yet completely robust, so we are not using it for now.
    # TODO: Note, we can potentially do this in a more robust way by using the text block custom attributes created
    #  in postprocessor.py, which I've updated. This will allow us to deal with edge cases, for example where the
    #  previous block is not either context or part of the same list from the previous page. This would be the case
    #  when, for example, there are random elements between pages that the postprocessors haven't been able to catch.
    #  But I've ignored this for now because it seems that the postprocessing in postprocessor.py has dealt with the
    #  vast majority of edge cases (as indicated by the rarity of certain debugging metadata).
    text = prev_processed_text_block + "\n" + text
    return text


def delete_string_indices(data: str, indices: List[int]) -> str:
    """Delete a list of indices from a string.
    Args:
        data (str): string to delete indices from.
        indices (List[int]): list of indices to delete.
    Returns:
        str: string with indices deleted.
    """
    return "".join([char for idx, char in enumerate(data) if idx not in indices])


def get_text_from_merged_block(text_block: dict) -> str:
    """
    Remove unnecessary styling from merged text blocks (superscripts).

    Args:
        text_block: A block of text that has been merged.

    Returns:
        str: The text block with styling that is not related to semantics removed.

    """
    # Text output with no processing.
    if len(text_block["text"]) >1:
        breakpoint()
    text_output = (
        "".join(text_block["text"]).strip(),
        text_block["text_block_id"],
    )
    # Remove superscripts only. Bolding has no impact on the block's content once merged, so we don't need to remove
    # anything. Subscripts are kept because, for example, we want to keep CO2 even when it is subscripted).
    # Superscripts are almost always references not related to semantics, so we can remove them.
    try:
        style_spans = text_block["custom_attributes"]["styleSpans"]
        delete_indices = []
        for style_span in style_spans:
            if style_span["style"] == "superscript":
                remove_start = style_span["start_idx"]
                remove_end = style_span["end_idx"]
                # if superscript is of the form st, nd, rd, th, do not remove as this can potentially
                # be used by language models.
                delete_substr = text_output[0][remove_start : remove_end + 1]
                if re.match(r"(st|nd|rd|th)$", delete_substr):
                    continue  # don't remove
                delete_indices.extend(list(range(remove_start, remove_end)))

        # The indices are relative to the whole block, not just elements in the block.
        # Remove the indices from deleted_indices from text_output.
        if delete_indices:  # There will only be indices to delete in superscript case.
            text_output_amended = delete_string_indices(text_output[0], delete_indices)
            text_output = (text_output_amended, text_block["text_block_id"])
            return text_output
        else:
            return text_output
    # Blocks are sometimes merged by the styling processor for rare reasons other
    # than style, in which case there is no stylespan attribute, hence this exception handling.
    # This happens when, for example, there is a block with a unique path between two blocks with the same path.
    # For example, italicized text often has a different path to the block it is part of because it
    # is considered a span element. The styling processor as is does not handle this case, as for some
    # reason Adobe doesn't consider italicization a style, and so the code is not robust to this. This
    # is something that is probably easy to fix, but it's relatively rare so is left for now and is caught
    # by the exception.
    except KeyError:
        # TODO: Fix problem that creates need for this exception (see comment above) handling (low priority).
        #  c.f page 17 of cclw-9460 first block for an example.
        logger.debug(
            f"No style spans found for this merged text block. Some semantics may be missing from this block (e.g. "
            f"italics). "
        )
        return text_output


def get_text_from_document_dict(document: dict) -> List[Tuple[str, str]]:
    """Get the text and ID from each text block in a .json file created from a `Document` object.

    A string is created for a text block by removing unnecessary styling elements, and removing
    semantically irrelevant content from list types.

    Args:
        document (dict): dict created from a `Document` object, e.g. imported from a JSON file.

    Returns:
        List[Tuple[str, str]]: list of (text, text_block_id) tuples.
    """

    text_output = []
    prev_block_processed_text = None
    for page in document["pages"]:
        for text_block in page["text_blocks"]:
            if text_block["type"] == "merged_text_block":
                text = get_text_from_merged_block(text_block)
            elif text_block["type"] == "list":
                text = get_text_from_list(text_block, prev_block_processed_text)
            else:
                text = "".join(text_block["text"]).strip()
            text_output.append((text, text_block["text_block_id"]))
            # Keep previous text block in case we need to prepend it to a list as context.
            prev_block_processed_text = text

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
    pd.DataFrame(
        text_and_ids, columns=["text", "text_block_id", "document_id"]
    ).to_json(
        output_dir / f"ids_{model_name}_{curr_time}.json",
        orient="records",
    )
    logger.info(f"Saved embeddings and IDs to {output_dir}")


if __name__ == "__main__":
    run_cli()
