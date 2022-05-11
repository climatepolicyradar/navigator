import datetime as dt
from typing import List

import pandas as pd

from app.model import PolicyLookup, PolicyData, Key, Doc
from app.loaders.loader_cclw_v2.transform.main import transform


def test_transform():
    policies_fe = pd.DataFrame(
        {
            "policy_id": ["1", "2"],
            "document_name": ["foo", "will be dropped as has no URL"],
            "document_description": ["some description", "another description"],
            "country_code": ["cc", "xx"],
            "document_url": ["http://doc|en", None],
            "category": ["legislative", "legislative"],
            "policy_description": ["<div>foobar</div>", "nodoc"],
            "events": ["17/11/1979|Law passed", None],
            "sectors": ["Two;Sectors", ""],
            "instruments": ["", ""],
            "frameworks": ["", ""],
            "responses": ["", ""],
            "hazards": ["", ""],
            "document_type": ["doc type", ""],
            "keywords": ["keyword1; keyword2", ""],
            "document_year": ["2020", "2021"],
            "document_language": ["English", "Afrikaans"],
        }
    )

    results: PolicyLookup = transform(policies_fe)

    keys = list(results.keys())
    assert len(keys) == 1

    key: Key = keys[0]
    policy: PolicyData = results[key]

    assert policy.policy_name == "1"
    assert policy.country_code == "cc"
    # a bunch of properties are not being set on policy/action-level for the CCLW v2 parser
    assert policy.policy_category is None
    assert policy.policy_date is None
    assert policy.policy_description is None

    docs: List[Doc] = policy.docs
    assert len(docs) == 1

    doc_one: Doc = docs[0]
    assert doc_one.doc_name == "foo"
    assert doc_one.doc_description == "some description"
    assert doc_one.doc_languages == ["English"]
    assert doc_one.doc_url == "https://doc"
    assert doc_one.document_category == "Law"
    assert doc_one.publication_date == dt.datetime(2020, 1, 1)
    assert doc_one.sectors == ["Two", "Sectors"]
    assert doc_one.document_type == "doc type"
    assert doc_one.keywords == ["keyword1", "keyword2"]


# TODO multiple related docs


def test_transform_no_url():
    policies_fe = pd.DataFrame(
        {
            "policy_id": ["1"],
            "document_name": ["will be dropped as has no URL"],
            "document_description": ["description"],
            "country_code": ["cc"],
            "document_url": [None],
            "policy_description": ["foobar"],
            "events": ["17/11/1979|Law passed"],
            "category": ["legislative"],
            "sectors": [""],
            "instruments": [""],
            "frameworks": [""],
            "responses": [""],
            "hazards": [""],
            "document_type": ["doc type"],
            "keywords": [""],
            "document_year": ["2020"],
            "document_language": ["English"],
        }
    )

    results: PolicyLookup = transform(policies_fe)

    keys = list(results.keys())
    assert len(keys) == 0


def test_transform_no_date():
    policies_fe = pd.DataFrame(
        {
            "policy_id": ["1"],
            "document_name": ["will be dropped as has no date"],
            "document_description": ["description"],
            "country_code": ["cc"],
            "document_url": ["https://doc"],
            "policy_description": ["foobar"],
            "events": [""],  # no date here either
            "category": ["legislative"],
            "sectors": [""],
            "instruments": [""],
            "frameworks": [""],
            "responses": [""],
            "hazards": [""],
            "document_type": ["doc type"],
            "keywords": [""],
            "document_year": [None],
            "document_language": ["English"],
        }
    )

    results: PolicyLookup = transform(policies_fe)

    keys = list(results.keys())
    assert (
        len(keys) == 1
    )  # as dates always default to 1900, in the absence of anything else.
