"""Simple script to verify the csv files in the data folder"""
from typing import Any, Dict, Set
from app.db.models.litiguation import (
    LitParty,
    LitPartyType,
)
from sqlalchemy.orm import Session
from data_load import data_load

from app.db.models import Case
from app.db.session import SessionLocal


def load(
    db: Session,
    cases: Dict[str, Dict],
    events: Dict[str, Dict],
    documents: Dict[str, Dict],
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

        # TODO: Create any Events
        # TODO: Create any Documents
        # TODO: Create any Bodies

        # TODO: Find Sector
        # TODO: Find Geography


def add_parties(
    db: Session,
    parties: Dict[str, Dict],
):
    for id, p in parties.items():
        print(p["Party name"])
        print("-" * 20)
        # pprint(p)
        new_party = LitParty(
            name=p["Party name"],
            party_type=LitPartyType(p["Party type"]),
            side_type=p["Side type"],
        )
        db.add(new_party)
    db.commit()


if __name__ == "__main__":
    db = SessionLocal()

    data = data_load()
    cases = data["cases"]
    parties = data["parties"]
    documents = data["documents"]
    events = data["events"]

    add_parties(db, parties)
    # load(cases, events, documents, parties)
    print("--- DONE ---")
