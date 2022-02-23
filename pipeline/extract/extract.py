"""Extracts text from a PDF document using a PDF parser

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
from typing import Optional, Tuple, List

from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.exception.exceptions import (
    ServiceApiException,
    ServiceUsageException,
    SdkException,
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
from adobe.pdfservices.operation.io.file_ref import FileRef
from adobe.pdfservices.operation.pdfops.extract_pdf_operation import ExtractPDFOperation

from .document import Document, Page, TextBlock
from .exceptions import DocumentTextExtractorException
from .utils import split_pdf


SEPARATOR = " "


class DocumentTextExtractor:
    """Base class for extracting text from a document."""

    def pdf_to_data(self, pdf_filepath: Path, output_path: Path, **kwargs):
        """Extract information from the given document and save the results to an output path."""
        raise NotImplementedError

    def data_to_document(self, data_path: Optional[Path] = None, **kwargs) -> Document:
        raise NotImplementedError

    def extract(self, pdf_filepath: Path, data_output_path: Path):
        """Extract text from the given document"""

        self.pdf_to_data(pdf_filepath, data_output_path)
        document = self.data_to_document(data_output_path)

        return document


class DocumentEmbeddedTextExtractor(DocumentTextExtractor):
    """
    Extracts embedded text stored in a pdf document using the pdfalto pdf parser.

    This extractor can be used to extract text embedded in a pdf document. It uses
    the pdfalto pdf parser (used by grobid) to perform the extraction.

    The path to pdfalto may be defined by specifying the path in the constructor, or
    by setting the environment variable PDFALTO_PATH to the appropriate path.
    """

    def __init__(self, pdfalto_path: Optional[Path] = None, **kwargs):
        """Initialise the document embedded text extractor

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

    def pdf_to_data(self, pdf_filepath: Path, output_path: Path):
        """Convert a pdf file to xml using the alto xml schema.

        Use pdfalto to parse the pdf file as an alto XML document and save it to `output_path`.

        Args:
            pdf_filepath: Path to pdf file to process

        Raises:
            DocumentTextExtractorException: An error occurred calling pdfalto.
        """

        if not self._pdfalto_path.exists():
            raise DocumentTextExtractorException(
                "Path to pdfalto executable does not exist."
            )

        try:
            # Create a temporary file to store the xml output from pdfalto
            pdfalto_args = [
                str(self._pdfalto_path),
                "-noImage",
                "-outline",
                "-readingOrder",
                str(pdf_filepath),
                output_path.name,
            ]

            subprocess.run(pdfalto_args, check=True)

        except subprocess.CalledProcessError:
            raise DocumentTextExtractorException("Exception occurred calling pdfalto.")

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
        """Gets the dimensions of a page."""

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

    def extract(self, pdf_filepath: Path, data_output_path: Path) -> Document:
        """Extracts the text from a given pdf file and returns document structure.

        Args:
            pdf_filepath: /path/to/pdf/file to process

        Returns:
            An instance of a Document containing the document structure and text.
        """
        self.pdf_to_data(pdf_filepath, data_output_path)
        doc = self.data_to_document(data_output_path, pdf_filepath.name)

        return doc


