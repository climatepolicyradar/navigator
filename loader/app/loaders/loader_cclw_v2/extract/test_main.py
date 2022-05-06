from pathlib import Path

from app.loaders.loader_cclw_v2.extract.main import extract


def test_extract():
    csv_path = (
        Path(__file__).parent.resolve()
        / ".."
        / ".."
        / ".."
        / ".."
        / "data"
        / "cclw_new_format_20220503.csv"
    )

    policies_fe = extract(csv_path)
    assert len(policies_fe) == 1313
