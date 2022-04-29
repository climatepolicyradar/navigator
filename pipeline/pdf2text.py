"""CLI which extracts text from pdf documents in a directory.

Implements a cli which will extract the text contained in a set of pdf files in a directory.
"""

import argparse
from pathlib import Path
import tempfile
from collections import namedtuple
from typing import Generator, Tuple, Optional
from multiprocessing import Pool, cpu_count
from uuid import uuid4

from tqdm import tqdm

from navigator.core.aws import S3Client
from navigator.core.log import get_logger
from extract.extract import DocumentEmbeddedTextExtractor, AdobeAPIExtractor
from extract.exceptions import DocumentTextExtractorException

logger = get_logger(__name__)

S3PathComponents = namedtuple(
    "S3PathComponents", ["bucket", "folders", "filename", "extension"]
)


def split_s3_path(s3_path: Path, include_bucket=True, include_filename=True):
    """Return the components of an s3 path.

    Returns a path to an s3 bucket/folder or s3 object as a set of components
    """
    bucket = None
    folders = None

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
    pdf_path: Path, use_s3: bool = False
) -> Generator[Tuple[Path, str], None, None]:
    """Retrieve files from an S3 bucket/folder, or local directory.

    Yields paths to pdf files to be processed. The files are either retrieved from a bucket/folder on S3,
    or from a local directory, depending on the use_s3 argument.

    Args:
        pdf_path (str): path to a directory on the local file system, or bucket/folder location on S3 in format:
            [bucket]/[folder]/[folder]/...
        use_s3 (bool): if True, will treat pdf_path as an s3 bucket path, otherwise as a path on the local file system.

    Yields:
        Tuple[Path, str]: path and filename of each pdf document found in the directory, S3 bucket, or S3 folder.
    """
    if use_s3:
        s3_client = S3Client()
        s3_path_components = split_s3_path(
            pdf_path, include_bucket=True, include_filename=False
        )
        s3_documents = s3_client.list_files(s3_path_components.bucket)
        if s3_documents is False:
            raise RuntimeError(
                f"Failed to list s3 bucket '{s3_path_components.bucket}'"
            )
        if s3_documents is True:
            raise RuntimeError("Unexpected response from s3 bucket listing")
        for s3_document in s3_documents:
            s3_document_path_components = split_s3_path(
                Path(s3_document.key), include_bucket=False, include_filename=True
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
    out_path: Path, save_filename: str, out_json_filepath: Path, out_text_filepath: Path
):
    """Upload the extracted json and text files to an s3 bucket.

    Uploads the json and text extract files to an s3 bucket. save_filename is used as the
    root filename for these files to make sure that they have the same name as the file processed.
    For example, if extracting `document.pdf`, the json and text extract files will be called
    `document.json` and `document.txt` respectively.

    Args:
        out_path (Path): path to bucket and folders to upload files to in format
            [bucket]/[folder]/[folder]/...
        save_filename (str): name of file being processed
        out_json_filepath (Path): path for temporary output json file
        out_text_filepath (Path): path for temporary output text file
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
        out_json_filepath.name, out_path_components.bucket, key=s3_json_key
    )
    s3_client.upload_file(
        out_text_filepath.name, out_path_components.bucket, key=s3_text_key
    )


class PDFProcessor:
    """Process PDF files using the Adobe Extractor, falling back to the embedded text extractor when it fails."""

    def __init__(
        self,
        data_dir: Path,
        out_path: Path,
        use_s3: bool,
        adobe_extractor: AdobeAPIExtractor,
        embedded_extractor: DocumentEmbeddedTextExtractor,
    ):
        """Initalise PDFProcessor.

        Args:
            data_dir (Path): directory to store intermediate results in
            out_path (str): directory to store output files (.json and .txt) in
            use_s3 (bool): whether input and output directories are s3 buckets or folders
            adobe_extractor (AdobeAPIExtractor): instance of Adobe API extractor
            embedded_extractor (DocumentEmbeddedTextExtractor): instance of embedded text extractor
        """
        self.data_dir = data_dir
        self.out_path = out_path
        self.use_s3 = use_s3
        self.adobe_extractor = adobe_extractor
        self.embedded_extractor = embedded_extractor

    def process_file(self, pdf_filepath: Path, pdf_filename: str):
        """Process a single file. Produces a .json and .txt file containing extracted text and associated positional data.

        Args:
            pdf_filepath (Path): path to PDF file.
            pdf_filename (str): name of PDF file.
        """

        try:
            pdf_doc = self.adobe_extractor.extract(
                pdf_filepath=pdf_filepath,
                pdf_name=pdf_filename,
                data_output_dir=self.data_dir,
            )
        except Exception as e:
            print(
                f"Adobe extractor failed with error {e} for {pdf_filename}. Falling back to embedded text extractor."
            )

            try:
                pdf_doc = self.embedded_extractor.extract(
                    pdf_filepath=pdf_filepath,
                    pdf_name=pdf_filename,
                    data_output_dir=self.data_dir,
                )
            except Exception as e:
                print(
                    f"Embedded extractor also failed with error {e} for {pdf_filename}."
                )

        save_filename = Path(pdf_filename).stem

        with tempfile.TemporaryDirectory() as temp_dir:
            if self.use_s3:
                _u = str(uuid4())
                out_json_filepath = Path(temp_dir) / f"navigator_{_u}.json"
                out_text_filepath = Path(temp_dir) / f"navigator_{_u}.txt"
            else:
                out_json_filepath = Path(self.out_path) / f"{save_filename}.json"
                out_text_filepath = Path(self.out_path) / f"{save_filename}.txt"

            # Save the json and text for the document
            pdf_doc.save_json(out_json_filepath)
            pdf_doc.save_text(out_text_filepath)

            # If we're using s3, upload the document to the given bucket/folder
            if self.use_s3:
                upload_extract_files(
                    self.out_path,
                    save_filename,
                    out_json_filepath,
                    out_text_filepath,
                )

    def _process_file_star(self, args):
        """Enable use of multiprocessing.imap rather than multiprocessing.starmap, meaning tqdm can be used to create a progress bar."""
        return self.process_file(*args)

    def process(self, pdf_path: Path, n_process: Optional[int] = None):
        """Extract text from text in a directory containing pdf files.

        Iterate through files with a .pdf extension in a given directory or s3 bucket/folder,
        and processes those files to extract text. Produces a .json and/or
        .txt file containing extracted text and associated positional data.

        Args:
            pdf_path (str): Either a path to a local directory or an s3 bucket/folder containing input pdf files.
            If an S3 bucket or folder, the `use_s3` argument for the class must be set to True.
            n_process (int, optional): number of process to parallelise PDF processing over. Defaults to the
            CPU count of the host machine.
        """
        pdf_file_iterator = get_pdf_files(pdf_path, self.use_s3)

        if n_process is None:
            n_process = cpu_count()

        if n_process == 1:
            logger.info("Processing PDFs using single process")
            for filepath, filename in tqdm(pdf_file_iterator):
                self.process_file(filepath, filename)
        else:
            logger.info(f"Processing PDFs using {n_process} processes")
            with Pool(processes=n_process) as pool:
                _ = list(
                    tqdm(
                        pool.imap_unordered(self._process_file_star, pdf_file_iterator)
                    )
                )


def configure_args():
    """Configure command line arguments for the cli."""
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
    parser.add_argument(
        "--single_process",
        action="store_true",
        default=False,
        help="Whether to run processing on a single process. Otherwise runs on two processes.",
    )

    args = parser.parse_args()

    return args


def cli():
    """Run the cli."""
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

    adobe_extractor = AdobeAPIExtractor(
        credentials_path="./pdfservices-credentials.json"
    )
    embedded_extractor = DocumentEmbeddedTextExtractor()

    # Process the files in the directory
    processor = PDFProcessor(
        data_dir=data_dir,
        out_path=out_path,
        use_s3=args.s3,
        adobe_extractor=adobe_extractor,
        embedded_extractor=embedded_extractor,
    )
    if args.single_process:
        processor.process(pdf_path, n_process=1)
    else:
        # Two processes has been selected experimentally as the max number of processes
        # possible whilst avoiding queuing and timeout errors.
        processor.process(pdf_path, n_process=2)


if __name__ == "__main__":
    cli()
