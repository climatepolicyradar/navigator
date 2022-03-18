import json
import pathlib
from typing import List, Iterable

from pipeline.extract.document import Document, TextBlock, Page


def minimal_bounding_box(coords: List[Iterable]) -> list:
    """
    Return the minimally enclosing bounding box of bounding boxes.

    Args:
        coords: A list of coordinates for each bounding box formatted [x1,y1,x2,y2] with the top left as the origin.

    Returns:
        A list of coordinates for the minimally enclosing bounding box for all input bounding boxes.

    """
    x_min = min(coord[0] for coord in coords)
    y_min = min(coord[1] for coord in coords)
    x_max = max(coord[2] for coord in coords)
    y_max = max(coord[3] for coord in coords)
    return [x_min, y_min, x_max, y_max]

def json_to_document(path: pathlib.Path) -> Document:
    with open(path, "r") as f:
        data = json.load(f)
    new_pages = []
    for ix, page in enumerate(data['pages']):
        new_blocks = []
        for block in page['text_blocks']:
            new_block = TextBlock(**block)
            new_blocks.append(new_block)
        page['text_blocks'] = new_blocks
        page = Page(**page)
        new_pages.append(page)
    data['pages'] = new_pages
    doc = Document(**data)
    return doc