class AdobeAPIExtractor(DocumentTextExtractor):
    def __init__(self, credentials_path: str, **kwargs):
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

        self._execution_context = self._setup_credentials(credentials_path)

        # Number of pages to limit each PDF to whether scanned or not scanned
        self.API_MAX_PAGES = 100
        self.API_SCANNED_MAX_PAGES = 50

    def _setup_credentials(credentials_path: str) -> ExecutionContext:
        credentials = (
            Credentials.service_account_credentials_builder()
            .from_file(credentials_path)
            .build()
        )

        # Create an ExecutionContext using credentials and create a new operation instance.
        return ExecutionContext.create(credentials)

    @staticmethod
    def _flatten_data(data: dict) -> dict:
        """Flatten out 'Kids' elements which refer to PDF structure."""
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
    def _get_lines(char_bounds) -> List[Tuple[float, float]]:
        """Get and merge lines.

        Args:
            char_bounds (_type_): _description_

        Returns:
            _type_: _description_
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
    def _get_line_number_of_char_bound(char_bound, lines):
        in_line_bool_array = [
            char_bound[1] >= line[0] and char_bound[3] <= line[1] for line in lines
        ]
        line_number_list = [idx for idx, val in enumerate(in_line_bool_array) if val]

        if len(line_number_list) != 1:
            raise Exception

        return line_number_list[0]

    def _element_to_text_block(self, el: dict, block_id: str) -> TextBlock:
        char_bounds = el["CharBounds"]
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
            + [len(el["Text"])]
        )
        text_by_line = [
            el["Text"][line_change_idxs[idx] : line_change_idxs[idx + 1]].strip()
            for idx in range(len(line_change_idxs) - 1)
        ]

        return TextBlock(
            text=text_by_line,
            text_block_id=block_id,
            coords=self._convert_coordinate_axis(el["Bounds"], el["Page"]),
            type=self._structure_path(el["Path"], remove_numbers=True)[-1],
            path=self._structure_path(el["Path"], remove_numbers=False),
        )

    def _convert_coordinate_axis(
        self, coords: List[float], page_number: int
    ) -> List[float]:
        """Convert coordinates so that the origin is at top left, rather than bottom left output by Adobe.

        Args:
            data: JSON data output by Adobe API.
            coords: list of coordinates output by Adobe: [x0, y0, x1, y1] with origin at bottom left.
            page_number: number of page output by Adobe. Indexed at 0.
        """
        page_height = self._current_data["pages"][page_number]["height"]

        # To reverse the coordinate system we subtract y0 and y1 from the page height and swap
        # them.
        return [coords[0], page_height - coords[3], coords[2], page_height - coords[1]]

    @staticmethod
    def _structure_path(path: str, remove_numbers: bool = True) -> List[str]:
        """
        Convert a PDF path into a list.
        E.g. '//Document/Aside[3]/P[2]' becomes['Document', 'Aside', 'P'].
        """

        path_split = path[2:].split("/")

        if not remove_numbers:
            return path_split
        else:
            return [re.sub(r"\[\d+\]", "", i) for i in path_split]

    @staticmethod
    def _index_of(val, in_list):
        try:
            return in_list.index(val)
        except ValueError:
            return None

    def _convert_data(self, data: dict, filename: str) -> Document:
        page_id = 0
        block_counter = 1
        text_blocks_by_page = defaultdict(list)
        self._current_data = self._flatten_data(data)

        for el in self._current_data["elements"]:
            # Ignore rotated text elements
            element_rotation = el.get("Rotation", 0)
            if (
                self._max_rotation_degrees
                < element_rotation
                < 360 - self._max_rotation_degrees
            ):
                continue

            # Ignore superscript
            if el.get("attributes", {}).get("TextPosition") == "Sup":
                continue

            # TODO: handle subscript

            if el["Page"] != page_id:
                page_id += 1
                block_counter = 1

            if not any(
                [e in self._structure_path(el["Path"]) for e in self._elements_exclude]
            ):
                block_id = f"p{page_id}_b{block_counter}"

                # Ignore blocks without any text which haven't already been excluded by type
                if "Text" in el:
                    text_blocks_by_page[page_id].append(
                        self._element_to_text_block(el, block_id)
                    )

                block_counter += 1

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
            filename=filename,
        )

        return document

    def pdf_to_adobe_zip(self, pdf_filepath: Path):
        """
        Parse doc and save parsing results to ./output folder.
        """

        input_name = Path(pdf_filepath).name
        output_path = f"./adobe-full-output/{input_name}"
        zip_output_path = f"{output_path}.zip"

        folder_path_for_splits = Path(pdf_filepath).parent

        if not os.path.exists(folder_path_for_splits):
            os.mkdir(folder_path_for_splits)

        try:
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

            # Execute the operation.
            result: FileRef = extract_pdf_operation.execute(self._execution_context)

            # Save the result to the specified location.
            result.save_as(zip_output_path)

            # Unzip zip file and remove it
            shutil.unpack_archive(zip_output_path, output_path)
            os.remove(zip_output_path)

        except (ServiceApiException, ServiceUsageException, SdkException) as e:
            if (
                isinstance(e, ServiceApiException)
                and e.message
                == "DISQUALIFIED - File not suitable for content extraction: File exceeds page limit"
            ):
                split_paths = split_pdf(
                    pdf_filepath, self.API_MAX_PAGES, folder_path_for_splits
                )
                logging.info(
                    f"Failed due to 'file exceeds page limit error'. Retrying with PDF split into {len(split_paths)} separate PDFs with max page size {self.API_MAX_PAGES}."
                )
                for p in split_paths:
                    self.pdf_to_adobe_zip(p, folder_path_for_splits)

            elif (
                isinstance(e, ServiceApiException)
                and e.message
                == "DISQUALIFIED - File not suitable for content extraction: Scanned file exceeds page limit"
            ):
                split_paths = split_pdf(
                    pdf_filepath, self.API_SCANNED_MAX_PAGES, folder_path_for_splits
                )
                logging.info(
                    f"Failed due to 'file exceeds page limit error'. Retrying with PDF split into {len(split_paths)} separate PDFs with max page size {self.API_SCANNED_MAX_PAGES}."
                )
                for p in split_paths:
                    self.pdf_to_adobe_zip(p, folder_path_for_splits)

            logging.exception(
                f"Exception encountered while executing operation for {pdf_filepath}"
            )

    def extract(self, pdf_filepath: Path) -> Document:
        """Extracts the text from a given pdf file and returns document structure.

        Args:
            pdf_filepath: /path/to/pdf/file to process

        Returns:
            An instance of a Document containing the document structure and text.
        """
