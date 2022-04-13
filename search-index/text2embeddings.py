"""CLI to convert JSON documents outputted by the PDF parsing pipeline to embeddings."""

import codecs
import json
import os
import re
from pathlib import Path
from typing import List, Optional, Dict, Union

import click
import numpy as np
from navigator.core.log import get_logger
from navigator.core.utils import get_timestamp
from tqdm.auto import tqdm
from cloudpathlib import CloudPath

from app.db import PostgresConnector
from app.load_data import create_dataset
from app.ml import SBERTEncoder, SentenceEncoder
from app.utils import paginate_list

logger = get_logger(__name__)


def get_text_from_list(text_block: dict, prev_processed_text_block: dict) -> str:
    """Get text from list type and apply some decoding and minimal formatting.

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
    # This snippet is ugly/non pythonic. It's used to get around some upstream bad code with html tags. Really, this
    # was a bad way of doing things in the first place, so not overly concerned with fixing it for now. This will do.
    try:
        text = codecs.decode(text, "unicode_escape")
    except UnicodeDecodeError:
        # Flush the pipe if we can't decode the string. This needs an upstream fix,
        # but for now let's log the errors to a file for visibility.
        logger.error("Could not decode string: %s", text)
        pass
    text = "\n".join([s for s in text.split("\n") if s])
    # Always append previous text block as context. This is a fairly strong assumption, and the code to make this
    # better has been started, in postprocessor.py, but is not yet completely robust, so we are not using it for now.
    # TODO: Note, we can potentially do this in a more robust way by using the text block custom attributes created
    #  in postprocessor.py, which I've updated. This will allow us to deal with edge cases, for example where the
    #  previous block is not either context or part of the same list from the previous page. This would be the case
    #  when, for example, there are random elements between pages that the postprocessors haven't been able to catch.
    #  But I've ignored this for now because it seems that the postprocessing in postprocessor.py has dealt with the
    #  vast majority of edge cases (as indicated by the rarity of certain debugging metadata).
    try:
        text = prev_processed_text_block + "\n" + text
    except TypeError:
        breakpoint()
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
    """Remove unnecessary styling from merged text blocks (superscripts).

    Args:
        text_block: A block of text that has been merged.

    Returns:
        str: The text block with styling that is not related to semantics removed.

    """
    # Text output with no processing. Note here that we do not need to join with a space as this is already
    # done upstream, where each list item in a text block has a space at the end before text blocks are merged.
    text_output = (
        "".join(text_block["text"]).strip(),
        text_block["text_block_id"],
    )

    # Get text as opposed to block id.
    text_output_text = text_output[0]

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
                delete_indices.extend(list(range(remove_start, remove_end + 1)))

        # The indices are relative to the whole block, not just elements in the block.
        # Remove the indices from deleted_indices from text_output.
        if delete_indices:  # There will only be indices to delete in superscript case.
            text_output_amended = delete_string_indices(text_output[0], delete_indices)
            text_output = (text_output_amended, text_block["text_block_id"])
            return text_output_amended
        else:
            return text_output_text
    # Blocks are sometimes merged by the styling processor for reasons other
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
            "No style spans found for this merged text block. Some semantics may be missing from this block (e.g. "
            "italics). "
        )
        return text_output_text


def get_text_from_document_dict(
    document: dict,
) -> List[Dict[str, Union[str, int, List[List[float]]]]]:
    """Get the text and ID from each text block in a .json file created from a `Document` object.

    A string is created for a text block by removing unnecessary styling elements, and removing
    semantically irrelevant content from list types.

    Args:
        document (dict): dict created from a `Document` object, e.g. imported from a JSON file.

    Returns:
        List[Dict[str, Union[str, int, List[List[float]]]]]: dicts have keys 'text', 'text_block_id', 'coords', 'page_num'.
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

            text_output.append(
                {
                    "text": text,
                    "text_block_id": text_block["text_block_id"],
                    "coords": text_block["coords"],
                    "page_num": int(
                        re.findall(r"p(\d+)_.*", text_block["text_block_id"])[0]
                    ),
                }
            )

            # Keep previous text block in case we need to prepend it to a list as context.
            prev_block_processed_text = text

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
    required=False,
    help="Directory containing JSON files.",
)
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(exists=True, path_type=Path),
    required=False,
    help="Directory to save embeddings and IDs to.",
)
@click.option(
    "--s3",
    "-s",
    is_flag=True,
    required=False,
    help="Whether or not we are reading from and writing to S3.",
)
@click.option(
    "--s3-input-dir",
    type=str,
    required=False,
    help="Directory containing JSON files.",
)
@click.option(
    "--s3-output-dir",
    type=str,
    required=False,
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
    s3: Optional[str],
    s3_input_dir: Optional[str],
    s3_output_dir: Optional[str],
    model_name: str,
    batch_size: int,
    limit: Optional[int],
):
    """Run CLI to produce embeddings from pdf2text JSON outputs. Encoding will automatically run on the GPU if one is available.

    Args:
        input_dir (Path): Directory containing JSON files
        output_dir (Path): Directory to save embeddings and IDs to
        s3 (Optional[str]): Whether or not we are reading from and writing to S3.
        s3_input_dir (Optional[str]): Directory containing JSON files.
        s3_output_dir (Optional[str]): Directory to save embeddings and IDs to.
        model_name (str): Name of the sentence-BERT model to use. See https://www.sbert.net/docs/pretrained_models.html.
        batch_size (int): Batch size for encoding.
        limit (Optional[int]): Optionally limit the number of text samples to process. Useful for debugging.
    """
    logger.info(f"Getting text from JSONs in {input_dir}")
    if s3:
        assert s3_input_dir.startswith("s3://")
        input_dir = CloudPath(s3_input_dir)
        # output_dir = CloudPath(s3_output_dir)
    # else:
    #     input_dir = Path(input_dir)
    curr_time = get_timestamp()
    json_filepaths = input_dir.glob("*.json")  # glob.glob(str(input_dir / "*.json"))

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
