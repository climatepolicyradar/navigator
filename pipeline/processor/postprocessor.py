import copy
import re
from abc import ABC, abstractmethod
from collections import Counter
from collections import defaultdict
from copy import deepcopy
from typing import List, Dict, Optional

import pandas as pd
from english_words import english_words_set
from extract.document import Document, TextBlock


class PostProcessor(ABC):
    @staticmethod
    def _minimal_bounding_box(coords: List[List[float]]) -> List[List[float]]:
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

    @abstractmethod
    def process(self, document: Document, filename: Optional) -> Document:
        """
        Process the document.

        Args:
            document: The document to process.
            filename: The filename of the document.

        Returns:
            The processed document.
        """
        pass


class HyphenationPostProcessor(PostProcessor):
    """
    Post processor to join words that are separated into separate blocks due
    to hyphenation at line breaks.
    """

    @staticmethod
    def _rewrap_hyphenated_words(li: list) -> list:
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
        new_list = copy.deepcopy(li)
        for ix, l in enumerate(li):
            regex_match = re.search(r"\w+(-|–){1}$", l)

            if current:
                word_fragment = current.rstrip("-")
                # TODO: Handle non-English words
                if word_fragment in english_words_set:
                    # Check if the word with hyphen removed is an english
                    # word and if it is, make this the first word of the newline
                    # without the hyphen (e.g. repair-ing)
                    newline_first_word = word_fragment + l.split(" ")[0].lstrip("-")
                    if newline_first_word in english_words_set:
                        new_list[ix] = newline_first_word + " ".join(l.split(" ")[1:])

                    # Otherwise, keep the hyphenation but put it on a newline e.g. post-processing.
                    else:
                        new_list[ix] = word_fragment + "-" + l
                else:
                    new_list[ix] = word_fragment + l
                # Reset.
                current = None
            if regex_match:
                # Strip matching regex from the end of the string.
                new_list[ix] = l[: regex_match.start()]
                current = regex_match[0]
        return new_list

    def process(self, contents: Document) -> Document:
        contents = contents.to_dict()
        for ix, page in enumerate(contents["pages"]):
            for text_block in page["text_blocks"]:
                text_block["text"] = self._rewrap_hyphenated_words(text_block["text"])
        contents = Document.from_dict(contents)
        return contents


