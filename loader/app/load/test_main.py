import datetime as dt
from unittest.mock import patch

import pandas as pd

from app.load import load


@patch('app.load.main.get_geography_id')
@patch('app.load.main.get_type_id')
@patch('app.load.main.post_action')
def test_load(mock_post_action, mock_get_type_id, mock_get_geography_id):
    mock_post_action.return_value.status_code = 200
    mock_get_type_id.return_value = 123
    mock_get_geography_id.return_value = 456

    policies = pd.DataFrame({
        'policy_name': ['foo'],
        'policy_type': ['legislative'],
        'policy_date': [dt.date(1979, 11, 17)],
        'country_code': ['cc'],
        'description': ['foobar'],
    })
    policy = policies.iloc[0]

    load(policies)

    mock_post_action.assert_called_once_with({
        "name": policy["policy_name"],
        "description": policy["description"],
        "year": 1979,
        "month": 11,
        "day": 17,
        "geography_id": 456,
        "type_id": 123,
        "source_id": 1,  # CCLW is source_id 1
        "documents": [],
    })
    mock_get_type_id.assert_called_once_with("Law")
    mock_get_geography_id.assert_called_once_with("cc")
