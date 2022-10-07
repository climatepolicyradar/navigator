import logging
from typing import Any, Mapping, Set
from app.db.models.litiguation import LitParty, LitPartyType, LitSideType
from app.db.models.case import (
    Case,
    CaseStatus,
    ClimateAlignmentClass,
    StrategicAlignmentClass,
    UNFCCCPillars,
)
from app.db.models.geography import Geography
from app.db.models.document import Sector

from sqlalchemy.orm import Session


def _to_bool(value: str) -> bool:
    return value.upper() == "YES" or value.upper() == "TRUE"


def _validate_refs(
    log: logging.Logger,
    entities: Mapping[str, Any],
    entity_name: str,
    entity_key: str,
    primary_set: Set[str],
):
    log.info(f"Checking {entity_name}:")
    referenced_cases = set([e[entity_key] for e in entities.values()])
    unknown_cases = referenced_cases - primary_set
    orphaned_cases = primary_set - referenced_cases

    log.info(f"  Found {len(referenced_cases)} referenced {entity_key}s.")

    log.info(f"  Got {len(unknown_cases)} unknown referenced {entity_key}s.")
    if len(unknown_cases) > 0:
        log.info(unknown_cases)

    log.info(
        f"  Leaving {len(orphaned_cases)} {entity_key}(s) orphaned of {entity_name}."
    )
    if len(orphaned_cases) > 0:
        log.info(orphaned_cases)


def verify(
    log: logging.Logger,
    cases: Mapping[str, Mapping],
    events: Mapping[str, Mapping],
    documents: Mapping[str, Mapping],
    parties: Mapping[str, Mapping],
):
    """Checks the relationships

    Event:      Case ID
    Parties     Case ID
    Document:   Case ID     Event ID
    """

    all_cases = set(cases.keys())
    log.info(f"Found {len(cases)} Cases, {len(all_cases)} unique.")

    _validate_refs(log, events, "Events", "Case ID", all_cases)
    _validate_refs(log, parties, "Parties", "Case ID", all_cases)
    _validate_refs(log, documents, "Documents", "Case ID", all_cases)
    _validate_refs(log, documents, "Documents", "Event ID", set(events))


def transform_to_json(
    log: logging.Logger,
    cases: Mapping[str, Mapping],
    events: Mapping[str, Mapping],
    documents: Mapping[str, Mapping],
    parties: Mapping[str, Mapping],
):
    json_cases = {}

    # Initalise attributes
    for idx, cid in enumerate(cases):
        json_cases[cid] = dict(cases[cid])
        json_cases[cid]["events"] = []
        json_cases[cid]["documents"] = []
        json_cases[cid][LitSideType.FILING_PARTY.value] = []
        json_cases[cid][LitSideType.RESPONDING_PARTY.value] = []
        json_cases[cid][LitSideType.INTERVENOR.value] = []

    # Add events
    for _, e in events.items():
        cid = e["Case ID"]
        if cid not in json_cases.keys():
            msg = f"Event {e} references a non-existent case {cid}"
            log.error(msg)
            # raise ValueError(f"Event {e} references a non-existent case {cid}")  - uncomment to abort instead
            continue
        json_cases[cid]["events"].append(e)

    # Add parties
    for _, p in parties.items():
        cid = p["Case ID"]
        if cid not in json_cases.keys():
            msg = f"Party {p} references a non-existent case {cid}"
            log.error(msg)
            # raise ValueError(msg) - uncomment to abort instead
            continue

        side = p["Side type"]
        if side == LitSideType.FILING_PARTY:
            json_cases[cid][LitSideType.FILING_PARTY.value].append(p)
        elif side == LitSideType.RESPONDING_PARTY:
            json_cases[cid][LitSideType.RESPONDING_PARTY.value].append(p)
        elif side == LitSideType.INTERVENOR:
            json_cases[cid][LitSideType.INTERVENOR.value].append(p)
        else:
            raise ValueError(f"Party {p} has unknown side {side}")

    # Add documents
    for _, d in documents.items():
        cid = d["Case ID"]
        if cid not in json_cases.keys():
            msg = f"Dopcument {d} references a non-existent case {cid}"
            log.error(msg)
            # raise ValueError(msg) - uncomment to abort instead
            continue
        json_cases[cid]["documents"].append(d)

    return json_cases


def ingest_party(db: Session, csv_row: Mapping[str, str]) -> LitParty:
    """Will attempt to find or create the Party represented by csv_row."""

    name = (csv_row["Party name"],)
    party_type = LitPartyType(csv_row["Party type"])
    side_type = LitSideType(csv_row["Side type"])

    found = (
        db.query(LitParty)
        .filter(LitParty.name == name)
        .filter(LitParty.party_type == party_type)
        .filter(LitParty.side_type == side_type)
        .first()
    )

    if found is not None:
        return found

    new_party = LitParty(
        name=name,
        party_type=party_type,
        side_type=side_type,
    )

    db.add(new_party)
    db.commit()
    return new_party


def ingest_case(db: Session, log: logging.Logger, json_case: Mapping[str, Any]) -> Case:
    """Will attempt to find or create a Case represented by json_case."""

    found = db.query(Case).filter(Case.name == json_case["Case name"]).first()
    if found:
        return found

    # Validate geography
    geography_id = (
        db.query(Geography.id)
        .filter(Geography.value == json_case["Country ISO"])
        .scalar()
    )
    if geography_id is None:
        log.error(
            f"Geography '{json_case['Country ISO']}' missing for case '{json_case['Case name']}' ({json_case['Case ID']}) was invalid: "
        )

    # Validate sectors
    for s in json_case["Sector"].split(";"):
        sector_id = db.query(Sector.id).filter(Sector.name == s).scalar()
        if sector_id is None:
            log.error(
                f"Sector '{s}' missing for case '{json_case['Case name']}' ({json_case['Case ID']})"
            )

    # Validate sources
    climate_class = json_case["Climate alignment classification"]
    strategic_class = json_case["Strategic case type classification"]

    case = Case(
        name=json_case["Case name"],
        ext_id="CCLW:" + json_case["Case ID"],
        year=json_case["Year of filing"],
        status=CaseStatus.from_value(json_case["Current status"]),
        outcome=json_case["Assessment of outcome"],
        objective=json_case["Core objective"],
        pillars=UNFCCCPillars.from_value(
            json_case["UNFCCC pillars"].split(";")[0]
        ),  # Schema change?
        summary=json_case["Summary"],
        reference=json_case["Citation/reference number"],
        strategic=_to_bool(json_case["Classified as strategic case"]),
        climate_class=ClimateAlignmentClass.from_value(climate_class),
        strategic_class=StrategicAlignmentClass.from_value(
            strategic_class.split(",")[0]
        ),
        case_class=json_case["Case grounds classification"],
        source=json_case["Data source"],  # semicolon sep
        keywords=json_case["Keywords"].split(","),
    )
    """_summary_

     'Sector'
     'Connected internal laws'
     'Connected external laws' - bar sep
     'Keywords' - comma sep
     ''
     'events'
     'documents'

     'Filing party'
     'Responding party'
     'Intervenor'

     TODO:
     - Add keywords
     - Add case_link_source
     - Add case_link_sector
    """

    db.add(case)
    db.commit()
    return case
