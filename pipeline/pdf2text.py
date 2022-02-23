"""CLI which extracts text from pdf documents in a directory.

Implements a cli which will extract the text contained in a set of pdf files in a directory.
"""

import argparse
from pathlib import Path

from extract.extract import DocumentEmbeddedTextExtractor
from extract.exceptions import DocumentTextExtractorException


def process(pdf_dir: Path, out_dir: Path, save_json: bool, save_text: bool):
    """Extracts text from text in a directory containing pdf files.

    Iterates through files with a .pdf extension in a given directory,
    and processes those files to extract text. Produces a .json and/or
    .txt file containing extracted text and associated positional data.

    Args@
        pdf_dir: Path to input pdf files
        out_dir: Path to destination directory to write output files
        save_json: If True will save a json file for each pdf containing extracted text
        save_text: If True will save a text file for each pdf containing extracted text
    """

    extractor = DocumentEmbeddedTextExtractor()

    for pdf_file in pdf_dir.glob("*.pdf"):
        data_out_path = out_dir / f"{Path(pdf_file).stem}.xml"

        # Extract embedded text in pdf file
        pdf_doc = extractor.extract(pdf_file, data_out_path)
        save_filename = Path(pdf_doc.filename).stem

        if save_json:
            out_json_filepath = out_dir / f"{save_filename}.json"
            pdf_doc.save_json(out_json_filepath)
        if save_text:
            out_text_filepath = out_dir / f"{save_filename}.txt"
            pdf_doc.save_text(out_text_filepath)


def configure_args():
    """Configure command line arguments for the cli"""

    parser = argparse.ArgumentParser(
        prog="pdf2text",
        description="Extracts text from a directory containing pdf documents.",
    )
    parser.add_argument(
        "pdf_dir",
        type=str,
        help="Path to directory containing pdf files to process",
    )
    parser.add_argument(
        "out_dir",
        type=str,
        help="Path to directory to store output files",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        default=False,
        help="Generates a json output file for each pdf document",
    )
    parser.add_argument(
        "--text",
        action="store_true",
        default=False,
        help="Generates a text output file for each pdf document",
    )

    args = parser.parse_args()

    if not (args.json or args.text):
        parser.error("At least one output format should be selected: --json / --text")

    return args


def cli():
    """Main entry point for the cli"""

    # Configure and parse command line arguments
    args = configure_args()

    pdf_dir = Path(args.pdf_dir)
    out_dir = Path(args.out_dir)

    # Check that the input/output directories exist and raise error if not
    if not pdf_dir.exists():
        raise DocumentTextExtractorException("Path to input pdf docuents is invalid")
    if not out_dir.exists():
        raise DocumentTextExtractorException("Output path is invalid")

    # Process the files in the directory
    process(pdf_dir, out_dir, args.json, args.text),


if __name__ == "__main__":
    cli()
