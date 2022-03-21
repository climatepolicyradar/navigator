import json
import pathlib
import re
from collections import defaultdict
from typing import List, Dict, Optional

import numpy as np
import pandas as pd
from pipeline.processor.utils import minimal_bounding_box

from pipeline.extract.document import Document, TextBlock, Page

from collections import Counter
from copy import deepcopy
from english_words import english_words_set

class HyphenationPostProcessor:
    """
    Post processor to join words that are separated into separate blocks due
    to hyphenation at line breaks.
    """

    def rewrap_hyphenated_words(self, li: list) -> list:
        """
        Reorganise a list of strings so that word fragments separated
        by hyphens or em dashes to start new lines are joined into a single
        word if the word fragments have no meaning by themselves.

        Args:
            li: List of strings/sentences.

        Returns:
            List of strings/sentences with hyphenated words joined into a single word.

        """
        current = None
        for ix, l in enumerate(li):
            regex_match = re.search(r'\w+(-|–){1}$', l)
            if current:
                word_fragment = current.rstrip('-')
                # TODO: Handle non-English words
                if word_fragment in english_words_set:
                    # Check if the word with hyphen removed is an english
                    # word and if it is, make this the first word of the newline
                    # without the hyphen (e.g. repair-ing)
                    newline_first_word = word_fragment + l.split(' ')[0].lstrip('-')
                    if newline_first_word in english_words_set:
                        li[ix] = newline_first_word + l.split(' ')[1:]
                    # Otherwise, keep the hyphenation but put it on a newline e.g. post-processing.
                    else:
                        li[ix] = word_fragment + '-' + l
                else:
                    li[ix] = word_fragment + l
                # Reset.
                current = None
            if regex_match:
                # Strip matching regex from the end of the string.
                li[ix] = l[:regex_match.start()]
                current = regex_match[0]
        return li

    def process(self, contents) -> Document:
        for ix, page in enumerate(contents['pages']):
            new_text_blocks = self.rewrap_hyphenated_words(page['text_blocks'])
            contents['pages'][ix]['text_blocks'] = new_text_blocks

