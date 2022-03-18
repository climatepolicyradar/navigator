import copy
import json
import pathlib
import re
from collections import defaultdict
from pathlib import Path
from typing import List, DefaultDict, Tuple, Dict
import argparse

import pandas as pd

# logger boilerplate
import logging


# Static method
def _minimal_bounding_box(coords: List[list]) -> list:
    """
    Return the minimally enclosing bounding box of bounding boxes.

    Args:
        coords: A list of coordinates for each bounding box formatted [x1,y1,x2,y2] with the top left as the origin.

    Returns:
        A list of coordinates for the minimally enclosing bounding box for all input bounding boxes.

    """
    x_min = min(coord[0] for coord in coords)
    y_min = min(coord[1] for coord in coords)
    x_max = max(coord[2] for coord in coords)
    y_max = max(coord[3] for coord in coords)
    return [x_min, y_min, x_max, y_max]


def _find_first_occurrence(reg: str, list_of_strings):
    """
    Finds the first occurrence of a regular expression in a list of strings.

    Args:
        reg: Regular expression to search for in the list of strings.
        list_of_strings: List of strings to search through.

    Returns:
        The first occurrence of the regular expression in the list of strings.

    """
    for string in list_of_strings:
        if re.search(reg, string):
            return string
    return None


def _pprint_list(df: pd.DataFrame) -> str:
    """
    Pretty print a text block list so that
    it can be viewed in a programming language
    or text editor.

    Args:
        df:

    Returns:

    """
    string = ""
    for ix, row in df.iterrows():
        if row["type"] == "Lbl":
            string += f"{row['text'][0]} "
        elif row["type"] == "LBody":
            string += f"{row['text'][0]}\n"
        else:
            string += f"{row['text'][0]}\n"
    return string


def _create_custom_attributes(blocks: List[Dict]) -> dict:
    """
    Create custom attributes for a list element.

    Args:
        blocks: List of text blocks belonging to a list element.

    Returns:
        A dictionary with appended custom attributes for a list element.
    """

    df = pd.DataFrame(blocks)
    df = df.loc[
        df.astype(str).drop_duplicates().index
    ]  # Bit of a hack to deal with problem upstream.
    df["page_num"] = (
        df["text_block_id"].str.split("_").str[0].str.extract("(\d+)").astype(int)
    )

    full_list_text = df["text"].tolist()
    paths = df["path"].tolist()
    block_ids = df["text_block_id"].tolist()
    custom_bounding_boxes = (
        df.groupby("page_num")
        .apply(lambda x: _minimal_bounding_box(x["coords"]))
        .tolist()
    )
    custom_attributes_dict = {
        "paths": paths,
        "text_block_ids": block_ids,
        "pretty_list_string": _pprint_list(df),
    }
    # Add custom attributes already creates during the list grouping process (joined with previous flags)
    if df['custom_attributes'].iloc[0] is not None:
        custom_attributes_dict.update(df['custom_attributes'].iloc[0])
    new_dict = {
        "text_block_id": block_ids[0],
        "path": paths[0],
        "type": "list",
        "coords": custom_bounding_boxes,
        "text": full_list_text,
        "custom_attributes": custom_attributes_dict,
    }
    return new_dict


def normalize_list_labels(l: list) -> list:
    raise NotImplementedError


