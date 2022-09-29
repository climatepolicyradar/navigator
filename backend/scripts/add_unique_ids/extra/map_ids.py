import json
import sys
from csv import DictReader
from pathlib import Path


def main(cclw_newer_path: Path, exported_document_table: Path):
    current_name_urls = {}
    with open(exported_document_table) as doct:
        csv_reader = DictReader(doct)
        for r in csv_reader:
            name = r["name"].strip()
            url = r["source_url"].strip()
            if (name, url) in current_name_urls:
                print(name)
            current_name_urls[(name, url)] = r["id"]

    doc_id_to_import = {}
    with open(cclw_newer_path) as cclw_newer:
        csv_reader = DictReader(cclw_newer)
        for r in csv_reader:
            name = r["Title"].strip()
            url = r["Documents"].split("|")[0].strip().replace("http://", "https://")
            action_id = int(float(r["Id"].strip()))
            doc_id = int(r["Document Id"].strip() or 0)
            category = r["Category"].strip().lower()
            if (name, url) in current_name_urls:
                doc_id_to_import[
                    current_name_urls[(name, url)]
                ] = f"CCLW:{category}:{action_id}:{doc_id}"
            else:
                print(f"Not found: {action_id}:{doc_id} - {name} {url}")

    with open("out.json", "w") as out:
        out.write(json.dumps(doc_id_to_import, indent=2))


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
