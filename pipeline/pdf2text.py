"""CLI which extracts text from pdf documents in a directory.

Implements a cli which will extract the text contained in a set of pdf files in a directory.
"""

import argparse
from pathlib import Path
import tempfile

from navigator.core.aws import S3Client, S3Document
from extract.extract import DocumentEmbeddedTextExtractor
from extract.exceptions import DocumentTextExtractorException


def split_s3_path(s3_bucket_path: str):
    """"""
    s3_bucket_path = Path(s3_bucket_path)
    bucket = s3_bucket_path.parts[0]
    folders = "/".join([folder for folder in s3_bucket_path.parts[1:]])

    return bucket, folders


def get_s3_file_path(s3_document: S3Document):
    s3_document_path = Path(s3_document.key)
    folders = "/".join([folder for folder in s3_document_path.parts[:-1]])

    return s3_document_path, folders


def get_files(pdf_path: str, use_s3: bool = False):
    """Retrieve files from an s3 bucket and folder, or local directory

    s3: [bucket]/[folder]/[folder]
    """
    if use_s3:
        s3_client = S3Client()
        bucket, folders = split_s3_path(pdf_path)
        for s3_document in s3_client.list_files(bucket):
            s3_document_path, s3_document_folders = get_s3_file_path(s3_document)
            if s3_document_folders == folders and s3_document_path.suffix == ".pdf":
                object_response = s3_client.download_file(s3_document)

                temp_f = tempfile.NamedTemporaryFile(prefix="navigator_", suffix=".pdf")
                temp_f.write(object_response.read())

                yield Path(temp_f.name)
    else:
        for pdf_file in Path(pdf_path).glob("*.pdf"):
            yield pdf_file


def process(
    pdf_path: str, out_dir: Path, save_json: bool, save_text: bool, use_s3: bool = False
):
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

    for pdf_file in get_files(pdf_path, use_s3):
        print(f"Processing {pdf_file}...")

        # Extract embedded text in pdf file
        pdf_doc = extractor.extract(pdf_file)

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
        "pdf_path",
        type=str,
        help="Path to directory or name of s3 bucket and subfolders containing pdf files to process",
    )
    parser.add_argument(
        "out_dir",
        type=str,
        help="Path to directory or name of s3 bucket and subfolders to store output files",
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
    parser.add_argument(
        "--s3",
        action="store_true",
        default=False,
        help="Retrieve and write files to s3 buckets",
    )

    args = parser.parse_args()

    if not (args.json or args.text):
        parser.error("At least one output format should be selected: --json / --text")

    return args


def cli():
    """Main entry point for the cli"""

    # Configure and parse command line arguments
    args = configure_args()

    pdf_path = Path(args.pdf_path)
    out_dir = Path(args.out_dir)

    # Check that the input/output directories exist and raise error if not
    if not pdf_path.exists() and not args.s3:
        raise DocumentTextExtractorException("Path to input pdf docuents is invalid")
    if not out_dir.exists():
        raise DocumentTextExtractorException("Output path is invalid")

    # Process the files in the directory
    process(pdf_path, out_dir, args.json, args.text, args.s3),


if __name__ == "__main__":
    cli()