# def _group_list_elements(file: pathlib.Path, reg: str) -> Tuple[dict, DefaultDict]:
#     """
#     Groups text elements in each file if they belong to the same list (as recognized by a regular expression), including introductory context.
#
#     Args:
#         file: path pointing to json file of Adobe outputs.
#
#     Returns:
#         A tuple of the original adobe content and a default dict of grouped list elements.
#
#     """
#
#     with open(file, "r") as j:
#         contents = json.loads(j.read())
#
#     # Loop through the text blocks on each page and group them if they belong to the same list,
#     # (including introductory context), indexing by the block index (e.g p0_b2) of the first
#     # element. The resulting dictionary will be used later to replace the list blocks in the
#     # original adobe content. It's not trivial to replace within this loop because this code
#     # attempts to handle the case where a list starts on the previous page. It's therefore
#     # simpler to replace in a separate step.
#     grouped_list_dict = defaultdict(list)
#     previous_text_block = (
#         None  # For prepending context to first element of each list block
#     )
#     blocks_seen = 0  # Total blocks seen.
#     prev_list_block_ix = 0  # Total blocks seen that belong to a list.
#     list_num = 0  # List in doc (First list is 0, second is 1, etc.)
#     for page in contents["pages"]:
#         for text_block in page["text_blocks"]:
#             # Not all text blocks have a populated path attribute.
#             if text_block["path"]:
#                 text_block["file_name"] = file.stem
#                 # Get list group if list element (e.g. L, L[1], L[2], etc).
#                 list_group = _find_first_occurrence(reg, text_block["path"])
#                 if list_group:
#                     # If the list element is adjacent to the last seen list element,
#                     # assume it belongs to the same list, even if we've crossed pages.
#                     if (
#                             blocks_seen != prev_list_block_ix + 1
#                     ):  # i.e. if not adjacent (rule not perfect due to elements
#                         # at bottom and top of pages).
#                         list_num += 1  # Increment list number.
#                         # first_block_id = text_block["text_block_id"]
#
#                     # Handle the first element of the first list by prepending the previous text block
#                     # by default for context. This could result in some false positive semantics, but
#                     # it's a good start. Note, first block id comes from the previous iteration if it's
#                     # inferred that we're on the previous iteration's list.
#                     if (list_num == 1) and (not grouped_list_dict):
#                         current_list_id = previous_block_id
#                         grouped_list_dict[f"{current_list_id}"].append(
#                             previous_text_block
#                         )
#
#                     # Append text to current list group.
#                     grouped_list_dict[f"{current_list_id}"].append(text_block)
#
#                     # If the element is more than 1 block away from the previous list element and there is at least 1
#                     # intervening text block, start a new list and prepend the previous text block to the list. The
#                     # assumption is that in this case the prepended item is introductory context. This may produce
#                     # false negatives (failing to group items in the same semantic list) because sometimes the same
#                     # list is more than 1 element away because of garbage text blocks at the end of the page rather
#                     # than because it is a new list. Nevertheless, this is a good start. In any case, it's hard to
#                     # generalise here because the Adobe API also parses into separate lists in cases like this,
#                     # and so we can't just infer from path names. Depending on the extent of this issue, we can add
#                     # some custom logic depending on whether elements are at the end of a page.
#                     if (
#                             previous_text_block
#                             and prev_list_block_ix + 1
#                             < blocks_seen  # implies discontinuity so start a new list.
#                     ):
#                         list_num += 1
#                         current_list_id = previous_block_id
#                         grouped_list_dict[f"{current_list_id}"].append(
#                             previous_text_block
#                         )
#
#                     # Update previous list index.
#                     prev_list_block_ix = (
#                         blocks_seen  # Save total index for next iteration.
#                     )
#
#                 # Save text block and text block id, so we can use it for the next iteration.
#                 # (we may need to prepend context to the first element of the list).
#                 previous_text_block = text_block
#                 previous_block_id = text_block["text_block_id"]
#             # Increment blocks seen, needed for determining discontinuities between different lists.
#             blocks_seen += 1
#     return contents, grouped_list_dict

def _new_custom_attributes(text_block: dict) -> dict:
    """
    Helper function to update custom attributes when a block should be joined with the previous page's block.
    Args:
        text_block:

    Returns:

    """
    new_custom_attributes = {
        "joined_with_previous_block": True
    }
    if text_block['custom_attributes'] is not None:
        text_block["custom_attributes"].update(new_custom_attributes)
    else:
        text_block["custom_attributes"] = new_custom_attributes
    return text_block

def _group_list_elements(file: pathlib.Path, reg: str) -> dict:
    """
    Args:
        file:
        reg:

    Returns:

    """

    with open(file, "r") as j:
        contents = json.loads(j.read())
    prev_list_ix = 0
    blocks_seen = 0
    last_page_ix = 0
    new_pages = []
    for ix, page in enumerate(contents["pages"]):
        previous_block = None
        new_text_blocks = []
        dd = defaultdict(list)
        for text_block in page["text_blocks"]:
            blocks_seen += 1
            if text_block["path"]:
                list_group = _find_first_occurrence(reg, text_block["path"])
                if list_group:
                    current_list_id = f"{ix}_{list_group}"
                    # Handle the case where we have a new list at the beginning of a page and where
                    # the previous list block is assumed context. Seen cases where this happens.
                    if text_block['text_block_id'].split("_")[1] == 'b1':
                        text_block = _new_custom_attributes(text_block)
                    # If the list group for the current page is unpopulated and there is
                    # a previous list block on the page, prepend it under
                    # the assumption that it is context.
                    if (len(dd[current_list_id]) == 0) and (previous_block):
                        dd[current_list_id].append(previous_block)
                        # Heuristic: If the list block is adjacent to the previous list block and the current list id
                        # was unpopulated and the start of this conditional, assume we are on the same list but on a
                        # new page, appending the appropriate metadata to custom attributes. We likely need to add
                        # some logic to handle the case where the list is more than 1 element away because of garbage
                        # text blocks at the end of the page. But for now this may be good enough.
                        if prev_list_ix + 1 == blocks_seen:
                            text_block = _new_custom_attributes(text_block)

                    dd[current_list_id].append(text_block)
                    prev_list_ix += 1
                else:
                    new_text_blocks.append(text_block)
            else:
                new_text_blocks.append(text_block)
            previous_block = text_block
            blocks_seen += 1

        last_page_ix += 1
        # Append default dict to page.
        for ll in dd.values():
            grouped_block = _create_custom_attributes(ll)
            new_text_blocks.append(grouped_block)
        # If blocks have a repeated block id, only keep the final one as the others are context values
        # that are included in the list group.
        # Sort blocks by block index of the first attribute.
        new_text_blocks = _postprocess_list_grouped_page(new_text_blocks)
        new_pages.append(new_text_blocks)
    new_contents = {'pages': new_pages}
    return new_contents

