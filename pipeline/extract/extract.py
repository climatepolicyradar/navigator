"""Extract text from a PDF document using a PDF parser.

Provides extractor classes which implement text extraction from a PDF document. These can extract
text directly embedded in a PDF, or third party apis or libraries to extract the text using
OCR or similar. The DocumentTextExtractor class should be overriden to implement a new extractor.
DocumentEmbeddedTextExtractor implements an embedded text extractor.

    Typical usage example:

    # Make sure path to pdfalto is configured in environment variable
    # (usually done outside code)
    import os
    os.putenv("PDFALTO_PATH", "/path/to/pdfalto")

    # Define path to pdf file to process
    pdf_filepath = Path("/path/to/pdf")

    # Initialise extractor and extract text from document
    extractor = DocumentEmbeddedTextExtractor()
    doc = extractor.extract(pdf_filepath)
"""

import logging
import os
from pathlib import Path
import subprocess
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
import re
import shutil
from collections import defaultdict
import json
from typing import Optional, Tuple, List

from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.exception.exceptions import (
    ServiceApiException,
)
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_pdf_options import (
    ExtractPDFOptions,
)
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_element_type import (
    ExtractElementType,
)
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_renditions_element_type import (
    ExtractRenditionsElementType,
)
from adobe.pdfservices.operation.pdfops.options.extractpdf.table_structure_type import (
    TableStructureType,
)
from adobe.pdfservices.operation.execution_context import ExecutionContext
from adobe.pdfservices.operation.client_config import ClientConfig
from adobe.pdfservices.operation.io.file_ref import FileRef
from adobe.pdfservices.operation.pdfops.extract_pdf_operation import ExtractPDFOperation

from .document import Document, Page, TextBlock
from .exceptions import DocumentTextExtractorException
from .utils import split_pdf


class DocumentTextExtractor:
    """Base class for extracting text from a document."""

    def pdf_to_data(
        self,
        pdf_filepath: Path,
        output_dir: Path,
        pdf_name: Optional[str] = None,
        **kwargs,
    ):
        """Extract information from the given document and save the results to an output path."""
        raise NotImplementedError

    def data_to_document(self, data_path: Optional[Path] = None, **kwargs) -> Document:
        """Convert data outputted by `pdf_to_data` into a `Document` object."""
        raise NotImplementedError

    def extract(
        self,
        pdf_filepath: Path,
        data_output_dir: Path,
        pdf_name: Optional[str] = None,
        **kwargs,
    ):
        """Extract text from the given document."""
        raise NotImplementedError