class AdobeTextStylingPostProcessor(PostProcessor):
    """
    Some semantic passages have separate blocks for styling markers such
    as underlines, superscripts and subscripts. We want to group such cases
    into single contiguous blocks. However, we want to keep the styling information
    because it's often relevant to semantics. For example, CO2 is often represented
    using a subscript. For now, we keep everything and indicate the styling with custom
    style span attributes.
    """

    def __init__(self):
        super(AdobeTextStylingPostProcessor, self).__init__()

    @staticmethod
    def _classify_text_block_styling(text_block: TextBlock) -> Optional[str]:
        """
        Get text block styling, if present.

        Args:
            text_block:

        Returns:

        """
        if not text_block["custom_attributes"]:
            return None

        if text_block["custom_attributes"].get("BaselineShift", 0) < 0:
            return "subscript"
        elif text_block["custom_attributes"].get("TextDecorationType") == "Underline":
            return "underline"
        elif text_block["custom_attributes"].get("TextPosition") == "Sup":
            return "superscript"
        else:
            return None

    def merge_text_blocks(self, text_blocks: List[dict]) -> dict:
        """
        Merge text blocks in the same semantic category (same path) that have been separated due to styling elements.

        Note, the indexing style is slightly un-pythonic here (a single digit superscript has start and end indices (144, 144)
        instead of (144, 145). See TODO below.

        Args:
            text_blocks:

        Returns:
            A new text block

        """
        all_coords = [tuple(text_block["coords"]) for text_block in text_blocks]
        merged_coords = self._minimal_bounding_box(all_coords)

        style_spans = []
        merged_block_text = []
        cumulative_block_len = 0
        for text_block in text_blocks:
            start_ix = cumulative_block_len
            cumulative_block_len += sum([len(line) for line in text_block["text"]])
            block_styling = self._classify_text_block_styling(text_block)

            if merged_block_text == []:
                merged_block_text = text_block["text"]
            else:
                merged_block_text[-1] = merged_block_text[-1] + text_block["text"][0]
                merged_block_text += text_block["text"][1:]

            # Append style metadata that will later be added to custom attributes for text block.
            if block_styling:
                # The last style index here is the index of the block with sentences joined.
                last_style_ix = (
                    len("".join((text for text in merged_block_text)).strip()) - 1
                )
                # TODO: Make indexing more pythonic. See docstring.
                style_span = {
                    "style": block_styling,
                    "start_idx": start_ix,
                    "end_idx": last_style_ix,
                }
                style_spans.append(style_span)

        if style_spans:
            custom_attributes = {"styleSpans": style_spans}
        else:
            custom_attributes = {}

        text_block = {
            "text": merged_block_text,
            "type": "merged_text_block",
            "coords": merged_coords,
            "path": text_blocks[0]["path"],
            "text_block_id": text_blocks[0]["text_block_id"] + "_merged",
            "custom_attributes": custom_attributes,
        }
        return text_block

    def process(self, document: Document) -> Document:
        """
        Iterate through a document and merge text blocks that have been separated due to styling elements.

        Args:
            document:

        Returns:
                A new dict object with styling info added.
        """
        new_document = deepcopy(document)
        new_document = new_document.to_dict()

        for page in new_document["pages"]:
            # If page blocks do not have a path (because they're from the embedded text extractor), skip them.
            # TODO: This is a hack. We should be able to handle this better.
            if len(page["text_blocks"]) == 0:
                continue
            else:
                if page["text_blocks"][0]["path"] is None:
                    continue

            # Count repeated paths since blocks with custom styling (subscript, superscript, underline)
            # have separate elements in the same text block.
            path_counts = Counter(
                [tuple(block["path"]) for block in page["text_blocks"]]
            )

            # TODO: This logic does not always work. For instance, cclw-9460.
            duplicated_paths = [
                path for path, count in path_counts.items() if count > 1
            ]
            try:
                for path in duplicated_paths:
                    try:
                        text_block_idxs, text_blocks_to_merge = list(
                            zip(
                                *[
                                    (idx, block)
                                    for idx, block in enumerate(page["text_blocks"])
                                    if tuple(block["path"])
                                    == path  # Sometimes no matches. Why?
                                ]
                            )
                        )
                        merged_text_block = self.merge_text_blocks(text_blocks_to_merge)
                        page["text_blocks"] = (
                            page["text_blocks"][0 : text_block_idxs[0]]
                            + [merged_text_block]
                            + page["text_blocks"][text_block_idxs[-1] + 1 :]
                        )
                    # TODO: Fix this rare exception.
                    except ValueError:  # Occasional failure.
                        print("Failure to merge text blocks at path:", path)

            except TypeError:
                pass

        new_document = Document.from_dict(new_document)
        return new_document


