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
from typing import List, Tuple, Optional
from dataclasses import dataclass, asdict


@dataclass
class TextBlock:
    """Represents an individual text block on a page.

    Stores the text and positional information for a single
    text block extracted from a document.

    Attributes:
        text: List of text lines contained in the text block
        text_block_id: Unique identifier for the text block
        coords: List of coordinates of the vertices defining the boundary of the text block.
           Each coordinate is a tuple in the format (x, y). (0, 0) is at the top left corner of
           the page, and the positive x- and y- directions are right and down.
    """

    text: List[str]  # Text in text block as a list of text lines
    text_block_id: str  # Unique identifier of text block
    coords: List[Tuple[float, float]]  # Coordinates of text block
    type: Optional[str] = None  # Type of text block
    path: Optional[List[str]] = None  # Path of text block. Similar to DOM tree in HTML.
    custom_attributes: Optional[
        dict
    ] = None  # Any attributes returned by the parser that can be used for post-processing.

    def to_string(self) -> str:
        """Returns the lines in a text block as a string with the lines separated by spaces."""

        return " ".join([line.strip() for line in self.text])


@dataclass
class Page:
    """Represents a page in a document.

    All text blocks on a page are contained within a Page object. Also, the dimensions of the page can
    be specified.

    Attributes:
       text_blocks: List of text blocks contained in the document
       dimensions: The dimensions of the page as a tuple in the format (x, y).
          where x is horizontal and y is vertical dimension.
       page_id: Unique id of the page, e.g. page number starting at 0.
    """

    text_blocks: List[TextBlock]
    dimensions: Tuple[float, float]
    page_id: int

    def to_string(self) -> str:
        """Return the text blocks in the page as a string"""

        page_text = [text_block.to_string().strip() for text_block in self.text_blocks]

        return "\n".join(page_text)


@dataclass
class Document:
    """Represents a document and associated pages and text blocks.

    Stores all of the pages that are contained in a document.

    Attributes:
        pages: List of pages contained in the document
        filename: Name of the pdf file
    """

    pages: List[Page]  # List of textblocks in the document
    filename: str  # Name of the pdf file that this document relates to
    md5hash: str  # MD5 hash of the pdf file

    def save_json(self, json_filepath: Path):
        """Save the document contents to json"""

        with open(json_filepath, "wt") as f:
            json.dump(asdict(self), f, indent=2)

    def to_dict(self) -> dict:
        """Return the document as a dictionary"""
        return asdict(self)

    def to_string(self) -> str:
        """Return the document contents as a string"""

        doc_text = [page.to_string() for page in self.pages]

        return "\n".join(doc_text)

    def save_text(self, text_filepath: Path):
        """Save the document contents to a text file"""

        with open(text_filepath, "wt") as f:
            f.write(self.to_string())

    @classmethod
    def from_dict(cls, json_dict: dict) -> "Document":
        """Load a document from a dictionary"""
        for page in json_dict["pages"]:
            page["text_blocks"] = [TextBlock(**block) for block in page["text_blocks"]]
        return cls(
            pages=[Page(**page) for page in json_dict["pages"]],
            filename=json_dict["filename"],
            md5hash=json_dict["md5hash"],
        )

    @classmethod
    def from_json(cls, json_filepath: Path):
        """Create a new Document instance from a given json file"""
        with open(json_filepath, "r") as f:
            data = json.load(f)

        new_pages = []
        for ix, page in enumerate(data["pages"]):
            new_blocks = []
            for block in page["text_blocks"]:
                new_block = TextBlock(**block)
                new_blocks.append(new_block)
            page["text_blocks"] = new_blocks
            page = Page(**page)
            new_pages.append(page)
        data["pages"] = new_pages
        doc = Document(**data)
        return doc
