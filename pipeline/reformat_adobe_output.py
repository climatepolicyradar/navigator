import argparse
from pathlib import Path

from processor.postprocessor import AdobeDocumentPostProcessor


def process(in_path, out_path):
    """
    Process a document into a better format for downstream tasks.

    Args:
        in_path: Directory with Adobe output files to process further.
        out_path: Directory to write post-processed files to.

    Returns:

    """
    # TODO: Add s3 support.
    postprocessor = AdobeDocumentPostProcessor()
    for file in in_path.iterdir():
        if file.suffix == ".json":
            doc = postprocessor.postprocess(file)
            doc.save_json(out_path / file.stem)


if __name__ == "__main__":
    # create logger
    parser = argparse.ArgumentParser()
    parser.add_argument("in_path", type=str, help="Path to the contents.json file.")
    parser.add_argument("out_path", type=str, help="Path to the output directory.")
    args = parser.parse_args()
    in_dir = Path(args.in_path)
    out_dir = Path(args.out_path)
    process(in_dir, out_dir)