class AdobeTextStylingPostProcessor:
    """
    Some semantic passages have separate blocks for styling markers such
    as underlines, superscripts and subscripts. We want to group such cases
    into single contiguous blocks. However, we want to keep the styling information
    because it's often relevant to semantics. For example, CO2 is often represented
    using a subscript. For now, we keep everything and indicate the styling with
    HTML style tags inline.

    """
    @staticmethod
    def _classify_text_block_styling(text_block: TextBlock) -> Optional[str]:
        """
        Get text block styling, if present.

        Args:
            text_block:

        Returns:

        """
        if not text_block.custom_attributes:
            return None

        if text_block.custom_attributes.get("BaselineShift", 0) < 0:
            return "subscript"
        elif text_block.custom_attributes.get("TextDecorationType") == "Underline":
            return "underline"
        elif text_block.custom_attributes.get("TextPosition") == "Sup":
            return "superscript"
        else:
            return None

    @staticmethod
    def _add_text_styling_markers(text: str, styling: str) -> str:
        """
        Add inline styling markers to text.

        Args:
            text: raw text without styling.
            styling: styling to apply.

        Returns:

        """
        leading_spaces = " " * (len(text) - len(text.lstrip(" ")))
        trailing_spaces = " " * (len(text) - len(text.rstrip(" ")))

        if styling == "subscript":
            # Keep subscripts as they may be semantically relevant (as in CO2)
            return f"{leading_spaces}<sub>{text.strip()}</sub>{trailing_spaces}"
        elif styling == "superscript":
            # Superscripts not semantically relevant, remove them.
            return f"{leading_spaces + trailing_spaces}"
        elif styling == "underline":
            # TODO: What is the semantic relevance of underlines?
            return f"{leading_spaces}<u>{text.strip()}</u>{trailing_spaces}"
        else:
            return text

    def merge_text_blocks(self, text_blocks: List[TextBlock]) -> TextBlock:
        """
        Merge text blocks in the same semantic category (same path) that have been separated due to styling elements.

        Args:
            text_blocks:

        Returns:
            A new text block

        """
        all_coords = [tuple(text_block.coords) for text_block in text_blocks]
        merged_coords = minimal_bounding_box(all_coords)

        merged_block_text = []

        for text_block in text_blocks:
            block_styling = self._classify_text_block_styling(text_block)
            new_block_text = [
                self._add_text_styling_markers(line, block_styling)
                for line in text_block.text
            ]

            if merged_block_text == []:
                merged_block_text = new_block_text
            else:
                merged_block_text[-1] = merged_block_text[-1] + new_block_text[0]
                merged_block_text += new_block_text[1:]

        return TextBlock(
            text=merged_block_text,
            text_block_id=text_blocks[0].text_block_id + "_merged",
            coords=merged_coords,
            path=text_blocks[0].path,
        )

    def process(self, document: Document) -> Document:
        """
        Iterate through a document and merge text blocks that have been separated due to styling elements.

        Args:
            document: pdf doc object.

        Returns:
                A new document object with styling info added.
        """
        new_document = deepcopy(document)

        for page in new_document.pages:
            # If page blocks do not have a path (because they're from the embedded text extractor), skip them.
            # TODO: This is a hack. We should be able to handle this better.
            if page.text_blocks[0].path is None:
                continue
            # Count repeated paths since blocks with custom styling (subscript, superscript, underline)
            # have separate elements in the same text block.
            path_counts = Counter([tuple(block.path) for block in page.text_blocks])

            # TODO: This logic does not always work. For instance, cclw-9460 separates
            duplicated_paths = [
                path for path, count in path_counts.items() if count > 1
            ]

            for path in duplicated_paths:
                text_block_idxs, text_blocks_to_merge = list(
                    zip(
                        *[
                            (idx, block)
                            for idx, block in enumerate(page.text_blocks)
                            if tuple(block.path) == path
                        ]
                    )
                )
                merged_text_block = self.merge_text_blocks(text_blocks_to_merge)
                page.text_blocks = (
                        page.text_blocks[0: text_block_idxs[0]]
                        + [merged_text_block]
                        + page.text_blocks[text_block_idxs[-1] + 1:]
                )

        return new_document


