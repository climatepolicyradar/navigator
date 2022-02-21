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


import os
from pathlib import Path
from tempfile import NamedTemporaryFile
import subprocess
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from typing import Optional, Tuple, List

from .document import Document, Page, TextBlock
from .exceptions import DocumentTextExtractorException


SEPARATOR = " "


class DocumentTextExtractor:
    """Base class for extracting text from a document."""

    def extract(self, pdf_filepath: Path):
        """Extract text from the given document"""

        raise NotImplementedError


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

    def _pdf_to_xml(self, pdf_filepath: Path) -> ElementTree:
        """Convert a pdf file to xml using the alto xml schema.

        Use pdfalto to parse the pdf file as an alto XML document and return it as an XML ElementTree

        Args:
            pdf_filepath: Path to pdf file to process

        Returns:
            ElementTree representing the pdf XML as a tree where each node is represented by an Element.

        Raises:
            DocumentTextExtractorException: An error occurred calling pdfalto.
        """

        if not self._pdfalto_path.exists():
            raise DocumentTextExtractorException(
                "Path to pdfalto executable does not exist."
            )

        try:
            # Create a temporary file to store the xml output from pdfalto
            with NamedTemporaryFile() as xml_f:
                pdfalto_args = [
                    str(self._pdfalto_path),
                    "-noImage",
                    "-outline",
                    "-readingOrder",
                    str(pdf_filepath),
                    xml_f.name,
                ]

                subprocess.run(pdfalto_args, check=True)

                return ElementTree.parse(xml_f.name).getroot()

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

    def _parse_alto_xml(self, pdf_xml: ElementTree, pdf_filename: Path) -> Document:
        """Parse the alto xml document and returns document structure.

        Processes the xml document tree and returns the document structure as a
        list of text blocks within the document

        Args:
            pdf_xml: XML tree representing document structure
            pdf_filename: Name of pdf file being processed.

        Returns:
            An instance of a Document containing the document structure and text.
        """

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

    def extract(self, pdf_filepath: Path) -> Document:
        """Extracts the text from a given pdf file and returns document structure.

        Args:
            pdf_filepath: /path/to/pdf/file to process

        Returns:
            An instance of a Document containing the document structure and text.
        """

        pdf_alto_xml = self._pdf_to_xml(pdf_filepath)
        doc = self._parse_alto_xml(pdf_alto_xml, pdf_filepath.name)

        return doc
