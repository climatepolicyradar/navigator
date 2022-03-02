"""CLI which extracts text from pdf documents in a directory.

Implements a cli which will extract the text contained in a set of pdf files in a directory.
"""

import argparse
from pathlib import Path
import tempfile
from collections import namedtuple
from typing import TextIO, Generator, Tuple


# def process(
#    pdf_dir: Path, data_dir: Path, out_dir: Path, save_json: bool, save_text: bool
# ):
from tqdm import tqdm

from navigator.core.aws import S3Client
from extract.extract import DocumentEmbeddedTextExtractor, AdobeAPIExtractor
from extract.exceptions import DocumentTextExtractorException


S3PathComponents = namedtuple(
    "S3PathComponents", ["bucket", "folders", "filename", "extension"]
)


def split_s3_path(s3_path: str, include_bucket=True, include_filename=True):
    """Return the components of an s3 path.

    Returns a path to an s3 bucket/folder or s3 object as a set of components
    """

    bucket = None
    folders = None

    s3_path = Path(s3_path)
    start_ix = 0
    end_ix = -1 if include_filename else len(s3_path.parts)
    if include_bucket:
        bucket = s3_path.parts[0]
        start_ix = 1

    folders = "/".join([folder for folder in s3_path.parts[start_ix:end_ix]])

    filename = s3_path.name if include_filename else None
    extension = s3_path.suffix if include_filename else None

    return S3PathComponents(bucket, folders, filename, extension)


def get_pdf_files(
    pdf_path: str, use_s3: bool = False
) -> Generator[Tuple[Path, str], None, None]:
    """Retrieve files from an s3 bucket/folder, or local directory

    Yields paths to pdf files to be processed. The files are either retrieved from a bucket/folder on S3,
    or from a local directory, depending on the use_s3 argument.

    Args:
        pdf_path (str): path to a directory on the local file system, or bucket/folder location on S3 in format:
            [bucket]/[folder]/[folder]/...
        use_s3 (bool): if True, will treat pdf_path as an s3 bucket path, otherwise as a path on the local file system.

    Yields:
        (Path) a path to each pdf document found in pdf_path.
    """

    if use_s3:
        s3_client = S3Client()
        s3_path_components = split_s3_path(
            pdf_path, include_bucket=True, include_filename=False
        )
        for s3_document in s3_client.list_files(s3_path_components.bucket):
            s3_document_path_components = split_s3_path(
                s3_document.key, include_bucket=False, include_filename=True
            )
            if (
                s3_path_components.folders == s3_document_path_components.folders
                and s3_document_path_components.extension.upper() == ".PDF"
            ):
                object_response = s3_client.download_file(s3_document)

                temp_f = tempfile.NamedTemporaryFile(prefix="navigator_", suffix=".pdf")
                temp_f.write(object_response.read())

                yield Path(temp_f.name), s3_document_path_components.filename

                # Close the temporary file after it has been processed - this will ensure it is deleted
                temp_f.close()
    else:
        for pdf_file in Path(pdf_path).glob("*.pdf"):
            yield pdf_file, pdf_file.name


def upload_extract_files(
    out_path: str, save_filename: str, out_json_file: TextIO, out_text_file: TextIO
):
    """Upload the extracted json and text files to an s3 bucket.

    Uploads the json and text extract files to an s3 bucket. save_filename is used as the
    root filename for these files to make sure that they have the same name as the file processed.
    For example, if extracting `document.pdf`, the json and text extract files will be called
    `document.json` and `document.txt` respectively.

    Args:
        out_path (str): path to bucket and folders to upload files to in format
            [bucket]/[folder]/[folder]/...
        save_filename (str): name of file being processed
        out_json_file (TextIO): file like object for temporary output json file
        out_text_file (TextIO): file like object for temporary output text file
    """

    out_path_components = split_s3_path(
        out_path, include_bucket=True, include_filename=False
    )

    s3_client = S3Client()

    # Create keys for uploaded files
    s3_json_key = (
        f"{out_path_components.folders}/{save_filename}.json"
        if out_path_components.folders
        else f"{save_filename}.json"
    )
    s3_text_key = (
        f"{out_path_components.folders}/{save_filename}.txt"
        if out_path_components.folders
        else f"{save_filename}.txt"
    )

    # Upload the files
    s3_client.upload_file(
        out_json_file.name, out_path_components.bucket, key=s3_json_key
    )
    s3_client.upload_file(
        out_text_file.name, out_path_components.bucket, key=s3_text_key
    )

    # Close the temp files to ensure they're deleted afterwards
    out_json_file.close()
    out_text_file.close()


