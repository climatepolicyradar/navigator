import time
from datetime import datetime

import pytest

from app.api.api_v1.routers import search
from app.db.schemas.search import SortOrder


def test_search_body_valid(test_opensearch, monkeypatch, client, user_token_headers):
    """Test a simple known valid search responds with success."""
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    response = client.post(
        "/api/v1/searches",
        json={"query_string": "disaster", "exact_match": False},
        headers=user_token_headers,
    )
    assert response.status_code == 200

    response = client.post(
        "/api/v1/searches",
        json={"query_string": "disaster", "exact_match": True},
        headers=user_token_headers,
    )
    assert response.status_code == 200


def test_keyword_filters(
    test_opensearch, monkeypatch, client, user_token_headers, mocker
):
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    query_spy = mocker.spy(search._OPENSEARCH_CONNECTION, "query")
    response = client.post(
        "/api/v1/searches",
        json={
            "query_string": "disaster",
            "exact_match": False,
            "keyword_filters": {"action_geography_english_shortname": ["Kenya"]},
        },
        headers=user_token_headers,
    )
    assert response.status_code == 200
    assert query_spy.call_count == 1

    query_body = query_spy.mock_calls[0].args[0]
    assert {"terms": {"action_geography_english_shortname": ["Kenya"]}} in query_body[
        "query"
    ]["bool"]["filter"]


@pytest.mark.parametrize(
    "year_range", [(None, None), (1900, None), (None, 2020), (1900, 2020)]
)
def test_year_range_filters(
    test_opensearch, monkeypatch, client, user_token_headers, mocker, year_range
):
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    query_spy = mocker.spy(search._OPENSEARCH_CONNECTION, "query")
    response = client.post(
        "/api/v1/searches",
        json={
            "query_string": "disaster",
            "exact_match": False,
            "year_range": year_range,
        },
        headers=user_token_headers,
    )
    query_body = query_spy.mock_calls[0].args[0]

    assert response.status_code == 200
    assert query_spy.call_count == 1

    if year_range[0] or year_range[1]:
        expected_range_check = {
            "range": {
                "action_date": dict(
                    [
                        r
                        for r in zip(
                            ["gte", "lte"],
                            [
                                f"01/01/{year_range[0]}"
                                if year_range[0] is not None
                                else None,
                                f"31/12/{year_range[1]}"
                                if year_range[1] is not None
                                else None,
                            ],
                        )
                        if r[1] is not None
                    ]
                )
            }
        }

        assert expected_range_check in query_body["query"]["bool"]["filter"]
    else:
        assert "filter" not in query_body["query"]["bool"]


def test_multiple_filters(
    test_opensearch, monkeypatch, client, user_token_headers, mocker
):
    """Check that multiple filters are successfully applied"""
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    query_spy = mocker.spy(search._OPENSEARCH_CONNECTION, "query")
    response = client.post(
        "/api/v1/searches",
        json={
            "query_string": "disaster",
            "exact_match": False,
            "keyword_filters": {
                "action_geography_english_shortname": ["Kenya"],
                "action_source_name": ["CCLW"],
            },
            "year_range": (1900, 2020),
        },
        headers=user_token_headers,
    )
    query_body = query_spy.mock_calls[0].args[0]

    assert response.status_code == 200
    assert query_spy.call_count == 1

    assert {"terms": {"action_geography_english_shortname": ["Kenya"]}} in query_body[
        "query"
    ]["bool"]["filter"]
    assert {"terms": {"action_source_name": ["CCLW"]}} in query_body["query"]["bool"][
        "filter"
    ]
    assert {
        "range": {"action_date": {"gte": "01/01/1900", "lte": "31/12/2020"}}
    } in query_body["query"]["bool"]["filter"]


def test_result_order_score(
    test_opensearch, monkeypatch, client, user_token_headers, mocker
):
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    query_spy = mocker.spy(search._OPENSEARCH_CONNECTION, "query")
    response = client.post(
        "/api/v1/searches",
        json={
            "query_string": "disaster",
            "exact_match": False,
        },
        headers=user_token_headers,
    )
    assert response.status_code == 200
    query_response = query_spy.spy_return.raw_response
    result_docs = query_response["aggregations"]["sample"]["top_docs"]["buckets"]

    s = None
    for d in result_docs:
        new_s = d["top_hit"]["value"]
        if s is not None:
            assert new_s <= s
        s = new_s


@pytest.mark.parametrize("order", [SortOrder.ASCENDING, SortOrder.DESCENDING])
def test_result_order_date(
    test_opensearch, monkeypatch, client, user_token_headers, order
):
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    response = client.post(
        "/api/v1/searches",
        json={
            "query_string": "disaster",
            "exact_match": False,
            "sort_field": "date",
            "sort_order": order.value,
        },
        headers=user_token_headers,
    )
    assert response.status_code == 200

    response_body = response.json()
    documents = response_body["documents"]
    assert len(documents) > 1

    dt = None
    for d in documents:
        new_dt = datetime.strptime(d["document_date"], "%d/%m/%Y")
        if dt is not None:
            if order == SortOrder.DESCENDING:
                assert new_dt <= dt
            if order == SortOrder.ASCENDING:
                assert new_dt >= dt
        dt = new_dt


