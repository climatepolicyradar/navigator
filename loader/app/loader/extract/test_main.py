from pathlib import Path

from app.loader.extract import extract


def test_extract():
    data_dir = Path(__file__).parent.resolve() / ".." / ".." / "data"

    policies_fe = extract(data_dir)
    assert len(policies_fe) == 2544
