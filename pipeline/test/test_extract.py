import os
import json
import pytest
from extract.document import Document, TextBlock, BlockCoordinates, SEPARATOR


@pytest.fixture
def document():
    return Document(
        text_blocks=[
            TextBlock(
                "paragraph 1",
                "p1_b1",
                "p1",
                coords=[
                    BlockCoordinates(1, 1),
                    BlockCoordinates(1, 2),
                    BlockCoordinates(2, 2),
                    BlockCoordinates(2, 1),
                ],
            )
        ],
        filename="test_document.pdf",
        dimensions=BlockCoordinates(4, 4),
    )


def test_document_save_json(document, tmpdir):
    output_path = os.path.join(tmpdir, "test_document.json")

    document.save_json(output_path)

    assert os.path.exists(output_path)
    assert len(tmpdir.listdir()) == 1

    with open(output_path, "r") as f:
        doc_data = json.load(f)

    assert doc_data == {
        "filename": "test_document.pdf",
        "dimensions": {"x": 4, "y": 4},
        "text_blocks": [
            {
                "text": "paragraph 1",
                "text_block_id": "p1_b1",
                "page_id": "p1",
                "coords": [
                    {"x": 1, "y": 1},
                    {"x": 1, "y": 2},
                    {"x": 2, "y": 2},
                    {"x": 2, "y": 1},
                ],
            }
        ],
    }


def test_document_to_string(document):

    assert document.to_string() == SEPARATOR + "paragraph 1" + "\n"


def test_document_save_text(document, tmpdir):
    output_path = os.path.join(tmpdir, "test_document.txt")

    document.save_text(output_path)

    assert os.path.exists(output_path)
    assert len(tmpdir.listdir()) == 1

    with open(output_path, "r") as f:
        doc_txt = f.read()

    assert doc_txt == SEPARATOR + "paragraph 1" + "\n"


def test_document_from_json(tmp_path):
    with pytest.raises(NotImplementedError):
        _ = Document.from_json(tmp_path / "test.json")
