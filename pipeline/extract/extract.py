"""Module to extract embedded text in a PDF document using a PDF parser
"""

import json
from pathlib import Path
from typing import Optional, List
from dataclasses import dataclass
from tempfile import TemporaryFile
import subprocess
from xml.etree import ElementTree


class DocumentTextExtractorException(Exception):
    pass


@dataclass
class TextBlock:
    """Represents an individual text block on a page"""

    text: str
    text_block_id: str
    page_id: str


@dataclass
class Document:
    """Represents text blocks in a document"""

    text_blocks: List[TextBlock] = None
    filename: str = None


class DocumentTextExtractor:
    """Base class for extracting text from a document"""

    def __init__(
        self,
        pdf_filepath: Path,
        output_path: Optional[Path] = None,
        output_textfile: bool = True,
        output_json: bool = True,
    ):
        self._pdf_filepath = pdf_filepath
        self._output_path = output_path
        self._output_textfile = output_textfile
        self._output_json = output_json

        # Attribute storing document structure following call to self.extract() method
        self._doc = Document()

        self._SEPARATOR = " "

    def extract(self):
        """Extract text from the given document"""
        return self._doc

    def save_json(self, json_filepath: Path):
        """Save the document contents to json"""

        with open(json_filepath, "wt") as f:
            json.dump(self._doc, f, indent=2)

    def to_string(self):
        """Return the document contents as a string"""
        doc_text = ""
        for text_block in self._doc.text_blocks:
            doc_text = doc_text + self._SEPARATOR + text_block.text.strip() + "\n"

        return doc_text

    def save_text(self, text_filepath: Path):
        """Save the document contents to a text file"""

        with open(text_filepath, "wt") as f:
            f.write(self.to_string())


class DocumentEmbeddedTextExtractor(DocumentTextExtractor):
    """Extracts embedded text stored in a pdf document using the pdfalto pdf parser"""

    def __init__(self, pdfalto_path: Path, **kwargs):
        # Call constructor on base class
        super().__init__(**kwargs)

        self._pdfalto_path = pdfalto_path

    def _pdf_to_xml(self):
        """Use pdfalto to parse the pdf file as an alto XML document and return it as an ElementTree"""

        if not self._pdfalto_path.exists():
            raise DocumentTextExtractorException(
                "Path to pdfalto executable does not exist."
            )

        try:
            # Create a temporary file to store the xml output from pdfalto
            with TemporaryFile() as xml_f:
                pdfalto_args = [
                    self._pdfalto_path,
                    "-noImage",
                    "-outline",
                    "-readingOrder",
                    self._pdf_filepath,
                    xml_f.name,
                ]

                subprocess.run(pdfalto_args, check=True)

            return ElementTree.parse(xml_f.name).getroot()

        except subprocess.CalledProcessError:
            raise DocumentTextExtractorException("Exception occurred calling pdfalto.")

    def _parse_alto_xml(self, pdf_xml: ElementTree):
        """Parses the alto xml document and returns document structure"""

        # Define the alto namespace used in the document
        xml_namespace = {"alto": "http://www.loc.gov/standards/alto/ns-v3#"}

        # Get the pages in the document
        pages = pdf_xml.findall("alto:Layout/altoPage", xml_namespace)

        SEP = " "

        text_blocks = []

        # Iterate through each page and process the text blocks that they contain
        for page in pages:
            # Get the page id
            page_id = page.attrib.get("ID", None)
            # Iterate through page text blocks
            for text_block in page.findall(
                "alto:PrintSpace/alto:TextBlock", xml_namespace
            ):
                # Get the text block id
                text_block_id = text_block.attrib.get("ID", None)
                text_block_lines = []
                # Iterate through the lines in the text block and merge lines into a single string
                for text_line in text_block.getchildren():
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
                        )
                    )

        return Document(text_blocks, self._pdf_filename)
