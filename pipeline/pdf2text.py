"""Extracts text from a batch of pdf documents
"""

import argparse
from pathlib import Path

from extract.extract import DocumentEmbeddedTextExtractor
from extract.exceptions import DocumentTextExtractorException


def process_document():
    pass


def process_batch(pdf_url: Path, out_url: Path, save_json: bool, save_text: bool):
    extractor = DocumentEmbeddedTextExtractor()

    for pdf_file in pdf_url.glob("*.pdf"):
        # Extract embedded text in pdf file
        pdf_doc = extractor.extract(pdf_file)

        save_filename = Path(pdf_doc.filename).stem
        if save_json:
            out_json_filepath = out_url / f"{save_filename}.json"
            pdf_doc.save_json(out_json_filepath)
        if save_text:
            out_text_filepath = out_url / f"{save_filename}.txt"
            pdf_doc.save_text(out_text_filepath)


def configure_args():
    # TODO Add extractor type -> embedded, ocr and pass in appropriate class

    parser = argparse.ArgumentParser(
        prog="pdf2text",
        description="Extracts text from a directory or s3 bucket containing pdf documents.",
    )
    parser.add_argument(
        "pdf_url",
        type=str,
        help="Path to directory or url to s3 bucket containing pdf files",
    )
    parser.add_argument(
        "out_url",
        type=str,
        help="Path to directory or url to s3 bucket to store extracted text",
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
    args = configure_args()

    pdf_url = Path(args.pdf_url)
    out_url = Path(args.out_url)

    if not pdf_url.exists():
        raise DocumentTextExtractorException("Path to input pdf docuents is invalid")
    if not out_url.exists():
        raise DocumentTextExtractorException("Output path is invalid")

    process_batch(pdf_url, out_url, args.json, args.text),


if __name__ == "__main__":
    cli()
