from typing import List
import os
from pathlib import Path
import hashlib

from PyPDF2 import PdfFileReader, PdfFileWriter


def split_pdf(pdf_path: Path, max_pages_per_split: int, output_dir: Path) -> List[Path]:
    """Splits a PDF into smaller PDFs each with maximum size `max_pages_per_split`.

    Outputs the PDF in `output_dir` with the name `ORIGINAL_PDF_NAME_split_0_maxpages_100`,
    0 representing the order of the split in the original PDF, and 100 representing the
    value of the `max_pages_per_split` argument.

    Args:
        pdf_path: path to original PDF.
        max_pages_per_split: maximum pages per split. The last split PDF may have fewer pages than this.
        output_dir: directory to output smaller PDFs to.

    Returns:
        A list paths to the files created by this method.
    """
    input_pdf = PdfFileReader(open(pdf_path, "rb"))
    pages_range = range(input_pdf.numPages)
    pages_range_split = [
        pages_range[i : i + max_pages_per_split]
        for i in range(0, len(pages_range), max_pages_per_split)
    ]
    output_file_paths = []

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    for idx, split in enumerate(pages_range_split):
        output = PdfFileWriter()
        output_filename = f"{Path(pdf_path).stem}_split_{idx}_maxpages_{max_pages_per_split}{Path(pdf_path).suffix}"
        output_path = output_dir / output_filename
        output_file_paths.append(output_path)

        for i in split:
            output.addPage(input_pdf.getPage(i))

        with open(output_path, "wb") as outputStream:
            output.write(outputStream)

    return output_file_paths


def get_md5_hash(pdf_path: Path) -> str:
    """Return the MD5 hash of a PDF file.

    Args:
        pdf_path (Path): path to PDF

    Returns:
        str: hexadecimal MD5 hash
    """

    with open(pdf_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()
