from pathlib import Path

from app.extract import extract
from app.model import IngestData


def test_extract():
    data_dir = Path(__file__).cwd() / 'data'

    results: IngestData = extract(data_dir)
    assert len(results.policies_fe) == 2544
    assert len(results.policies) == 2568
    assert len(results.docs) == 2892
    assert len(results.targets) == 2458
