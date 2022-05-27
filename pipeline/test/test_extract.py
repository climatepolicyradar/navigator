import os
import json
from pathlib import Path
import shutil

import pytest
from adobe.pdfservices.operation.io.file_ref import FileRef
from adobe.pdfservices.operation.internal.io.file_ref_impl import FileRefImpl
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException
from PyPDF2 import PdfFileReader

from extract.document import Document, Page, TextBlock
from extract.extract import DocumentEmbeddedTextExtractor, AdobeAPIExtractor
from extract.utils import split_pdf


@pytest.fixture
def test_pdf_path() -> Path:
    """Return path to test pdf"""

    return Path(__file__).parent / "data/cclw-1318-d7f66920a18e4ddf94c83cf21fa2bcfa.pdf"


@pytest.fixture
def test_pdf_no_pages(test_pdf_path) -> int:
    """Number of pages in test PDF"""

    return PdfFileReader(open(test_pdf_path, "rb")).numPages


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

    return Document([page], "test_document.pdf", "86a2bb05b4358f8ce654f4121d4f7874")


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
                        "path": None,
                        "type": None,
                        "custom_attributes": None,
                    },
                    {
                        "coords": [[1, 1], [1, 2], [2, 2], [2, 1]],
                        "text": [
                            "paragraph 2 line 1",
                            "paragraph 2 line 2",
                            "paragraph 2 line 3",
                        ],
                        "text_block_id": "p1_b2",
                        "path": None,
                        "type": None,
                        "custom_attributes": None,
                    },
                ],
            }
        ],
        "filename": "test_document.pdf",
        "md5hash": "86a2bb05b4358f8ce654f4121d4f7874",
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


# def test_document_from_json(tmp_path):
#     """Test that a document can be created from a json file"""
#
#     with pytest.raises(NotImplementedError):
#         _ = Document.from_json(tmp_path / "test.json")


def test_embedded_text_extractor(test_pdf_path, tmp_path):
    """Test to check that text can be extracted from a test pdf file"""

    data_output_dir = tmp_path
    text_extractor = DocumentEmbeddedTextExtractor()
    doc = text_extractor.extract(test_pdf_path, data_output_dir)

    # Check that the filename matches the filename of the pdf
    assert doc.filename == test_pdf_path.name.strip(".pdf")

    # Check that 6 pages have been returned in the document
    assert len(doc.pages) == 6

    # Check that text has been returned on the first page
    assert len(doc.pages[0].text_blocks) > 0

    # Check that the first text block has at least 4 coordinates, where each coordinate is a tuple of floats
    assert len(doc.pages[0].text_blocks[0].coords) >= 4
    assert type(doc.pages[0].text_blocks[0].coords[0]) == tuple
    assert type(doc.pages[0].text_blocks[0].coords[0][0]) == float


def get_sample_adobe_fileref(*args, **kwargs):
    sample_path = Path(__file__).parent / "data/sample_adobe_output.zip"
    return FileRef.create_from_local_file(str(sample_path))


def mock_file_ref_impl_save_as(self, destination_file_path):
    abs_path = os.path.abspath(destination_file_path)
    dir = os.path.dirname(abs_path)
    if not os.path.exists(dir):
        os.mkdir(dir)
    if not os.path.exists(abs_path):
        shutil.copy(self._file_path, abs_path)
        return


def test_adobe_text_extractor(test_pdf_path, tmp_path, mocker):

    mocker.patch.object(FileRefImpl, "save_as", new=mock_file_ref_impl_save_as)
    mocker.patch.object(
        AdobeAPIExtractor, "_get_adobe_api_result", new=get_sample_adobe_fileref
    )

    data_output_dir = tmp_path / "data"
    os.mkdir(data_output_dir)

    text_extractor = AdobeAPIExtractor(credentials_path="fake/path")

    doc = text_extractor.extract(
        test_pdf_path,
        data_output_dir=data_output_dir,
    )

    assert doc.filename == test_pdf_path.name

    # The returned document can have up to 8 pages (the number of pages in the original PDF).
    # Pages with no parsed content (e.g. all figures) won't be added to the document.
    assert len(doc.pages) == 8

    # Every page in the Adobe output should have text blocks, as pages are only created if there are text blocks
    assert all([len(page.text_blocks) > 0 for page in doc.pages])

    # Check that text blocks all have paths and types
    assert all(
        [text_block.path for page in doc.pages for text_block in page.text_blocks]
    )
    assert all(
        [text_block.type for page in doc.pages for text_block in page.text_blocks]
    )

    # Check that files have been successfully unzipped and stored and that split_dir is empty
    assert os.listdir(data_output_dir) == [test_pdf_path.stem]
    assert sorted(os.listdir(data_output_dir / test_pdf_path.stem)) == [
        "figures",
        "structuredData.json",
    ]


