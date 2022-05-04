import datetime as dt
from typing import List

import pandas as pd

from app.model import PolicyLookup, PolicyData, Key, Doc
from app.loaders.loader_cclw_v1.transform.main import transform


def test_transform():
    policies_fe = pd.DataFrame(
        {
            "policy_name": ["foo", "will be dropped as has no doc"],
            "country_code": ["cc", "xx"],
            "document_list": ["doc name|http://doc|en;second doc|http://doc2|", None],
            "policy_description": ["<div>foobar</div>", "nodoc"],
            "events": ["17/11/1979|Law passed", None],
            "policy_category": ["legislative", "legislative"],
            "sectors": ["Two,Sectors", ""],
            "instruments": ["", ""],
            "frameworks": ["", ""],
            "responses": ["", ""],
            "hazards": ["", ""],
            "document_type": ["doc type", ""],
        }
    )

    results: PolicyLookup = transform(policies_fe)

    keys = list(results.keys())
    assert len(keys) == 1

    key: Key = keys[0]
    policy: PolicyData = results[key]

    assert policy.policy_name == "foo"
    assert policy.policy_category == "Law"
    assert policy.country_code == "cc"
    assert policy.policy_date.date() == dt.date(1979, 11, 17)
    assert policy.policy_description == "foobar"

    docs: List[Doc] = policy.docs
    assert len(docs) == 2

    doc_one: Doc = docs[0]
    assert doc_one.doc_name == "doc name"
    assert doc_one.doc_languages == ["en"]
    assert doc_one.doc_url == "https://doc"
    assert doc_one.sectors == ["Two", "Sectors"]
    assert doc_one.document_type == "doc type"

    doc_two: Doc = docs[1]
    assert doc_two.doc_name == "second doc"
    assert doc_two.doc_languages == [None]
    assert doc_two.doc_url == "https://doc2"
    assert doc_two.sectors == ["Two", "Sectors"]
    assert doc_two.document_type == "doc type"


def test_transform_no_doc():
    policies_fe = pd.DataFrame(
        {
            "policy_name": ["will be dropped as has no doc"],
            "country_code": ["cc"],
            "document_list": [None],
            "policy_description": ["foobar"],
            "events": ["17/11/1979|Law passed"],
            "policy_category": ["legislative"],
            "sectors": [""],
            "instruments": [""],
            "frameworks": [""],
            "responses": [""],
            "hazards": [""],
        }
    )

    results: PolicyLookup = transform(policies_fe)

    keys = list(results.keys())
    assert len(keys) == 0


def test_transform_no_date():
    policies_fe = pd.DataFrame(
        {
            "policy_name": ["will be dropped as has no date"],
            "country_code": ["cc"],
            "document_list": ["doc name|http://doc|;second doc|http://doc2|en"],
            "policy_description": ["foobar"],
            "events": [None],
            "policy_category": ["legislative"],
            "sectors": [""],
            "instruments": [""],
            "frameworks": [""],
            "responses": [""],
            "hazards": [""],
            "document_type": [""],
        }
    )

    results: PolicyLookup = transform(policies_fe)

    keys = list(results.keys())
    assert len(keys) == 0
