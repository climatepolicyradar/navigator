import os
import json
from pathlib import Path
import pytest
from extract.document import Document, Page, TextBlock
from extract.extract import DocumentEmbeddedTextExtractor


@pytest.fixture
def test_pdf_path():
    """Return path to test pdf"""

    return Path(__file__).parent / "data/cclw-1318-d7f66920a18e4ddf94c83cf21fa2bcfa.pdf"


@pytest.fixture
def document():
    """Setup a test Document"""

    page = Page(
        text_blocks=[
            TextBlock(
                ["paragraph 1 line 1", "paragraph 1 line 2", "paragraph 1 line 3"],
                "p1_b1",
                coords=[(1, 1), (1, 2), (2, 2), (2, 1)],
            ),
            TextBlock(
                ["paragraph 2 line 1", "paragraph 2 line 2", "paragraph 2 line 3"],
                "p1_b2",
                coords=[(1, 1), (1, 2), (2, 2), (2, 1)],
            ),
        ],
        dimensions=(4, 4),
        page_id=1,
    )

    return Document([page], "test_document.pdf")


def test_document_save_json(document, tmpdir):
    """Test to check that a document can be saved to a json file"""

    output_path = os.path.join(tmpdir, "test_document.json")

    document.save_json(output_path)

    assert os.path.exists(output_path)
    assert len(tmpdir.listdir()) == 1

    with open(output_path, "r") as f:
        doc_data = json.load(f)

    assert doc_data == {
        "pages": [
            {
                "dimensions": [4, 4],
                "page_id": 1,
                "text_blocks": [
                    {
                        "coords": [[1, 1], [1, 2], [2, 2], [2, 1]],
                        "text": [
                            "paragraph 1 line 1",
                            "paragraph 1 line 2",
                            "paragraph 1 line 3",
                        ],
                        "text_block_id": "p1_b1",
                    },
                    {
                        "coords": [[1, 1], [1, 2], [2, 2], [2, 1]],
                        "text": [
                            "paragraph 2 line 1",
                            "paragraph 2 line 2",
                            "paragraph 2 line 3",
                        ],
                        "text_block_id": "p1_b2",
                    },
                ],
            }
        ],
        "filename": "test_document.pdf",
    }


def test_document_to_string(document):
    """Test to check that the document can be output to a string"""

    document_lines = [
        "paragraph 1 line 1 paragraph 1 line 2 paragraph 1 line 3",
        "paragraph 2 line 1 paragraph 2 line 2 paragraph 2 line 3",
    ]

    for line_ix, line in enumerate(document.to_string().split("\n")):
        assert document_lines[line_ix] == line


def test_document_save_text(document, tmpdir):
    """Test to check that the document can be saved as a text file"""

    output_path = os.path.join(tmpdir, "test_document.txt")

    document.save_text(output_path)

    document_lines = [
        "paragraph 1 line 1 paragraph 1 line 2 paragraph 1 line 3\n",
        "paragraph 2 line 1 paragraph 2 line 2 paragraph 2 line 3",
    ]

    assert os.path.exists(output_path)
    assert len(tmpdir.listdir()) == 1

    with open(output_path, "r") as f:
        for line_ix, line in enumerate(f):
            assert document_lines[line_ix] == line


def test_document_from_json(tmp_path):
    """Test that a document can be created from a json file"""

    with pytest.raises(NotImplementedError):
        _ = Document.from_json(tmp_path / "test.json")


def test_embedded_text_extractor(test_pdf_path):
    """Test to check that text can be extracted from a test pdf file"""

    text_extractor = DocumentEmbeddedTextExtractor()
    doc = text_extractor.extract(test_pdf_path)

    # Check that the filename matches the filename of the pdf
    assert doc.filename == test_pdf_path.name

    # Check that 6 pages have been returned in the document
    assert len(doc.pages) == 6

    # Check that text has been returned on the first page
    assert len(doc.pages[0].text_blocks) > 0

    # Check that the first text block has at least 4 coordinates, where each coordinate is a tuple of floats
    assert len(doc.pages[0].text_blocks[0].coords) >= 4
    assert type(doc.pages[0].text_blocks[0].coords[0]) == tuple
    assert type(doc.pages[0].text_blocks[0].coords[0][0]) == float
