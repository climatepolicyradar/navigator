import json
import pathlib
import re
from collections import defaultdict
from typing import List, Dict

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
    def _update_custom_attributes(text_block: dict, new_attribute: str) -> dict:
        """
        Helper method to update custom attributes with metadata to inform that a block
        is contiguous with the previous element, which may be of a different type.

        Args:
            text_block: The text block that is contiguous from the previous page.
            new_attribute: The new attribute to add to custom_attributes.

        Returns:
            The text block with the updated custom attributes.

        """
        new_custom_attributes = {new_attribute: True}
        if text_block["custom_attributes"] is not None:
            text_block["custom_attributes"].update(new_custom_attributes)
        else:
            text_block["custom_attributes"] = new_custom_attributes
        return text_block

    @staticmethod
    def _postprocess_list_grouped_page(text_blocks: List[dict]) -> dict:
        """
        Remove list elements on a page that are not part of a list group.

        Args:
            text_blocks: All text blocks on a page.

        Returns:
            The text blocks with singular list elements removed.

        """
        df = pd.DataFrame(text_blocks)
        try:
            df["page_num"] = df["text_block_id"].str.split("_b").str[0]
        except KeyError:
            print('hi')
        df["block_num"] = df["text_block_id"].str.split("_b").str[1].astype(int)
        # Remove all but the last block for each id, as this is unsorted with
        # the last block being the grouped list element we want to keep.
        new_text_blocks = (
            df.groupby("text_block_id")
            .apply(lambda x: x.iloc[-1])
            .reset_index(drop=True)
            .sort_values(["page_num", "block_num"])
            .drop(columns=["page_num", "block_num"])
            .to_dict("records")
        )
        return new_text_blocks

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
        df = df.loc[df.astype(str).drop_duplicates().index]
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

    def _group_list_elements(self, contents: dict, filename) -> dict:
        """
        Parse Adobe outputs to group list elements

        Args:
            contents: A dict of the processed adobe output for a particular pdf.

        Returns:
            Reprocessed version of the Adobe output with grouped list elements.
        """

        prev_list_ix = 0
        blocks_seen = 0
        last_page_ix = 0
        new_pages = []
        for ix, page in enumerate(contents["pages"]):
            previous_block = None
            new_text_blocks = []
            dd = defaultdict(list)
            if type(page)!=dict:
                continue
            for text_block in page["text_blocks"]:
                blocks_seen += 1
                if text_block["path"]:
                    list_group = self._find_first_occurrence(
                        self.regex_pattern, text_block["path"]
                    )
                    if list_group:
                        current_list_id = f"{ix}_{list_group}"
                        # Handle the case where we have a new list at the beginning of a page and where
                        # the previous list block is assumed context.
                        if (text_block["text_block_id"].split("_")[1] == "b1") and previous_block:
                            text_block = self._update_custom_attributes(text_block, "contiguous_with_prev_page_context")
                        # If the list group for the current page is unpopulated and there is
                        # a previous list block on the page, prepend it under
                        # the assumption that it is context.
                        if (len(dd[current_list_id]) == 0) and previous_block:
                            # TODO: Before, we added the previous block to the list but decided to separate this out.
                            #  Perhaps it's a good idea to add it back in but to the metadata, so that we can
                            #  validate the assumption that the previous block is context by pretty printing the list
                            #  when coding.

                            # Heuristic: If the list block is adjacent to the previous list block and the current
                            # list id was unpopulated and the start of this conditional, assume we are on the same
                            # list but on a new page, appending the appropriate metadata to custom attributes. We
                            # likely need to add some logic to handle the case where the list is more than 1 element
                            # away because of garbage text blocks at the end of the page. But for now this may be
                            # good enough.
                            # TODO: Perhaps add some more nuance here, as another possibility is that it's contiguous
                            #  with the previous page but it's context/a list continuation.
                            if prev_list_ix + 1 == blocks_seen:
                                text_block = self._update_custom_attributes(
                                    text_block, "contiguous_with_previous_page_list"
                                )
                            else:
                                text_block = self._update_custom_attributes(
                                    text_block,
                                    "contiguous_with_same_page_context",
                                )

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
            for li in dd.values():
                grouped_block = self._create_custom_attributes(li)
                new_text_blocks.append(grouped_block)
            # If blocks have a repeated block id, only keep the final one: the others are context values
            # that are included in the list group.
            # Sort blocks by block index of the first attribute.
            # TODO: Why have we got pages with no list blocks?
            if len(new_text_blocks) > 0:
                new_text_blocks = self._postprocess_list_grouped_page(new_text_blocks)
            new_pages.append(new_text_blocks)
        new_contents = {"pages": new_pages}
        return new_contents

    def postprocess(
        self, root_path: pathlib.Path
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
        new_contents = self._group_list_elements(contents, filename)
        return Document(pages=new_contents["pages"], filename=filename)