def process(pdf_path: str, data_dir: Path, out_path: str, use_s3: bool = False):
    """Extracts text from text in a directory containing pdf files.

    Iterates through files with a .pdf extension in a given directory or s3 bucket/folder,
    and processes those files to extract text. Produces a .json and/or
    .txt file containing extracted text and associated positional data.

    Args:
        pdf_path (str): Either a path to a local directory or an s3 bucket/folders containing input pdf files
        data_dir (Path): Path to local directory to write output intermediate extract files
        out_path (str): Either a path to a local directory or an bucket/folders to upload files to in format
        use_s3 (bool): if True, will treat pdf_path as an s3 bucket path, otherwise as a path on the local file system.
    """

    adobe_extractor = AdobeAPIExtractor(
        credentials_path="./pdfservices-credentials.json"
    )
    embedded_extractor = DocumentEmbeddedTextExtractor()

    pdf_file_iterator = tqdm(
        get_pdf_files(pdf_path, use_s3), desc="Documents processed", unit="file"
    )
    for pdf_file, source_pdf_filename in pdf_file_iterator:
        pdf_file_iterator.set_description(desc=f"Processing {source_pdf_filename}")

        pdf_name = Path(source_pdf_filename).stem

        try:
            pdf_doc = adobe_extractor.extract(
                pdf_filepath=pdf_file,
                pdf_name=pdf_name,
                data_output_dir=data_dir,
                output_folder_pdf_splits="/temp",
            )
        except Exception as e:
            print(
                f"Adobe extractor failed with error {e}. Falling back to embedded text extractor."
            )
            pdf_doc = embedded_extractor.extract(
                pdf_filepath=pdf_file, pdf_name=pdf_name, data_output_dir=data_dir
            )

        save_filename = Path(source_pdf_filename).stem

        if use_s3:
            out_json_file = tempfile.NamedTemporaryFile(
                prefix="navigator_", suffix=".json"
            )
            out_json_filepath = out_json_file.name
            out_text_file = tempfile.NamedTemporaryFile(
                prefix="navigator_", suffix=".txt"
            )
            out_text_filepath = out_text_file.name
        else:
            out_json_filepath = Path(out_path) / f"{save_filename}.json"
            out_text_filepath = Path(out_path) / f"{save_filename}.txt"

        # Save the json and text for the document
        pdf_doc.save_json(out_json_filepath)
        pdf_doc.save_text(out_text_filepath)

        # If we're using s3, upload the document to the given bucket/folder
        if use_s3:
            upload_extract_files(out_path, save_filename, out_json_file, out_text_file)


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
        "data_dir",
        type=str,
        help="Path to directory to store intermediate files",
    )
    parser.add_argument(
        "out_path",
        type=str,
        help="Path to directory or name of s3 bucket and subfolders to store output files",
    )
    parser.add_argument(
        "--s3",
        action="store_true",
        default=False,
        help="Retrieve and write files to s3 buckets",
    )

    args = parser.parse_args()

    return args


def cli():
    """Main entry point for the cli"""

    # Configure and parse command line arguments
    args = configure_args()

    pdf_path = Path(args.pdf_path)
    data_dir = Path(args.data_dir)
    out_path = Path(args.out_path)

    # Check that the input/output directories exist and raise error if not
    if not pdf_path.exists() and not args.s3:
        raise DocumentTextExtractorException("Path to input pdf docuents is invalid")
    if not data_dir.exists():
        raise DocumentTextExtractorException("Data path is invalid")
    if not out_path.exists() and not args.s3:
        raise DocumentTextExtractorException("Output path is invalid")

    # Process the files in the directory
    process(pdf_path, data_dir, out_path, args.s3),


if __name__ == "__main__":
    cli()