class AdobeListGroupingPostProcessor(PostProcessor):
    """Further processing of processed outputs from the Adobe API (handling cases not easily
    handled by the API itself)."""

    list_regex_pattern = r"L\[?\d?\]?$"

    def __init__(self):
        super(AdobeListGroupingPostProcessor, self).__init__()

    # Find number of occurrences of a regex pattern in a list of strings
    @staticmethod
    def _find_all_list_occurrences(regex_pattern: str, list_of_strings):
        """
        Finds all occurrences of a regular expression in a list of strings.

        Args:
            regex_pattern: Regular expression to search for in the list of strings.
            list_of_strings: List of strings to search through.

        Returns:
            All occurrences of the regular expression in the list of strings.

        """
        return [
            string for string in list_of_strings if re.search(regex_pattern, string)
        ]

    def _format_semantic_lists(self, df: pd.DataFrame) -> List[List[str]]:
        """
        Takes a dataframe with list elements and associated metadata and
        parses the list text into a more formatted list of strings with html-esque
        tags. Best attempt is made to keep the right semantics and assign
        appropriate tags.

        Args:
            df: pd.DataFrame
                text                  object
                text_block_id         object
                coords                object
                type                  object
                path                  object
                custom_attributes     object
                page_num               int64
                list_num               int64
                first_list_index       int64
                last_list_index        int64
                first_list_ix_bool      bool
                last_list_ix_bool       bool
        """

        # TODO: Temporary hack from breakage created by text-hyphenation part of pipeline. Messy duplicatation.
        df["type"] = df["path"].apply(lambda x: x[-1])
        # Sometimes label is called ExtraCharSpan, replace it with label
        df["type"] = df["type"].replace(
            {"ExtraCharSpan": "Lbl", "ParagraphSpan": "LBody", "Span": "Lbl"}
        )

        # TODO: fix this!
        # Bit of a hack here to handle the fact that there are sometimes trailing stylespan elements that haven't
        # been dealt with upstream e.g. if there is more than one style span in a row.
        df = df[df.type != "StyleSpan"]
        lst = []
        new_string = ""
        for ix, row in df.iterrows():
            text_type = row["type"]
            text = row["text"][0].strip()
            list_number = row["list_num"]
            if text_type == "Lbl":
                new_string = ""
                label_string = fr"<Lbl>{text}<\Lbl>"
                if row["first_list_ix_bool"]:
                    new_string += f"\n<li{list_number}>\n{label_string}"
                else:
                    new_string += f"{label_string}"
            # TODO: Test more thoroughly.
            #  Assume that if the list element isn't a label and the type hasnt been
            #  handled above, it's part of a list body. This is a bit of a hack to get around the fact that there are
            #  sometimes other types e.g. Span or Paragraph span that (due to italics and such) that should really be
            #  part of a list body. Tested this and works so far, but there may be some difficult edge cases.
            else:
                if row["last_list_ix_bool"]:
                    new_string += (
                        fr"<LBody>{text}<\LBody>\n" + fr"\n<\li{list_number}>\n"
                    )
                else:
                    new_string += fr"<LBody>{text}<\LBody>\n"
                lst.append(new_string)
        return lst

    @staticmethod
    def _line_reformatting(line: str) -> str:
        """
        Replaces HTML formatting we don't want displayed in output and replace list labels
        with a normalised version (bullet points).

        Args:
            line: String to be reformatted.
        Returns:
            Reformatted string.
        """
        line = re.sub(r"<Lbl>.*<\\Lbl>", "*", line)
        line = re.sub(r"<LBody>", " ", line)
        line = re.sub(r"<\\LBody>", "", line)
        return line

    def _pprinter(self, text_lst: List[str]) -> str:
        """
        Pretty prints a list of strings for API/Python access, handling nested lists gracefully
        with tabulation. This can be used for debugging purposes.

        Args:
            text_lst: A list of strings, each of which is a list element.

        Returns:
            A nicely formatted string for API/Python access.

        """
        pretty_string = ""
        current_tab_level = 0
        for line in text_lst:
            if line.startswith("<Lbl>"):
                line = self._line_reformatting(line)
                end_of_list = re.search(r"<\\li\d+>$", line.strip())
                line = re.sub(r"<\\li\d+>", "", line)
                pretty_string += "\t" * current_tab_level + line.strip() + "\n"
                if end_of_list:
                    if current_tab_level > 0:
                        current_tab_level -= 1
            elif line.strip().startswith("<li"):
                list_num = int(re.search(r"<li(\d+)>", line.strip()).group(1))
                line = self._line_reformatting(line)
                line = re.sub(r"<li\d+>", "", line)
                if list_num > 1:
                    current_tab_level += 1
                pretty_string += "\t" * current_tab_level + line.strip() + "\n"
        return pretty_string

    @staticmethod
    def _update_contiguity_attributes(text_block: dict, new_attribute: str) -> dict:
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
        df["block_num"] = df["text_block_id"].str.extract(r"b(\d+)").astype(int)
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

    def _update_custom_attributes(self, blocks: List[Dict]) -> dict:
        """
        Create custom attributes for a list of text blocks that are part of the same semantic list.

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
            df["text_block_id"].str.split("_").str[0].str.extract(r"(\d+)").astype(int)
        )
        df["list_num"] = df["path"].apply(
            lambda x: len(self._find_all_list_occurrences(self.list_regex_pattern, x))
        )
        # Get the first and last index of each list number in a group of nested lists.
        # This is used to determine if a list element is the first or last element in a group,
        # which is used to determine the nesting level when printing and also to give html-esque
        # indicators e.g. <li1>, <li2>, etc.
        df = df.merge(
            df.index.to_series()
            .groupby(df.list_num)
            .agg(["first", "last"])
            .reset_index(),
            how="left",
            on="list_num",
        ).rename(columns={"first": "first_list_index", "last": "last_list_index"})
        # Get booleans to indicate whether each text block contains the first or last element of a
        # (nested) list.
        df["first_list_ix_bool"] = df["first_list_index"] == df.index
        df["last_list_ix_bool"] = df["last_list_index"] == df.index

        original_list_text = df["text"].tolist()
        full_list_text = self._format_semantic_lists(df)
        paths = df["path"].tolist()
        block_ids = df["text_block_id"].tolist()
        custom_bounding_boxes = (
            df.groupby("page_num")
            .apply(lambda x: self._minimal_bounding_box(x["coords"]))
            .tolist()
        )
        # Code here a little awkward due to the way the dataframe is structured (dict not hashable type), but works.
        orig_custom_attributes = {}
        for val in df["custom_attributes"].values:
            if type(val) == dict:
                orig_custom_attributes.update(val)

        # Text list to pass to pprinter.

        custom_attributes_new = {
            "paths": paths,
            "text_block_ids": block_ids,
            "pretty_list_string": self._pprinter(full_list_text),
            "original_list_text": original_list_text,
            "num_nesting_levels": df["list_num"].nunique(),
        }

        custom_attributes_concat = {**orig_custom_attributes, **custom_attributes_new}

        new_dict = {
            "coords": custom_bounding_boxes[0],
            "path": paths[0],
            "text_block_id": block_ids[0],
            "type": "list",
            "text": full_list_text,
            "custom_attributes": custom_attributes_concat,
        }
        return new_dict

    def _group_list_elements(self, contents: dict) -> dict:
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
                    list_occurrences = self._find_all_list_occurrences(
                        self.list_regex_pattern, text_block["path"]
                    )
                    if len(list_occurrences) == 0:
                        list_group = None
                    else:
                        list_group = list_occurrences[0]
                    if list_group:
                        current_list_id = f"{ix}_{list_group}"
                        block_num = int(
                            re.search(r"b(\d+)", text_block["text_block_id"]).group(1)
                        )
                        # TODO: Validate cases where this fails. Note, update by Kalyan may
                        #  add additional cases where this fails because the first block on a page
                        #   is not always block 1.
                        # Case 1: We have a new list at the beginning of a page and
                        # the previous list block is assumed context.
                        if (block_num == 1) and previous_block:
                            text_block = self._update_contiguity_attributes(
                                text_block, "possibly_contiguous_with_prev_page_context"
                            )
                        # If the list group for the current page is unpopulated and there is
                        # a previous list block on the page, prepend it under
                        # the assumption that it is context.
                        if (len(dd[current_list_id]) == 0) and previous_block:
                            # TODO: We used to add the previous block to the list but decided to separate this out.
                            #  Perhaps it's a good idea to add it back in but to the metadata, so that we can
                            #  validate the assumption that the previous block is context by pretty printing the list
                            #  when coding?

                            # Heuristic: If the list block is adjacent to the previous list block and the current
                            # list id was unpopulated and the start of this conditional, assume we are on the same
                            # list but on a new page, appending the appropriate metadata to custom attributes. We
                            # likely need to add some logic to handle the case where the previous list is more than 1
                            # element away solely due to garbage text blocks at the end of the page
                            # (which we should remove upstream) but for now this will capture many cases.
                            # TODO: Perhaps add some more nuance here, as another possibility is that it's contiguous
                            #  with the previous page but it's context/a list continuation.
                            if prev_list_ix + 1 == blocks_seen:
                                text_block = self._update_contiguity_attributes(
                                    text_block,
                                    "possibly_contiguous_with_previous_page_list",
                                )
                        else:
                            text_block = self._update_contiguity_attributes(
                                text_block,
                                "possibly_contiguous_with_same_page_context",
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
                grouped_block = self._update_custom_attributes(li)
                new_text_blocks.append(grouped_block)

            # If blocks have a repeated block id, only keep the final one: the others are context values
            # that are included in the list group.
            # Sort blocks by block index of the first attribute.
            # TODO: Look into why have we got pages with no list blocks?
            if len(new_text_blocks) > 0:
                new_text_blocks = self._remove_unmerged_lists(new_text_blocks)
            # In cases with 1 block on a page, sometimes coords appear ommitted. Add None. May affect downstream
            # processing.
            if len(new_text_blocks) == 1 and ("coords" not in new_text_blocks[0]):
                new_text_blocks[0]["coords"] = None
            # Convert to text block data class.
            # new_text_blocks = [TextBlock(**tb) for tb in new_text_blocks]
            newpage = {
                "text_blocks": new_text_blocks,
                "dimensions": page["dimensions"],
                "page_id": page["page_id"],
            }
            new_pages.append(newpage)

        new_contents = {"pages": new_pages}
        return new_contents

    def process(self, doc: Document, filename: str) -> Document:
        """
        Update a document object associated to a pdf by parse elements belonging to lists into single blocks,
        adding metadata on processing steps where appropriate.

        Args:
            filename: The filename of the pdf being processed.
            doc: Document for a single pdf.

        Returns:
            A Document object with elements that are associated to lists grouped together.
        """
        # Return original content dict and the grouped list blocks to overwrite original list elements with.
        doc = doc.to_dict()
        new_contents = self._group_list_elements(doc)
        new_contents["filename"] = filename
        return Document.from_dict(new_contents)
