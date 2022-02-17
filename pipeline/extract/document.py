"""Defines data classes storing the state of a document and text in that document.

Provides classes which represent a document, the text it contains and positional information
of that text.

    Typical usage example:

    pdf_filename = "pdffile.pdf"

    text_blocks = [
        TextBlock(
            text="The first paragraph in the document",
            text_block_id="tb-1",
            page_id="page-1",
            coords=(
                BlockCoordinates(0, 0),
                BlockCoordinates(10, 0),
                BlockCoordinates(0, 20),
                BlockCoordinates(10, 20),
            )
        )
    ]

    doc = Document(
        text_blocks=text_blocks,
        filename="pdf_filename",
        dimensions=(500, 1000)
    )
"""

import json
from pathlib import Path
from typing import List, Tuple
from dataclasses import dataclass, asdict

SEPARATOR = " "


@dataclass
class BlockCoordinates:
    """An x, y coordinate for one of the vertices of the text block"""

    x: float
    y: float


@dataclass
class TextBlock:
    """Represents an individual text block on a page.

    Stores the text and positional information for a single
    text block extracted from a document.

    Attributes:
        text: Text contained in the text block
        text_block_id: Unique identifier for the text block
        page_id: Unique identifier for the page that the text block is contained in
        coords: Coordinates of each of the four corners of a rectangular text block.
    """

    text: str  # Text in text block
    text_block_id: str  # Unique identifier of text block
    page_id: str  # Unique identifier of page that this text block is contained icoords: Tuple[int, int, int, int]
    coords: Tuple[  # Coordinates of text block:
        BlockCoordinates,  # x1, y1
        BlockCoordinates,  # x2, y2
        BlockCoordinates,  # x3, y3
        BlockCoordinates,  # x4, y4
    ]


@dataclass
class Document:
    """Represents all text blocks contained in a document.

    Stores all of the text blocks that are contained in a document and the dimensions
    of the document.

    Attributes:
        text_blocks: List of text blocks contained in the document
        filename: Name of the pdf file
        dimensions: the size of a single page in the document
    """

    text_blocks: List[TextBlock] = None  # List of textblocks in the document
    filename: str = None  # Name of the pdf file that this document relates to
    dimensions: BlockCoordinates = None  # Width and height of the page

    def save_json(self, json_filepath: Path):
        """Save the document contents to json"""

        with open(json_filepath, "wt") as f:
            json.dump(asdict(self), f, indent=2)

    def to_string(self) -> str:
        """Return the document contents as a string"""
        doc_text = ""
        for text_block in self.text_blocks:
            doc_text = doc_text + SEPARATOR + text_block.text.strip() + "\n"

        return doc_text

    def save_text(self, text_filepath: Path):
        """Save the document contents to a text file"""

        with open(text_filepath, "wt") as f:
            f.write(self.to_string())

    @classmethod
    def from_json(cls, json_filepath: Path):
        """Create a new Document instance from a given json file"""
        raise NotImplementedError
