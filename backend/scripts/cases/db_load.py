"""Simple script to verify the csv files in the data folder"""
from typing import Any, Dict, Set

from data_load import data_load

from app.db.models import Case
from app.db.session import SessionLocal


def load(
    cases: Dict[str, Dict],
    events: Dict[str, Dict],
    documents: Dict[str, Dict],
    parties: Dict[str, Dict],
):
    """Checks the relationships

    Event:      Case ID
    Parties     Case ID
    Document:   Case ID     Event ID
    """

    all_cases = set(cases.keys())
    for case in all_cases:
        print(f"Importing Case {case}")
        case_data = cases[case]
        
        # TODO: Create any Parties
        # TODO: Create any Events
        # TODO: Create any Documents
        # TODO: Create any Bodies
        
        # TODO: Find Sector
        # TODO: Find Geography
        



if __name__ == "__main__":
    db = SessionLocal()

    data = data_load()
    cases = data["cases"]
    parties = data["parties"]
    documents = data["documents"]
    events = data["events"]

    load(cases, events, documents, parties)
    print("--- DONE ---")
