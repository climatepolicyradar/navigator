from datetime import datetime
from unittest.mock import patch

from app.load import load
from app.model import Key, PolicyData, Doc, PolicyLookup


@patch("app.load.main.get_language_id_for_doc")
@patch("app.load.main.get_geography_id")
@patch("app.load.main.get_type_id")
@patch("app.load.main.post_action")
def test_load(
    mock_post_action,
    mock_get_type_id,
    mock_get_geography_id,
    mock_get_language_id_for_doc,
):
    mock_post_action.return_value.status_code = 200
    mock_get_type_id.return_value = 123
    mock_get_geography_id.return_value = 456
    mock_get_language_id_for_doc.return_value = 789

    policy_key = Key(
        policy_name="foo",
        policy_type="Law",
        country_code="cc",
        policy_date=datetime(1979, 11, 17),
    )
    doc: Doc = Doc(
        doc_url="http://doc",
        doc_name="doc name",
        doc_language="en",
    )
    policy_data: PolicyData = PolicyData(
        **policy_key.__dict__,
        policy_description="foobar",
        docs=[doc],
    )
    policies: PolicyLookup = {
        policy_key: policy_data,
    }

    load(policies)

    mock_post_action.assert_called_once_with(
        {
            "name": policy_data.policy_name,
            "description": policy_data.policy_description,
            "year": policy_data.policy_date.year,
            "month": policy_data.policy_date.month,
            "day": policy_data.policy_date.day,
            "geography_id": 456,
            "type_id": 123,
            "source_id": 1,  # CCLW is source_id 1
            "documents": [
                {
                    "name": doc.doc_name,
                    "language_id": 789,
                    "source_url": doc.doc_url,
                    "s3_url": None,
                    "year": policy_data.policy_date.year,
                    "month": policy_data.policy_date.month,
                    "day": policy_data.policy_date.day,
                },
            ],
        }
    )
    mock_get_type_id.assert_called_once_with(policy_data.policy_type)
    mock_get_geography_id.assert_called_once_with(policy_data.country_code)
    mock_get_language_id_for_doc.assert_called_once_with(doc)
