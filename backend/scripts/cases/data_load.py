import csv
from config import CSV_PARTIES, CSV_DOCUMENTS, CSV_CASES, CSV_EVENTS


def _data_load(filename: str, id_key: str) -> dict[str, dict]:
    """Reads the filename as csv returning a Dict indexed on the id_key"""
    objects = {}
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = row[id_key]
            objects[key] = row

    return objects


def data_load() -> Dict[str, Dict]:
    return {
        "cases": _data_load(CSV_CASES, "Case ID"),
        "parties": _data_load(CSV_PARTIES, "Party ID"),
        "documents": _data_load(CSV_DOCUMENTS, "Document ID"),
        "events": _data_load(CSV_EVENTS, "Event ID"),
    }
