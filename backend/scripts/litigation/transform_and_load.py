"""Simple script to verify the csv files in the data folder"""
import logging
from app.db.crud.litigation import ingest_case, transform_to_json
from app.db.session import SessionLocal

from scripts.litigation.utils import data_load

logging.basicConfig(level=logging.INFO, format="%(message)s")

if __name__ == "__main__":
    log = logging.getLogger(__file__)
    data = data_load()
    cases = data["cases"]
    parties = data["parties"]
    documents = data["documents"]
    events = data["events"]

    json_cases = transform_to_json(log, cases, events, documents, parties)
    log.info(f"Transformation completed on {len(json_cases)} cases.")

    db = SessionLocal()

    for cid, c in json_cases.items():
        case = ingest_case(db, log, c)

    log.info("--- DONE ---")
