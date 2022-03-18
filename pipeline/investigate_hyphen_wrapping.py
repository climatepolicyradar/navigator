import argparse
import json
import os
import re
from pathlib import Path

from tqdm import tqdm

from pipeline.extract.extract import AdobeAPIExtractor, DocumentEmbeddedTextExtractor

extractor = AdobeAPIExtractor(credentials_path="./pdfservices-credentials.json")
embedded_text_extractor = DocumentEmbeddedTextExtractor()
top_dir = "/home/stefan/Downloads/intermediate-small-temp/intermediate-small-temp"


def process_adobe(in_dir, out_dir_adobe, out_dir_embedded):
    # iterate through subdirectories and find json files. If found, apply data_to_document method and save to new directory
    fail_count = 0
    fail_list = []
    in_dir = str(in_dir)
    out_dir_adobe = str(out_dir_adobe)
    out_dir_embedded = str(out_dir_embedded)
    for dir in tqdm(os.listdir(in_dir)):
        if os.path.isdir(in_dir + "/" + dir):
            for file in os.listdir(in_dir + "/" + dir):
                if file.endswith(".json"):
                    try:
                        pdf_filename = f"{dir}.pdf"
                        doc = extractor.data_to_document(Path(in_dir + "/" + dir + "/" + file), pdf_filename)
                        doc.save_json(out_dir_adobe)
                        print('hi')
                    except:
                        fail_count += 1
                        print(fail_count)
                        fail_list.append(pdf_filename)
                        # count number of files that failed
                        try:
                            doc2 = embedded_text_extractor.extract(pdf_filepath=Path(pdf_filename), pdf_name=dir,
                                                                   data_output_dir=Path(out_dir_embedded),
                                                                   )
                            doc2.save_json(out_dir_embedded)
                        except:
                            pass
    with open('failurepdfs.txt', 'w') as f:
        for item in fail_list:
            f.write("%s\n" % item)


# # Find the types of cases where there is a hyphen at the end of a line.
# for file in os.listdir("/home/stefan/all_jsons"):
#     if file.endswith(".json"):
#         with open("/home/stefan/all_jsons/" + file) as json_file:
#             data = json.load(json_file)
#         for page in data['pages']:
#             for text_block in page['text_blocks']:
#                 # Only look at cases where the text block has multiple elements.
#                 if len(text_block['text']) > 1:
#                     for ix, li in enumerate(text_block['text']):
#                         # Check line ends with a word that ends with a hyphen followed by a space.
#                         if re.findall(r'\w+(-|–)\s$', li):
#                             st = '\n'.join(text_block['text'])
#                             print(f"{file}:", f"\n{st}\n")

if __name__ == "__main__":
    # create logger
    parser = argparse.ArgumentParser()
    parser.add_argument("in_dir", type=str, help="Path to the contents.json file.")
    parser.add_argument("out_dir_adobe", type=str, help="Path to the output directory.")
    parser.add_argument("out_dir_embedded", type=str, help="Path to the output directory.")
    args = parser.parse_args()
    in_dir = Path(args.in_dir)
    out_dir_adobe = Path(args.out_dir_adobe)
    out_dir_embedded = Path(args.out_dir_embedded)
    process_adobe(in_dir, out_dir_adobe, out_dir_embedded)
