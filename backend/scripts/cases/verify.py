"""Simple script to verify the csv files in the data folder"""
from typing import Any, Dict, Set

from data_load import data_load


def validate_refs(
    entities: Dict[str, Any], entity_name: str, entity_key: str, primary_set: Set[str]
):
    print()
    print(f"Checking {entity_name}:")
    referenced_cases = set([e[entity_key] for e in entities.values()])
    unknown_cases = referenced_cases - primary_set
    orphaned_cases = primary_set - referenced_cases
    print(f"  Found {len(referenced_cases)} referenced {entity_key}s.")
    print(f"  Got {len(unknown_cases)} unknown referenced {entity_key}s.")
    if len(unknown_cases) > 0:
        print(unknown_cases)
    print(f"  Leaving {len(orphaned_cases)} {entity_key}(s) orphaned of {entity_name}.")
    if len(orphaned_cases) > 0:
        print(orphaned_cases)


def verify(
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
    print(f"Found {len(cases)} Cases, {len(all_cases)} unique.")

    validate_refs(events, "Events", "Case ID", all_cases)
    validate_refs(parties, "Parties", "Case ID", all_cases)
    validate_refs(documents, "Documents", "Case ID", all_cases)
    validate_refs(documents, "Documents", "Event ID", set(events))


if __name__ == "__main__":
    data = data_load()
    cases = data["cases"]
    parties = data["parties"]
    documents = data["documents"]
    events = data["events"]

    verify(cases, events, documents, parties)
    print("--- DONE ---")