@pytest.mark.parametrize("order", [SortOrder.ASCENDING, SortOrder.DESCENDING])
def test_result_order_title(
    test_opensearch, monkeypatch, client, user_token_headers, order
):
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    response = client.post(
        "/api/v1/searches",
        json={
            "query_string": "disaster",
            "exact_match": False,
            "sort_field": "title",
            "sort_order": order.value,
        },
        headers=user_token_headers,
    )
    assert response.status_code == 200

    response_body = response.json()
    documents = response_body["documents"]
    assert len(documents) > 1

    t = None
    for d in documents:
        new_t = d["document_name"]
        if t is not None:
            if order == SortOrder.DESCENDING:
                assert new_t <= t
            if order == SortOrder.ASCENDING:
                assert new_t >= t
        t = new_t


def test_invalid_request(test_opensearch, monkeypatch, client, user_token_headers):
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    response = client.post(
        "/api/v1/searches",
        json={"exact_match": False},
        headers=user_token_headers,
    )
    assert response.status_code == 422

    response = client.post(
        "/api/v1/searches",
        json={"query_string": "disaster"},
        headers=user_token_headers,
    )
    assert response.status_code == 422

    response = client.post(
        "/api/v1/searches",
        json={},
        headers=user_token_headers,
    )
    assert response.status_code == 422


def test_case_insensitivity(test_opensearch, monkeypatch, client, user_token_headers):
    """Make sure that query string results are not affected by case."""
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    response1 = client.post(
        "/api/v1/searches",
        json={"query_string": "disaster", "exact_match": False},
        headers=user_token_headers,
    )
    response2 = client.post(
        "/api/v1/searches",
        json={"query_string": "DiSastEr", "exact_match": False},
        headers=user_token_headers,
    )
    response3 = client.post(
        "/api/v1/searches",
        json={"query_string": "DISASTER", "exact_match": False},
        headers=user_token_headers,
    )

    response1_json = response1.json()
    del response1_json["query_time_ms"]
    response2_json = response2.json()
    del response2_json["query_time_ms"]
    response3_json = response3.json()
    del response3_json["query_time_ms"]

    assert response1_json["documents"]
    assert response1_json == response2_json == response3_json


def test_punctuation_ignored(test_opensearch, monkeypatch, client, user_token_headers):
    """Make sure that punctuation in query strings is ignored."""
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    response1 = client.post(
        "/api/v1/searches",
        json={"query_string": "disaster.", "exact_match": False},
        headers=user_token_headers,
    )
    response2 = client.post(
        "/api/v1/searches",
        json={"query_string": "disaster, ", "exact_match": False},
        headers=user_token_headers,
    )
    response3 = client.post(
        "/api/v1/searches",
        json={"query_string": ";disaster", "exact_match": False},
        headers=user_token_headers,
    )

    response1_json = response1.json()
    del response1_json["query_time_ms"]
    response2_json = response2.json()
    del response2_json["query_time_ms"]
    response3_json = response3.json()
    del response3_json["query_time_ms"]

    assert response1_json["documents"]
    assert response1_json == response2_json == response3_json


def test_accents_ignored(test_opensearch, monkeypatch, client, user_token_headers):
    """Make sure that accents in query strings are ignored."""
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    response1 = client.post(
        "/api/v1/searches",
        json={"query_string": "disàster", "exact_match": False},
        headers=user_token_headers,
    )
    response2 = client.post(
        "/api/v1/searches",
        json={"query_string": "disastër", "exact_match": False},
        headers=user_token_headers,
    )
    response3 = client.post(
        "/api/v1/searches",
        json={"query_string": "disàstér", "exact_match": False},
        headers=user_token_headers,
    )

    response1_json = response1.json()
    del response1_json["query_time_ms"]
    response2_json = response2.json()
    del response2_json["query_time_ms"]
    response3_json = response3.json()
    del response3_json["query_time_ms"]

    assert response1_json["documents"]
    assert response1_json == response2_json == response3_json


def test_unauthenticated(client):
    """Make sure that unauthenticated requests are denied correctly."""
    response = client.post(
        "/api/v1/searches",
        json={"query_string": "a", "exact_match": True},
    )
    assert response.status_code == 401


def test_time_taken(test_opensearch, monkeypatch, client, user_token_headers):
    """Make sure that query time taken is sensible."""
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    start = time.time()
    response = client.post(
        "/api/v1/searches",
        json={"query_string": "disaster", "exact_match": False},
        headers=user_token_headers,
    )
    end = time.time()

    assert response.status_code == 200
    response_json = response.json()
    reported_response_time_ms = response_json["query_time_ms"]
    expected_response_time_ms_max = 1000 * (end - start)
    assert 0 < reported_response_time_ms < expected_response_time_ms_max


def test_empty_search_term(test_opensearch, monkeypatch, client, user_token_headers):
    """Make sure that empty search terms return no results."""
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    response = client.post(
        "/api/v1/searches",
        json={"query_string": "", "exact_match": False},
        headers=user_token_headers,
    )
    assert response.status_code == 200
    assert response.json()["hits"] == 0

    response = client.post(
        "/api/v1/searches",
        json={"query_string": "", "exact_match": True},
        headers=user_token_headers,
    )
    assert response.status_code == 200
    assert response.json()["hits"] == 0