"""Simple script to verify the csv files in the data folder"""

import logging
from app.db.crud.litigation import ingest_party
from scripts.litigation.utils import data_load

from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO, format="%(message)s")

if __name__ == "__main__":
    log = logging.getLogger(__file__)

    db = SessionLocal()

    data = data_load()
    cases = data["cases"]
    parties = data["parties"]
    documents = data["documents"]
    events = data["events"]

    for id, p in parties.items():
        new_party = ingest_party(db, p)

    log.info("--- DONE ---")
