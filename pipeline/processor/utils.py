import json
import pathlib

from pipeline.extract.document import Document, TextBlock, Page

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