def mock_get_adobe_api_result_raise_exception(
    self, pdf_filepath: Path, test_pdf_no_pages
):
    PAGE_LIMIT = 6

    if test_pdf_no_pages > PAGE_LIMIT:
        raise ServiceApiException(
            message="DISQUALIFIED - File not suitable for content extraction: File exceeds page limit",
            request_tracking_id="arbitrary",
        )
    else:
        return get_sample_adobe_fileref()


def test_adobe_text_extractor_with_pdf_split(
    test_pdf_path, tmp_path, test_pdf_no_pages, mocker
):
    """Test that document splitting works in AdobeAPIExtractor.extract as expected."""
    mocker.patch.object(FileRefImpl, "save_as", new=mock_file_ref_impl_save_as)
    mocker.patch.object(
        AdobeAPIExtractor,
        "_get_adobe_api_result",
        new=lambda self, x: mock_get_adobe_api_result_raise_exception(
            self, x, test_pdf_no_pages
        ),
    )

    data_output_dir = tmp_path / "data"
    os.mkdir(data_output_dir)

    text_extractor = AdobeAPIExtractor(credentials_path="fake/path")
    # Set API max pages limit to 5 - this means the extractor should split the 8 page input PDF into 5 and 3 page PDFs.
    text_extractor.API_MAX_PAGES = 5
    doc = text_extractor.extract(
        test_pdf_path,
        data_output_dir=data_output_dir,
    )

    # Note the returned documents will just be two instances of the same document because of the way that the mocking is set up.
    # We know the document in test_pdf_path has 8 pages so can still test for that.
    assert isinstance(doc, Document)
    assert len(doc.pages) == 8
    assert doc.filename == test_pdf_path.name


def mock_get_adobe_pdf_to_data_split_results(*args, **kwargs):
    return [
        Path(__file__).parent / "data/split_test_1.json",
        Path(__file__).parent / "data/split_test_2.json",
    ]


def test_adobe_text_extractor_with_pdf_split_valid_document_returned(
    test_pdf_path, mocker
):
    """Test that AdobePDFExtractor.extract correctly handles a case when it's given two Adobe JSON paths which represent two parts of the same PDF file."""
    mocker.patch.object(
        AdobeAPIExtractor, "pdf_to_data", new=mock_get_adobe_pdf_to_data_split_results
    )

    text_extractor = AdobeAPIExtractor(credentials_path="fake/path")
    doc = text_extractor.extract(
        test_pdf_path,
        data_output_dir=Path(""),
    )

    # All text block IDs should be unique
    text_block_ids = [
        text_block.text_block_id
        for page in doc.pages
        for text_block in page.text_blocks
    ]
    assert len(set(text_block_ids)) == len(text_block_ids)

    # All page IDs should be unique
    page_ids = [page.page_id for page in doc.pages]
    assert len(set(page_ids)) == len(page_ids)


def test_split_pdf(test_pdf_path, tmpdir):
    # PDF in test path has 6 pages.
    max_pages_per_split = 4
    orig_file_stem = Path(test_pdf_path).stem

    split_pdf(test_pdf_path, max_pages_per_split=max_pages_per_split, output_dir=tmpdir)

    target_filenames = [
        f"{orig_file_stem}_split_0_maxpages_{max_pages_per_split}.pdf",
        f"{orig_file_stem}_split_1_maxpages_{max_pages_per_split}.pdf",
    ]
    target_filepaths = [os.path.join(tmpdir, filename) for filename in target_filenames]

    # Test that correct number of files are in tmpdir.
    assert len(os.listdir(tmpdir)) == 2

    # Test that filenames are correct.
    assert sorted(os.listdir(tmpdir)) == target_filenames

    # First split page should have 4 pages, second should have 2 pages.
    assert [
        PdfFileReader(open(_pdf_path, "rb")).numPages for _pdf_path in target_filepaths
    ] == [4, 2]
