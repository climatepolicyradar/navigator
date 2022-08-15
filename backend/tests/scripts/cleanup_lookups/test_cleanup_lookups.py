from unittest.mock import patch

from app.db.models.document import Keyword
from scripts.cleanup_lookups.cleanup_lookups import (
    get_clean_keyword_map,
    update_keyword_links,
)


TEST_KEYWORD_MAP = {
    "E Vs": "EVs",
    "Ev": "EVs",
    "EV": "EVs",
    "Buses": "Buses",
    "coal": "Coal",
    "Coal": "Coal",
}


@patch("scripts.cleanup_lookups.cleanup_lookups.load_keyword_map")
def test_clean_keyword_map(mock_load_keyword_map, test_db):
    # Add some bad keyword data
    mock_load_keyword_map.return_value = TEST_KEYWORD_MAP

    # Add two identified variations of EV, but not the one we actually want
    # The value "EVs" should be created
    ev1 = Keyword(name="E Vs", description="d")
    ev2 = Keyword(name="Ev", description="d")
    ev3 = Keyword(name="EV", description="d")
    test_db.add(ev1)
    test_db.add(ev2)
    test_db.add(ev3)

    # Add one correct Keyword
    bus = Keyword(name="Buses", description="d")
    test_db.add(bus)

    # Add one keyword with identified variants including the one we want
    coal1 = Keyword(name="coal", description="d")
    coal2 = Keyword(name="Coal", description="d")
    test_db.add(coal1)
    test_db.add(coal2)

    test_db.commit()

    actual_keyword_map = get_clean_keyword_map(test_db)

    # This validates that entries are created when needed
    final_ev = test_db.query(Keyword).filter(Keyword.name == "EVs").first()
    expected_keyword_map = {
        ev1.id: final_ev.id,
        ev2.id: final_ev.id,
        ev3.id: final_ev.id,
        bus.id: bus.id,
        coal1.id: coal2.id,
        coal2.id: coal2.id,
    }

    assert actual_keyword_map == expected_keyword_map

    # Now check that the right keywords are removed
    update_keyword_links(test_db, expected_keyword_map)  # type: ignore
    expected_remaining_keyword_ids = {
        k for k, v in expected_keyword_map.items() if k == v
    } | {final_ev.id}

    test_db.commit()

    for kw in test_db.query(Keyword).all():
        assert kw.id in expected_remaining_keyword_ids
