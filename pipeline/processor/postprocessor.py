import copy
import json
import pathlib
import re
from collections import defaultdict
from typing import List, Dict, DefaultDict

import pandas as pd

from pipeline.extract.document import Document


class AdobeDocumentPostProcessor:
    """Further processing of processed outputs from the Adobe API (handling cases not easily
    handled by the API itself)."""

    regex_pattern = r"L\[?\d?\]?"


    @staticmethod
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

    @staticmethod
    def _find_first_occurrence(regex_pattern: str, list_of_strings):
        """
        Finds the first occurrence of a regular expression in a list of strings.

        Args:
            regex_pattern: Regular expression to search for in the list of strings.
            list_of_strings: List of strings to search through.

        Returns:
            The first occurrence of the regular expression in the list of strings.

        """
        for string in list_of_strings:
            if re.search(regex_pattern, string):
                return string
        return None

    @staticmethod
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

    @staticmethod
    def _sort_and_dedupe_pages(newpages: list):
        try:
            for pg_ix, page in enumerate(newpages):
                df = pd.DataFrame(page)
                df = df.loc[df.astype(str).drop_duplicates().index].reset_index(
                    drop=True
                )
                df["page"] = df["text_block_id"].str.split("_", expand=True)[0]
                df["block"] = df["text_block_id"].str.split("_", expand=True)[1]
                df.drop(columns=["page", "block"], inplace=True)
                df.sort_values(by=["page", "block"], inplace=True)
                newpages[pg_ix] = df.to_dict("records")
        except KeyError as e:
            print(e)

    @staticmethod
    def _insert_grouped_lists(
            old_contents: dict, list_default_dict: DefaultDict
    ) -> dict:
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


    def _create_custom_attributes(self, blocks: List[Dict]) -> dict:
        """
        Create custom attributes for a list of text blocks.

        Args:
            blocks: List of text blocks belonging to a list element.

        Returns:
            A dictionary with appended custom attributes for a list element.
        """

        df = pd.DataFrame(blocks)
        # Note this drop duplicates step is a bit of a hack to deal with undiagnosed upstream
        # issues leading to duplicates..
        df = df.loc[
            df.astype(str).drop_duplicates().index
        ]
        df["page_num"] = (
            df["text_block_id"].str.split("_").str[0].str.extract("(\d+)").astype(int)
        )

        full_list_text = df["text"].tolist()
        paths = df["path"].tolist()
        block_ids = df["text_block_id"].tolist()
        custom_bounding_boxes = (
            df.groupby("page_num")
                .apply(lambda x: self._minimal_bounding_box(x["coords"]))
                .tolist()
        )
        custom_attributes_dict = {
            "paths": paths,
            "text_block_ids": block_ids,
            "custom_bounding_boxes": custom_bounding_boxes,
            "pretty_list_string": self._pprint_list(df),
        }
        new_dict = {
            "text_block_id": block_ids[0],
            "type": "list",
            "text": full_list_text,
            "custom_attributes": custom_attributes_dict,
        }
        return new_dict


    def _group_list_elements(self, contents: dict, reg: str) -> dict:
        """
        Args:
            file:
            reg:

        Returns:

        """

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
                    list_group = self._find_first_occurrence(reg, text_block["path"])
                    if list_group:
                        current_list_id = f"{ix}_{list_group}"
                        # Handle the case where we have a new list at the beginning of a page and where
                        # the previous list block is assumed context. Seen cases where this happens.
                        if text_block['text_block_id'].split("_")[1] == 'b1':
                            text_block = self._new_custom_attributes(text_block)
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
                                text_block = self._new_custom_attributes(text_block)

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
                grouped_block = self._create_custom_attributes(ll)
                new_text_blocks.append(grouped_block)
            # If blocks have a repeated block id, only keep the final one: the others are context values
            # that are included in the list group.
            # Sort blocks by block index of the first attribute.
            new_text_blocks = self._postprocess_list_grouped_page(new_text_blocks)
            new_pages.append(new_text_blocks)
        new_contents = {'pages': new_pages}
        return new_contents


    def postprocess(
            self, root_path: pathlib.Path, out_path: pathlib.Path = None
    ) -> Document:
        """
        Parse the elements belonging to a list into a single block, including the list's introductory text.

        Args:
            root_path: Path to Adobe extract API output.

        Returns:
            A dictionary with values corresponding to a semantic block of a list (introductory context plus the list itself).
        """
        with open(root_path, "r") as j:
            contents = json.loads(j.read())
            filename = root_path.stem

        # Return original content dict and the grouped list blocks to overwrite original list elements with.
        new_contents = self._group_list_elements(
            contents, self.regex_pattern
        )
        return Document(pages=new_contents['pages'], filename=filename)

