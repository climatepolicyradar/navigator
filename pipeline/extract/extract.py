"""Module to extract embedded text in a PDF document using a PDF parser
"""

import os
from pathlib import Path
from tempfile import NamedTemporaryFile
import subprocess
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from .document import Document, TextBlock, BlockCoordinates
from .exceptions import DocumentTextExtractorException

SEPARATOR = " "


# TODO Nest textblocks inside pages
# TODO Add dimensions of each page (currently only stores the dimensions of the final page)
# TODO Get files from a named s3 bucket
# TODO Put output files in a named s3 bucket
# TODO Add method to Document to create a document from json


class DocumentTextExtractor:
    """Base class for extracting text from a document"""

    def extract(self, pdf_filepath: Path):
        """Extract text from the given document"""

        raise NotImplementedError


class DocumentEmbeddedTextExtractor(DocumentTextExtractor):
    """Extracts embedded text stored in a pdf document using the pdfalto pdf parser"""

    def __init__(self, pdfalto_path: Path = None, **kwargs):
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
        """Use pdfalto to parse the pdf file as an alto XML document and return it as an ElementTree"""

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

    def _get_text_block_coords(self, text_block: Element):
        tb_x = float(text_block.attrib.get("HPOS", 0))
        tb_y = float(text_block.attrib.get("VPOS", 0))
        tb_h = float(text_block.attrib.get("HEIGHT", 0))
        tb_w = float(text_block.attrib.get("WIDTH", 0))

        x1, y1 = tb_x, tb_y
        x2, y2 = tb_x + tb_w, tb_y
        x3, y3 = tb_x, tb_y + tb_h
        x4, y4 = tb_x + tb_w, tb_y + tb_h

        return (
            BlockCoordinates(x1, y1),
            BlockCoordinates(x2, y2),
            BlockCoordinates(x3, y3),
            BlockCoordinates(x4, y4),
        )

    def _get_page_dimensions(self, page: Element):
        w = float(page.attrib.get("WIDTH", 0))
        h = float(page.attrib.get("HEIGHT", 0))

        return w, h

    def _parse_alto_xml(self, pdf_xml: ElementTree, pdf_filename: Path) -> Document:
        """Parses the alto xml document and returns document structure"""

        # Define the alto namespace used in the document
        xml_namespace = {"alto": "http://www.loc.gov/standards/alto/ns-v3#"}

        # Get the pages in the document
        pages = pdf_xml.findall("alto:Layout/alto:Page", xml_namespace)

        SEP = " "

        text_blocks = []

        # Iterate through each page and process the text blocks that they contain
        for page in pages:
            # Get the page id
            page_id = page.attrib.get("ID", None)
            # Get page dimensions
            page_dimensions = self._get_page_dimensions(page)
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
                    text_line_content = ""
                    for text in text_line.getchildren():
                        text_line_content = (
                            text_line_content + SEP + text.attrib.get("CONTENT", "")
                        )
                    text_block_lines.append(text_line_content)

                if len(text_block_lines) > 0:
                    text_blocks.append(
                        TextBlock(
                            text="".join(text_block_lines).strip(),
                            text_block_id=text_block_id,
                            page_id=page_id,
                            coords=text_block_coords,
                        )
                    )

        return Document(text_blocks, pdf_filename, page_dimensions)

    def extract(self, pdf_filepath: Path) -> Document:
        pdf_alto_xml = self._pdf_to_xml(pdf_filepath)
        doc = self._parse_alto_xml(pdf_alto_xml, pdf_filepath.name)

        return doc
