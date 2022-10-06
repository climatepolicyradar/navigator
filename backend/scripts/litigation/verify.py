"""Simple script to verify the csv files in the data folder"""
import logging
from app.db.crud.litigation import verify

from scripts.litigation.utils import data_load

logging.basicConfig(level=logging.INFO, format="%(message)s")

if __name__ == "__main__":
    log = logging.getLogger(__file__)
    data = data_load()
    cases = data["cases"]
    parties = data["parties"]
    documents = data["documents"]
    events = data["events"]

    verify(log, cases, events, documents, parties)
    log.info("Verification complete.")