def _postprocess_list_grouped_page(text_blocks: List[dict]) -> dict:
    """
    Removes blocks that are already included in the new list blocks.
    Args:
        text_blocks: A list of dictionaries representing text blocks.

    Returns:

    """
    df = pd.DataFrame(text_blocks)
    df['page_num'] = df['text_block_id'].str.split('_b').str[0]
    df['block_num'] = df['text_block_id'].str.split('_b').str[1].astype(int)
    new_text_blocks = (
        df.groupby("text_block_id")
            .apply(lambda x: x.iloc[-1])
            .reset_index(drop=True)
            .sort_values(['page_num', 'block_num'])
            .drop(columns=['page_num', 'block_num'])
            .to_dict("records")
    )
    return new_text_blocks



def parse_adobe_list_outputs(
    root_path: Path, reg: str, out_path: Path = None
) -> DefaultDict:
    """
    Parse the elements belonging to a list into a single block, including the list's introductory text.

    Args:
        root_path: Path to Adobe extract API output.
        reg: Regular expression to match the list's identifier.
        contents_path: Path to the contents of the postprocessing output.

    Returns:
        A dictionary with values corresponding to a semantic block of a list (introductory context plus the list itself).
    """
    for file in root_path.iterdir():
        if file.suffix == ".json":
            # # Return original content dict and the grouped list blocks to overwrite original list elements with.
            # original_contents, grouped_list_dict = _group_list_elements(file, reg)
            # # Replace original with processed version.
            # for k, v in grouped_list_dict.items():
            #     grouped_list_dict[k] = _create_custom_attributes(v)
            #
            # # TODO: Add a condition here to see if we should keep the old list taxonomy or the new one.
            # new_contents = _insert_grouped_lists(original_contents, grouped_list_dict)
            # new_pages = _remove_ungrouped_list_elements(new_contents, reg)
            # _sort_and_dedupe_pages(new_pages)
            new_contents = _group_list_elements(file, reg)

            # TODO: Add grouped_list_dict s3 option
            with open(Path(out_path) / file.name, "w") as f:
                json.dump(new_contents, f, indent=4)


def _remove_ungrouped_list_elements(contents: dict, reg: str) -> dict:
    """
    Remove ungrouped list elements from the contents dict.

    Args:
        contents:

    Returns:

    """
    newpages = []
    for page in contents["pages"]:
        newblocks = []
        for block in page:
            if block["type"] == "list":
                newblocks.append(block)
            try:
                if block["path"]:
                    # Anything that's a list is already included in the new contents after the processing above,
                    # so ignore it.
                    if _find_first_occurrence(reg, block["path"]):
                        pass
                    else:
                        newblocks.append(block)
                else:
                    pass
            except KeyError:
                print("No path key in block:", block)
                newblocks.append(block)
        newpages.append(newblocks)
    return newpages


def _insert_grouped_lists(old_contents: dict, list_default_dict: DefaultDict) -> dict:
    """
    Create a new contents dict from the old contents dict.

    Args:
        old_contents: old contents dictionary.
        list_default_dict: defaultdict of semantic lists.

    Returns:
        new_contents: new contents dictionary.
    """

    # Create a new contents json file.
    # Pages is a bit of a misnomer here because lists can now overlap pages, but keeping it for now.
    new_contents = {"pages": []}
    for page in old_contents["pages"]:
        text_blocks = page["text_blocks"]
        # Reassigning the grouped list blocks to the first block of the list at
        # the correct index.
        text_blocks_copy = copy.deepcopy(
            text_blocks
        )  # Copy necessary here as insert happens in place.
        for block_ix, block in enumerate(text_blocks):
            block_id = block["text_block_id"]
            if block_id in list_default_dict.keys():
                _ = text_blocks_copy.pop(
                    block_ix
                )  # For some reason this isn't working as expected...
                text_blocks_copy.insert(
                    block_ix, list_default_dict[block_id]
                )  # Insert replacement block.
        new_contents["pages"].append(text_blocks_copy)
    return new_contents


def _sort_and_dedupe_pages(newpages):
    try:
        for pg_ix, page in enumerate(newpages):
            df = pd.DataFrame(page)
            df = df.loc[df.astype(str).drop_duplicates().index].reset_index(drop=True)
            df["page"] = df["text_block_id"].str.split("_", expand=True)[0]
            df["block"] = df["text_block_id"].str.split("_", expand=True)[1]
            df.drop(columns=["page", "block"], inplace=True)
            df.sort_values(by=["page", "block"], inplace=True)
            newpages[pg_ix] = df.to_dict("records")
    except KeyError as e:
        print(e)


def cli(in_path, out_path):
    reg = r"L\[?\d?\]?"
    new_contents = parse_adobe_list_outputs(in_path, reg, out_path)
    return new_contents


if __name__ == "__main__":
    # create logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info("Starting...")
    parser = argparse.ArgumentParser()
    parser.add_argument("in_path", type=str, help="Path to the contents.json file.")
    parser.add_argument("out_path", type=str, help="Path to the output directory.")
    args = parser.parse_args()
    in_dir = Path(args.in_path)
    out_dir = Path(args.out_path)
    new_contents = cli(in_dir, out_dir)