class AdobeDocumentPostProcessor:
    """Further processing of processed outputs from the Adobe API (handling cases not easily
    handled by the API itself)."""

    regex_pattern = r"L\[?\d?\]?$"

    @staticmethod
    def _minimal_bounding_box(coords: List[list]) -> list:
        """
        Return the minimally enclosing bounding box of bounding boxes.

        Args: coords: A list of coordinates for each bounding box formatted [x1,y1,x2,y2] with the bottom left as the
        origin.

        Returns:
            A list of coordinates for the minimally enclosing bounding box for all input bounding boxes.

        """
        x_min = min(coord[0][0] for coord in coords)
        y_min = min(coord[1][1] for coord in coords)
        x_max = max(coord[1][0] for coord in coords)
        y_max = max(coord[3][1] for coord in coords)
        return [[x_min, y_min], [x_max, y_min], [x_min, y_max], [x_max, y_max]]

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

    # Find number of occurrences of a regex pattern in a list of strings
    @staticmethod
    def _find_all_occurrences(regex_pattern: str, list_of_strings):
        """
        Finds all occurrences of a regular expression in a list of strings.

        Args:
            regex_pattern: Regular expression to search for in the list of strings.
            list_of_strings: List of strings to search through.

        Returns:
            All occurrences of the regular expression in the list of strings.

        """
        return [string for string in list_of_strings if re.search(regex_pattern, string)]

    def _format_semantic_lists(self, df: pd.DataFrame) -> List[List[str]]:
        """
        """
        # TODO: fix this!
        # Bit of a hack here to handle the fact that there are sometimes trailing stylespan elements that haven't
        # been dealt with upstream e.g. if there is more than one style span in a row.
        df = df[df.type != 'StyleSpan']
        lst = []
        new_string = ''
        for ix, row in df.iterrows():
            text_type = row['type']
            if text_type == 'Lbl':
                new_string = ''
                label_string=f"<Lbl>{row['text']}<\Lbl>"
                if row['first_bool']:
                    new_string += f"\n<li{row['list_num']}>\n{label_string}"
                else:
                    new_string += f"{label_string}"
            # Assume that if we haven't got a label, we're in a list body. This is a bit of a hack to get around the
            # fact that there are sometimes other types e.g. Span or Paragraph span that (due to italics and such)
            # that should really be part of a list body. Tested this and works in most cases, but doesn't work for
            # cclw-8149 for example.
            else:
                if row['last_bool']:
                    new_string +=f" <LBody>{row['text']}<\LBody>\n"+ f"\n<\li{row['list_num']}>\n"
                else:
                    new_string += f" <LBody>{row['text']}<\LBody>\n"
                lst.append(new_string)

        #     # Start list text by indicating the list nesting level.
        #     list_nesting_number = row['list_num']
        #     if list_nesting_number != prev_list_nesting_number:
        #         if list_nesting_number == 1:
        #             new_string += f"<li{list_nesting_number}>\n"
        #         else:
        #             new_string += f"<\li{prev_list_nesting_number}>\n<li{list_nesting_number}>\n"
        #     # TODO: Handle spans.
        #     if text_type == 'Lbl':
        #         if new_string:
        #             lst.append(new_string + '<LBody>\n')
        #         new_string = f"<Lbl>{row['text'][0].strip()}<Lbl>"
        #     else:
        #         if new_string.endswith('<Lbl>'):
        #             new_string += f"<LBody>{row['text'][0].strip()}"
        #         else:
        #             new_string += f"{row['text'][0].strip()} "
        #     prev_list_nesting_number = list_nesting_number
        # if not re.match(r"\n?<\\li1>",lst[-1]):
        #     lst.append("\n<\li1>")
        formatted = '. '.join([li for li in lst])
        return lst

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
            # TODO: Handle spans.
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
    def _remove_unmerged_lists(text_blocks: List[dict]) -> dict:
        """
        Remove list elements on a page that are not part of a list group.

        Args:
            text_blocks: All text blocks on a page.

        Returns:
            The text blocks with singular list elements removed.

        """
        df = pd.DataFrame(text_blocks)
        df["page_num"] = df["text_block_id"].str.split("_b").str[0]
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
        df['list_num'] = df['path'].apply(lambda x: len(self._find_all_occurrences(self.regex_pattern, x)))
        # Get the first and last index of each page number as this will be convenient for formatting.
        df = df.merge(df.index.to_series().groupby(df.list_num).agg(['first', 'last']).reset_index(), how='left',
                      on='list_num')
        df['first_bool'] = df['first'] == df.index
        df['last_bool'] = df['last'] == df.index
        self._format_semantic_lists(df)

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
                        if (
                                text_block["text_block_id"].split("_")[1] == "b1"
                        ) and previous_block:
                            text_block = self._update_custom_attributes(
                                text_block, "contiguous_with_prev_page_context"
                            )
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
                new_text_blocks = self._remove_unmerged_lists(new_text_blocks)
            # In cases with 1 block on a page, sometimes coords appear ommitted. Add None. May affect downstream
            # processing.
            if len(new_text_blocks) == 1 and ("coords" not in new_text_blocks[0]):
                new_text_blocks[0]["coords"] = None
            # Convert to text block data class.
            new_text_blocks = [TextBlock(**tb) for tb in new_text_blocks]
            newpage = Page(
                text_blocks=new_text_blocks,
                dimensions=page["dimensions"],
                page_id=page["page_id"],
            )
            new_pages.append(newpage)

        new_contents = {"pages": new_pages}
        return new_contents

    def postprocess(self, root_path: pathlib.Path) -> Document:
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
