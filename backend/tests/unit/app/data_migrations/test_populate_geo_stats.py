import pytest
from app.data_migrations.populate_geo_statistics import to_float


@pytest.mark.unit
@pytest.mark.parametrize("param", ["", "-", "chicken", "£$%"])
def test_to_float_bad_data(param):
    assert to_float(param) is None


@pytest.mark.unit
@pytest.mark.parametrize("param", ["0.123", "0.123 ", "0.123 %"])
def test_to_float_good_data(param):
    assert to_float(param) == 0.123
