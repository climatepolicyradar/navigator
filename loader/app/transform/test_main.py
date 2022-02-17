import datetime as dt

import pandas as pd

from app.model import IngestData
from app.transform import transform


def test_transform():
    policies_fe = pd.DataFrame({
        'policy_name': ['foo', 'will be dropped as has no doc', 'frontend only'],
        'country_code': ['cc', 'xx', 'yy'],
        'document_list': ['doc name|http://doc|', None, 'doc name|http://doc|'],
        'policy_description': ['foobar', 'nodoc', 'this row is in frontend csv only'],
        'events': ['17/11/1979|Law passed', None, '17/11/1979|Law passed'],
    })

    policies = pd.DataFrame({
        'source_policy_id': ['1', '2', '3'],
        'policy_name': ['foo', 'will be dropped as has no doc', 'backend only'],
        'policy_type': ['legislative', 'legislative', 'legislative'],
        'country_code': ['cc', 'xx', 'yy'],
    })

    data: IngestData = IngestData(policies_fe=policies_fe, policies=policies, docs=None, targets=None)

    results = transform(data)

    assert len(results) == 1, "Only 1 entry from each of frontend and backend CSVs should match"

    result = results.iloc[0]
    assert result.source_policy_id == '1'
    assert result.policy_name == 'foo'
    assert result.policy_type == 'legislative'
    assert result.country_code == 'cc'
    assert result.policy_id is None
    assert result.doc_name == 'doc name'
    assert result.language is None
    assert result.doc_url == 'http://doc'
    assert result.description == 'foobar'
    assert result.policy_date.date() == dt.date(1979, 11, 17)