class DocumentEmbeddedTextExtractor(DocumentTextExtractor):
    """Extracts embedded text stored in a pdf document using the pdfalto pdf parser.

    This extractor can be used to extract text embedded in a pdf document. It uses
    the pdfalto pdf parser (used by grobid) to perform the extraction.

    The path to pdfalto may be defined by specifying the path in the constructor, or
    by setting the environment variable PDFALTO_PATH to the appropriate path.
    """

    def __init__(self, pdfalto_path: Optional[Path] = None, **kwargs):
        """Initialise the document embedded text extractor.

        Args:
            pdfalto_path: Optional Path to pdfalto executable
                (may be specified instead using the PDFALTO_PATH environment variable)
        """
        # Call constructor on base class
        super().__init__(**kwargs)

        pdfalto_path = (
            pdfalto_path if pdfalto_path else Path(os.environ.get("PDFALTO_PATH", None))
        )

        if pdfalto_path is None:
            raise DocumentTextExtractorException(
                "Path to pdfalto not specified in constructor or PDFALTO_PATH environment variable."
            )

        self._pdfalto_path = pdfalto_path

    def pdf_to_data(
        self, pdf_filepath: Path, output_dir: Path, pdf_name: Optional[str] = None
    ):
        """Convert a pdf file to xml using the alto xml schema.

        Use pdfalto to parse the pdf file as an alto XML document and save it to `output_path`.

        Args:
            pdf_filepath: Path to pdf file to process
            output_dir: Path to export XML file to. The file will have the same name as the PDF, with an XML extension.
            pdf_name: (optional) name of the pdf file which will be used as the name of the output files,
                otherwise uses the filename given in pdf_filepath

        Raises:
            DocumentTextExtractorException: An error occurred calling pdfalto.
        """
        if not self._pdfalto_path.exists():
            raise DocumentTextExtractorException(
                "Path to pdfalto executable does not exist."
            )

        pdf_name = pdf_name if pdf_name is not None else pdf_filepath.stem
        xml_output_path = output_dir / f"{pdf_name}.xml"

        try:
            # Create a temporary file to store the xml output from pdfalto
            pdfalto_args = [
                str(self._pdfalto_path),
                "-noImage",
                "-outline",
                "-readingOrder",
                str(pdf_filepath),
                xml_output_path,
            ]

            subprocess.run(pdfalto_args, check=True)

        except subprocess.CalledProcessError:
            raise DocumentTextExtractorException(
                f"Exception occurred calling pdfalto for {pdf_name}."
            )

        return xml_output_path

    def _get_text_block_coords(self, text_block: Element) -> List[Tuple[float]]:
        """Get the coordinates of a text block element.

        Fetches the x, y, width and height coordinates from an alto xml text block element
        and returns as a list of x, y pairs.

        Args:
            text_block: Element representing a text block in the XML tree

        Returns:
            A list of four elements, where each element is a tuple containing the coordinate
            of each of the four corners of a rectangular text block.
        """
        tb_x = float(text_block.attrib.get("HPOS", 0))
        tb_y = float(text_block.attrib.get("VPOS", 0))
        tb_h = float(text_block.attrib.get("HEIGHT", 0))
        tb_w = float(text_block.attrib.get("WIDTH", 0))

        x1, y1 = tb_x, tb_y
        x2, y2 = tb_x + tb_w, tb_y
        x3, y3 = tb_x, tb_y + tb_h
        x4, y4 = tb_x + tb_w, tb_y + tb_h

        return [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]

    def _get_page_dimensions(self, page: Element):
        """Get the dimensions of a page."""
        w = float(page.attrib.get("WIDTH", 0))
        h = float(page.attrib.get("HEIGHT", 0))

        return w, h

    def data_to_document(self, data_path: Path, pdf_filename: Path) -> Document:
        """Parse the alto xml document and returns document structure.

        Processes the xml document tree and returns the document structure as a
        list of text blocks within the document

        Args:
            data path: path to XML file representing document structure
            pdf_filename: name of pdf file being processed.

        Returns:
            An instance of a Document containing the document structure and text.
        """
        pdf_xml = ElementTree.parse(data_path).getroot()

        # Define the alto namespace used in the document
        xml_namespace = {"alto": "http://www.loc.gov/standards/alto/ns-v3#"}

        # Get the pages in the document
        pages = pdf_xml.findall("alto:Layout/alto:Page", xml_namespace)

        SEP = " "

        document_pages = []

        # Iterate through each page and process the text blocks that they contain
        for page_ix, page in enumerate(pages):
            # Get the page id
            page_id = page_ix + 1
            # Get page dimensions
            page_dimensions = self._get_page_dimensions(page)

            page_text_blocks = []

            # Iterate through page text blocks
            for text_block in page.findall(
                "alto:PrintSpace/alto:TextBlock", xml_namespace
            ):
                # Get the text block id
                text_block_id = text_block.attrib.get("ID", None)
                text_block_lines = []
                # Iterate through the lines in the text block and merge lines into a single string
                for text_line in text_block.getchildren():
                    text_block_coords = self._get_text_block_coords(text_block)
                    text_line_content = []
                    for text in text_line.getchildren():
                        text_line_content.append(text.attrib.get("CONTENT", ""))
                    text_block_lines.append(SEP.join(text_line_content))

                if len(text_block_lines) > 0:
                    page_text_blocks.append(
                        TextBlock(
                            text=text_block_lines,
                            text_block_id=text_block_id,
                            coords=text_block_coords,
                        )
                    )

            document_pages.append(Page(page_text_blocks, page_dimensions, page_id))

        return Document(document_pages, pdf_filename)

    def extract(
        self, pdf_filepath: Path, data_output_dir: Path, pdf_name: Optional[str] = None
    ) -> Document:
        """Extract the text from a given pdf file and returns document structure.

        Args:
            pdf_filepath: /path/to/pdf/file to process
            data_output_dir: path to directory to output intermediate XML file produced by pdfalto.
            pdf_name: (optional) name of the pdf file which will be used as the name of the output files,
                otherwise uses the filename given in pdf_filepath

        Returns:
            An instance of a Document containing the document structure and text.
        """
        xml_path = self.pdf_to_data(pdf_filepath, data_output_dir, pdf_name)
        doc = self.data_to_document(xml_path, pdf_filepath.name)

        return doc


