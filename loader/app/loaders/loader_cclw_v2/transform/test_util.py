from datetime import datetime
from typing import List

import pytest

from app.loaders.loader_cclw_v2.transform.util import extract_events
from app.model import Event


@pytest.mark.parametrize(
    "csv_event,expected",
    [
        [
            "02/10/2015|Law passed",
            [Event(date=datetime(2015, 10, 2), name="Law passed")],
        ],
        [
            "02/10/2015|Law passed||",
            [Event(date=datetime(2015, 10, 2), name="Law passed")],
        ],
        [
            "28/11/2020|Approved||;22/04/2021|Entry into force||",
            [
                Event(date=datetime(2020, 11, 28), name="Approved"),
                Event(date=datetime(2021, 4, 22), name="Entry into force"),
            ],
        ],
        [
            "25/12/2002|Law passed;25/12/2012|Last amended",
            [
                Event(date=datetime(2002, 12, 25), name="Law passed"),
                Event(date=datetime(2012, 12, 25), name="Last amended"),
            ],
        ],
        [
            "25/12/2002|Law passed;25/12/2012|Last amended||",
            [
                Event(date=datetime(2002, 12, 25), name="Law passed"),
                Event(date=datetime(2012, 12, 25), name="Last amended"),
            ],
        ],
    ],
)
def test_events_parser(csv_event: str, expected: List[Event]):
    assert extract_events(csv_event) == expected


# 16/04/2016|Law passed||
