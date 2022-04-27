import argparse
from pathlib import Path

from extract.document import Document
from processor.postprocessor import (
    AdobeListGroupingPostProcessor,
    AdobeTextStylingPostProcessor,
    HyphenationPostProcessor,
)


def process(in_path, out_path):
    """Process a document into a better format for downstream tasks.

    Args:
        in_path: Directory with Adobe output files to process further.
        out_path: Directory to write post-processed files to.
    """
    # TODO: Add s3 support.
    text_styling_processor = AdobeTextStylingPostProcessor()
    hyphenation_processor = HyphenationPostProcessor()
    postprocessor = AdobeListGroupingPostProcessor()
    for file in in_path.iterdir():
        if file.suffix == ".json":
            doc = Document.from_json(file)
            doc = hyphenation_processor.process(doc)
            doc = text_styling_processor.process(
                doc,
            )
            doc = postprocessor.process(doc, f"{file.stem}")
            # Write to json file.
            doc.save_json(out_path / f"{file.stem}.json")


if __name__ == "__main__":
    # create logger
    parser = argparse.ArgumentParser()
    parser.add_argument("in_path", type=str, help="Path to the contents.json file.")
    parser.add_argument("out_path", type=str, help="Path to the output directory.")
    args = parser.parse_args()
    in_dir = Path(args.in_path)
    out_dir = Path(args.out_path)
    process(in_dir, out_dir)
