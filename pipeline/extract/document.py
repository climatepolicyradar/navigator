"""Defines data classes storing the state of a document and text in that document
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
    """Represents an individual text block on a page"""

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
    """Represents text blocks in a document"""

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
    def from_json(json_filepath: Path):
        """Create a new Document instance from a given json file"""
        raise NotImplementedError