class AdobeAPIExtractor(DocumentTextExtractor):
    """Extract text from pdf files using the Adobe PDF Services Extract API."""

    def __init__(self, credentials_path: str, **kwargs):
        """Extract text from a PDF document using Adobe PDF extract API.

        Extracts text from a PDF document using the Adobe PDF extract API. Also saves interim results, so API calls
        don't need to be re-run.

        Args:
            credentials_path: the path to the JSON file containing Adobe PDF services API credentials. A `private.key`
            file must also exist in the same folder.
        """
        super().__init__(**kwargs)
        self._elements_exclude = [
            "Aside",
            "Figure",
            "Footnote",
            "Reference",
            "TOC",
            "Watermark",
            "Table",
        ]
        # Maximum clockwise or anti-clockwise rotation a text element can have, otherwise it's excluded from the parsing results.
        self._max_rotation_degrees = 20

        self._credentials_path = credentials_path

        # Number of pages to limit each PDF to whether scanned or not scanned.
        # These values are used to split a PDF if the API returns a "File exceeds page limit" error.
        self.API_MAX_PAGES = 50
        self.API_SCANNED_MAX_PAGES = 25

    @staticmethod
    def _load_credentials(credentials_path: str) -> ExecutionContext:
        """Load credentials given the path to a credentials JSON file.

        Args:
            credentials_path: path to credentials JSON file.

        Returns:
            ExecutionContext: context used to run API calls using the PDF services SDK.
        """
        credentials = (
            Credentials.service_account_credentials_builder()
            .from_file(credentials_path)
            .build()
        )

        # Timeouts are in milliseconds. We've set these high as Python requests' None option
        # isn't supported by the Adobe SDK.
        client_config = (
            ClientConfig.Builder().with_connect_timeout(1e12).with_read_timeout(1e12)
        )

        # Create an ExecutionContext using credentials and create a new operation instance.
        return ExecutionContext.create(credentials, client_config)

    @staticmethod
    def _flatten_data(data: dict) -> dict:
        """Flattens Kids elements in returned Adobe JSON.

        Adobe data contains Kids elements which aim to encode sub-elements of an element.
        This method flattens all Kids elements out in the returned Adobe JSON as they are unreliable.

        Args:
            data (dict): JSON data returned by the Adobe Extract API.

        Returns:
            dict: flattened JSON data
        """
        new_data = {k: v for k, v in data.items() if k != "elements"}
        new_data["elements"] = []

        for el in data["elements"]:
            if "Kids" in el:
                # We take all the properties of the parent and pass them
                # to the each kid, but the kid can overwrite any properties
                # passed to it by the parent (e.g. bounding boxes).
                # This enables propagating page numbers, language prediction
                # and other properties to the kids.
                parent = {k: v for k, v in el.items() if k != "Kids"}
                for kid in el["Kids"]:
                    new_kid = parent.copy()
                    new_kid.update(kid)
                    new_data["elements"].append(kid)
            else:
                new_data["elements"].append(el)

        return new_data

    @staticmethod
    def _get_lines(char_bounds: List[List[float]]) -> List[Tuple[float, float]]:
        """Detect lines given a set of character bounds.

        Args:
            char_bounds: a list of character bounds. Each bound is in the form `x0,y0,x1,y1`.

        Returns:
            lines: list of [ymin, ymax] coordinates for each line with no overlaps, in ascending order.
        """
        # Get lines as ymin and ymax coordinates of each character bounds
        lines = [list(x) for x in set([(i[1], i[3]) for i in char_bounds])]
        lines.sort(key=lambda interval: interval[0])

        # Merge overlapping lines
        merged = [lines[0]]
        for current in lines:
            previous = merged[-1]
            if current[0] <= previous[1]:
                previous[1] = max(previous[1], current[1])
            else:
                merged.append(current)

        return merged

    @staticmethod
    def _get_line_number_of_char_bound(
        char_bound: List[float], lines: List[Tuple[float, float]]
    ):
        """Return the index of a line given a character bound.

        Args:
            char_bound: in the form [x0, y0, x1, y1].
            lines: returned by `_get_lines`.

        Returns:
            _type_: _description_
        """
        in_line_bool_array = [
            char_bound[1] >= line[0] and char_bound[3] <= line[1] for line in lines
        ]
        line_number_list = [idx for idx, val in enumerate(in_line_bool_array) if val]

        if len(line_number_list) != 1:
            logging.warning(
                "Method _get_line_number_of_char_bound found that a character was a member of zero or multiple lines. This will likely lead to an incorrect parsing result."
            )

        return line_number_list[0]

    def _element_to_text_block(self, element: dict, text_block_id: str) -> TextBlock:
        """Convert an element in the Adobe PDF Extract output JSON's `elements` into a `TextBlock`.

        Args:
            element: dictionary from `data['elements']`, where data is the JSON returned by the Adobe API.
            text_block_id: ID to give the text block

        Returns:
            TextBlock
        """
        char_bounds = element["CharBounds"]
        merged_lines = self._get_lines(char_bounds)
        chars_in_lines_idxs = [
            self._get_line_number_of_char_bound(char_bound, merged_lines)
            for char_bound in char_bounds
        ]
        line_change_idxs = (
            [0]
            + [
                i
                for i in range(1, len(chars_in_lines_idxs))
                if chars_in_lines_idxs[i] != chars_in_lines_idxs[i - 1]
            ]
            + [len(element["Text"])]
        )
        text_by_line = [
            element["Text"][line_change_idxs[idx] : line_change_idxs[idx + 1]]
            for idx in range(len(line_change_idxs) - 1)
        ]

        # Store custom attributes for StyleSpans which are nested under another element, e.g subscripts or underlines.
        # Also change their path to the path of their parent element to make them easier to merge later.
        # Type is left as StyleSpan.
        if (
            self._structure_path(element["Path"], remove_numbers=True)[-1]
            == "StyleSpan"
            and element.get("attributes")
            and element.get("Text")
        ):
            custom_attributes = element.get("attributes")
            path = self._structure_path(element["Path"], remove_numbers=False)[:-1]
        else:
            custom_attributes = None
            path = self._structure_path(element["Path"], remove_numbers=False)

        return TextBlock(
            text=text_by_line,
            text_block_id=text_block_id,
            coords=self._convert_coordinate_axis(element["Bounds"], element["Page"]),
            type=self._structure_path(element["Path"], remove_numbers=True)[-1],
            path=path,
            custom_attributes=custom_attributes,
        )

    def _convert_coordinate_axis(
        self, coords: List[float], page_number: int
    ) -> List[float]:
        """Convert coordinates so that the origin is at top left, rather than bottom left output by Adobe.

        Args:
            coords: list of coordinates output by Adobe: [x0, y0, x1, y1] with origin at bottom left.
            page_number: number of page output by Adobe. Indexed at 0.
        """
        page_height = self._current_data["pages"][page_number]["height"]

        # To reverse the coordinate system we subtract y0 and y1 from the page height and swap
        # them.
        return [coords[0], page_height - coords[3], coords[2], page_height - coords[1]]

    @staticmethod
    def _structure_path(path: str, remove_numbers: bool = True) -> List[str]:
        """Convert a PDF path into a list.

        E.g. '//Document/Aside[3]/P[2]' becomes ['Document', 'Aside', 'P'].

        Args:
            path: PDF path, string
            remove_numbers: if True, numbers in brackets are removed from the path as in the
            example above. If False, numbers are left in.
        """
        path_split = path[2:].split("/")

        if not remove_numbers:
            return path_split
        else:
            return [re.sub(r"\[\d+\]", "", i) for i in path_split]

    def data_to_document(self, data_path: Path, pdf_filename: str) -> Document:
        """Convert an Adobe Extract API JSON into a Document object.

        Args:
            data_path: path to JSON file outputted by Adobe API.
            pdf_filename: name or identifier for PDF - stored as an attribute in the returned `Document` object.

        Returns:
            Document
        """
        with open(data_path, "r") as f:
            data = json.load(f)

        page_id = 0
        block_counter = 1
        text_blocks_by_page = defaultdict(list)
        self._current_data = self._flatten_data(data)

        for el in self._current_data["elements"]:
            # Increment page_id and reset block_counter if starting new page.
            # Elements sometimes don't have page numbers, so in these cases we assume
            # the page hasn't changed.
            if el.get("Page", page_id) != page_id:
                block_counter = 1

            page_id = el.get("Page", page_id)

            # Ignore rotated text elements.
            element_rotation = (
                el.get("Rotation", 0) - data["pages"][page_id]["rotation"]
            )
            if (
                self._max_rotation_degrees
                < element_rotation
                < 360 - self._max_rotation_degrees
            ):
                continue

            # Only consider blocks that aren't in one of the types to exclude, and contain text.
            if not any(
                [e in self._structure_path(el["Path"]) for e in self._elements_exclude]
            ) and el.get("Text"):
                block_id = f"p{page_id}_b{block_counter}"
                text_blocks_by_page[page_id].append(
                    self._element_to_text_block(el, block_id)
                )
                block_counter += 1

        # Create pages from `text_blocks_by_page`, and a Document from these pages.
        pages = []

        for page_id, page_text_blocks in text_blocks_by_page.items():
            pages.append(
                Page(
                    text_blocks=page_text_blocks,
                    page_id=page_id,
                    dimensions=(
                        data["pages"][page_id]["width"],
                        data["pages"][page_id]["height"],
                    ),
                )
            )

        document = Document(
            pages=pages,
            filename=pdf_filename,
        )

        return document

    def _get_adobe_api_result(
        self,
        pdf_filepath: Path,
    ) -> FileRef:
        """Make a call to the Adobe PDF Extract API using the PDF services SDK.

        Args:
            pdf_filepath: path to a PDF

        Returns:
            FileRef representing ZIP file returned by API.
        """
        _execution_context = self._load_credentials(self._credentials_path)

        extract_pdf_operation = ExtractPDFOperation.create_new()

        source = FileRef.create_from_local_file(pdf_filepath)
        extract_pdf_operation.set_input(source)

        # Build ExtractPDF options and set them into the operation
        extract_pdf_options: ExtractPDFOptions = (
            ExtractPDFOptions.builder()
            .with_elements_to_extract(
                [ExtractElementType.TEXT, ExtractElementType.TABLES]
            )
            .with_elements_to_extract_renditions(
                [
                    ExtractRenditionsElementType.TABLES,
                    ExtractRenditionsElementType.FIGURES,
                ]
            )
            .with_include_styling_info(True)
            .with_get_char_info(True)
            .with_table_structure_format(TableStructureType.CSV)
            .build()
        )
        extract_pdf_operation.set_options(extract_pdf_options)
        result = extract_pdf_operation.execute(_execution_context)

        return result

    def pdf_to_data(
        self,
        pdf_filepath: Path,
        output_dir: Path,
        output_folder_pdf_splits: Path,
        pdf_name: Optional[str] = None,
    ) -> List[Path]:
        """Send document at `pdf_filepath` to the Adobe Extract API.

        Stores the data from the API in the `output_dir` folder.

        The Adobe Extract API has a variable page limit which is difficult to predict. To handle long PDFs this method
        splits a PDF into equal sized smaller PDFs and runs each through separately. These smaller PDFs are stored in
        `output_folder_pdf_splits`.

        Args:
            pdf_filepath: file path to a PDF.
            output_dir: folder path to store the PDF Extract API results in. These results are
            stored in a subfolder with the same name as the PDF.
            output_folder_pdf_splits: folder path to store the split PDFs.
            pdf_name: (optional) name of the pdf file which will be used as the name of the output files,
                otherwise uses the filename given in pdf_filepath

        Returns:
            List of paths to JSON files (pathlib.Path objects).
        """
        pdf_name = pdf_name if pdf_name is not None else pdf_filepath.stem

        try:
            result = self._get_adobe_api_result(pdf_filepath)
            output_dir = output_dir / pdf_name
            os.mkdir(output_dir)
            shutil.unpack_archive(result._file_path, output_dir)

            return [output_dir / "structuredData.json"]

        except ServiceApiException as e:
            # Raise any exception except for a 'File exceeds page limit' exception.
            if e.message not in [
                "DISQUALIFIED - File not suitable for content extraction: File exceeds page limit",
                "DISQUALIFIED - File not suitable for content extraction: Scanned file exceeds page limit",
            ]:
                raise (e)

            # If the exception is a 'File exceeds page limit' one, split the PDF and parse each split PDF separately.
            if (
                e.message
                == "DISQUALIFIED - File not suitable for content extraction: File exceeds page limit"
            ):
                split_page_limit = self.API_MAX_PAGES
            elif (
                e.message
                == "DISQUALIFIED - File not suitable for content extraction: Scanned file exceeds page limit"
            ):
                split_page_limit = self.API_SCANNED_MAX_PAGES

            split_paths = split_pdf(
                pdf_filepath, split_page_limit, output_folder_pdf_splits
            )
            logging.info(
                f"Failed due to 'file exceeds page limit error'. Retrying with PDF split into {len(split_paths)} separate PDFs with max page size {split_page_limit}."
            )

            json_paths = []
            for idx, pdf_path in enumerate(split_paths):
                split_output_dir = output_dir / f"{pdf_name}_{idx}"
                os.mkdir(split_output_dir)

                json_path = self.pdf_to_data(
                    pdf_filepath=pdf_path,
                    output_dir=split_output_dir,
                    output_folder_pdf_splits=output_folder_pdf_splits,
                    pdf_name=pdf_name,
                )

                json_paths += json_path

            return json_paths

    def extract(
        self,
        pdf_filepath: Path,
        data_output_dir: Path,
        output_folder_pdf_splits: Path,
        pdf_name: Optional[str] = None,
    ) -> Document:
        """Extract the text from a given pdf file and returns document structure.

        Args:
            pdf_filepath: /path/to/pdf/file to process.
            data_output_dir: folder to output Adobe Extract API data to.
            output_folder_pdf_splits: folder to store PDF splits. See `pdf_to_data` method.
            pdf_name: (optional) name of the pdf file which will be used as the name of the output files,
                otherwise uses the filename given in pdf_filepath

        Returns:
            An instance of a Document containing the document structure and text.
        """
        # In order to handle the case where documents have been split for processing,
        # the resulting pages of each split document are joined into a new Document
        # object which is returned.

        json_paths = self.pdf_to_data(
            pdf_filepath=pdf_filepath,
            output_dir=data_output_dir,
            output_folder_pdf_splits=output_folder_pdf_splits,
            pdf_name=pdf_name,
        )

        pages = []
        for _path in json_paths:
            temp_doc = self.data_to_document(
                data_path=_path, pdf_filename=pdf_filepath.name
            )

            pages += temp_doc.pages

        return Document(
            pages=pages,
            filename=pdf_filepath.name,
        )
