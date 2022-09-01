import time
from datetime import datetime

import pytest

from app.api.api_v1.routers import search
from app.api.api_v1.schemas.search import SortOrder, FilterField
from app.core.search import _FILTER_FIELD_MAP

_TOTAL_DOCUMENT_COUNT = 7


@pytest.mark.search
def test_simple_pagination(test_opensearch, monkeypatch, client, user_token_headers):
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    page1_response = client.post(
        "/api/v1/searches",
        json={
            "query_string": "climate",
            "exact_match": False,
            "limit": 2,
            "offset": 0,
        },
        headers=user_token_headers,
    )
    assert page1_response.status_code == 200

    page1_response_body = page1_response.json()
    page1_documents = page1_response_body["documents"]
    assert len(page1_documents) == 2

    page2_response = client.post(
        "/api/v1/searches",
        json={
            "query_string": "climate",
            "exact_match": False,
            "limit": 2,
            "offset": 2,
        },
        headers=user_token_headers,
    )
    assert page2_response.status_code == 200

    page2_response_body = page2_response.json()
    page2_documents = page2_response_body["documents"]
    assert len(page2_documents) == 2

    # Sanity check that we really do have 4 different documents
    document_names = {d["document_name"] for d in page1_documents} | {
        d["document_name"] for d in page2_documents
    }
    assert len(document_names) == 4

    for d in page1_documents:
        assert d not in page2_documents


@pytest.mark.search
def test_pagination_overlap(test_opensearch, monkeypatch, client, user_token_headers):
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    page1_response = client.post(
        "/api/v1/searches",
        json={
            "query_string": "climate",
            "exact_match": False,
            "limit": 2,
            "offset": 0,
        },
        headers=user_token_headers,
    )
    assert page1_response.status_code == 200

    page1_response_body = page1_response.json()
    page1_documents = page1_response_body["documents"]
    assert len(page1_documents) == 2

    page2_response = client.post(
        "/api/v1/searches",
        json={
            "query_string": "climate",
            "exact_match": False,
            "limit": 2,
            "offset": 1,
        },
        headers=user_token_headers,
    )
    assert page2_response.status_code == 200

    page2_response_body = page2_response.json()
    page2_documents = page2_response_body["documents"]
    assert len(page2_documents) == 2

    # Sanity check that we really do have 3 different documents
    document_names = {d["document_name"] for d in page1_documents} | {
        d["document_name"] for d in page2_documents
    }
    assert len(document_names) == 3

    assert page1_documents[-1] == page2_documents[0]


@pytest.mark.search
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


@pytest.mark.search
def test_keyword_filters(
    test_opensearch, monkeypatch, client, user_token_headers, mocker
):
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    query_spy = mocker.spy(search._OPENSEARCH_CONNECTION, "raw_query")
    response = client.post(
        "/api/v1/searches",
        json={
            "query_string": "climate",
            "exact_match": False,
            "keyword_filters": {"countries": ["Kenya"]},
        },
        headers=user_token_headers,
    )
    assert response.status_code == 200
    assert query_spy.call_count == 1
    query_body = query_spy.mock_calls[0].args[0]

    assert {
        "terms": {_FILTER_FIELD_MAP[FilterField("countries")]: ["Kenya"]}
    } in query_body["query"]["bool"]["filter"]


@pytest.mark.search
def test_invalid_keyword_filters(
    test_opensearch, monkeypatch, client, user_token_headers
):
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    response = client.post(
        "/api/v1/searches",
        json={
            "query_string": "disaster",
            "exact_match": False,
            "keyword_filters": {
                "geographies": ["Kenya"],
                "unknown_filter_no1": ["BOOM"],
            },
        },
        headers=user_token_headers,
    )
    assert response.status_code == 422


@pytest.mark.search
@pytest.mark.parametrize(
    "year_range", [(None, None), (1900, None), (None, 2020), (1900, 2020)]
)
def test_year_range_filters(
    test_opensearch,
    monkeypatch,
    client,
    user_token_headers,
    mocker,
    year_range,
):
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    query_spy = mocker.spy(search._OPENSEARCH_CONNECTION, "raw_query")
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
    # Check that search query default order is not modified unless requested
    assert query_body["aggs"]["sample"]["aggs"]["top_docs"]["terms"]["order"] == {
        "top_hit": "desc"
    }

    if year_range[0] or year_range[1]:
        expected_range_check = {
            "range": {
                "document_date": dict(
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


@pytest.mark.search
def test_multiple_filters(
    test_opensearch, monkeypatch, client, user_token_headers, mocker
):
    """Check that multiple filters are successfully applied"""
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    query_spy = mocker.spy(search._OPENSEARCH_CONNECTION, "raw_query")
    response = client.post(
        "/api/v1/searches",
        json={
            "query_string": "disaster",
            "exact_match": False,
            "keyword_filters": {
                "countries": ["Kenya"],
                "sources": ["CCLW"],
            },
            "year_range": (1900, 2020),
        },
        headers=user_token_headers,
    )
    assert response.status_code == 200
    assert query_spy.call_count == 1
    query_body = query_spy.mock_calls[0].args[0]

    assert {
        "terms": {_FILTER_FIELD_MAP[FilterField("countries")]: ["Kenya"]}
    } in query_body["query"]["bool"]["filter"]
    assert {
        "terms": {_FILTER_FIELD_MAP[FilterField("sources")]: ["CCLW"]}
    } in query_body["query"]["bool"]["filter"]
    assert {
        "range": {"document_date": {"gte": "01/01/1900", "lte": "31/12/2020"}}
    } in query_body["query"]["bool"]["filter"]


@pytest.mark.search
def test_result_order_score(
    test_opensearch, monkeypatch, client, user_token_headers, mocker
):
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    query_spy = mocker.spy(search._OPENSEARCH_CONNECTION, "raw_query")
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


@pytest.mark.search
@pytest.mark.parametrize("order", [SortOrder.ASCENDING, SortOrder.DESCENDING])
def test_result_order_date(
    test_opensearch, monkeypatch, client, user_token_headers, order
):
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    response = client.post(
        "/api/v1/searches",
        json={
            "query_string": "climate",
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


@pytest.mark.search
@pytest.mark.parametrize("order", [SortOrder.ASCENDING, SortOrder.DESCENDING])
def test_result_order_title(
    test_opensearch, monkeypatch, client, user_token_headers, order
):
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    response = client.post(
        "/api/v1/searches",
        json={
            "query_string": "climate",
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


@pytest.mark.search
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
        json={"limit": 1, "offset": 2},
        headers=user_token_headers,
    )
    assert response.status_code == 422

    response = client.post(
        "/api/v1/searches",
        json={},
        headers=user_token_headers,
    )
    assert response.status_code == 422


@pytest.mark.search
def test_case_insensitivity(test_opensearch, monkeypatch, client, user_token_headers):
    """Make sure that query string results are not affected by case."""
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    response1 = client.post(
        "/api/v1/searches",
        json={"query_string": "climate", "exact_match": False},
        headers=user_token_headers,
    )
    response2 = client.post(
        "/api/v1/searches",
        json={"query_string": "ClImAtE", "exact_match": False},
        headers=user_token_headers,
    )
    response3 = client.post(
        "/api/v1/searches",
        json={"query_string": "CLIMATE", "exact_match": False},
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


@pytest.mark.search
def test_punctuation_ignored(test_opensearch, monkeypatch, client, user_token_headers):
    """Make sure that punctuation in query strings is ignored."""
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    response1 = client.post(
        "/api/v1/searches",
        json={"query_string": "climate.", "exact_match": False},
        headers=user_token_headers,
    )
    response2 = client.post(
        "/api/v1/searches",
        json={"query_string": "climate, ", "exact_match": False},
        headers=user_token_headers,
    )
    response3 = client.post(
        "/api/v1/searches",
        json={"query_string": ";climate", "exact_match": False},
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


@pytest.mark.search
def test_accents_ignored(test_opensearch, monkeypatch, client, user_token_headers):
    """Make sure that accents in query strings are ignored."""
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    response1 = client.post(
        "/api/v1/searches",
        json={"query_string": "climàte", "exact_match": False},
        headers=user_token_headers,
    )
    response2 = client.post(
        "/api/v1/searches",
        json={"query_string": "climatë", "exact_match": False},
        headers=user_token_headers,
    )
    response3 = client.post(
        "/api/v1/searches",
        json={"query_string": "climàtë", "exact_match": False},
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


@pytest.mark.search
def test_unauthenticated(client):
    """Make sure that unauthenticated requests are denied correctly."""
    response = client.post(
        "/api/v1/searches",
        json={"query_string": "a", "exact_match": True},
    )
    assert response.status_code == 401


@pytest.mark.search
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


@pytest.mark.search
def test_empty_search_term_performs_browse(
    test_opensearch,
    monkeypatch,
    client,
    user_token_headers,
):
    """Make sure that empty search terms return no results."""
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    response = client.post(
        "/api/v1/searches",
        json={"query_string": ""},
        headers=user_token_headers,
    )
    assert response.status_code == 200
    assert response.json()["hits"] == _TOTAL_DOCUMENT_COUNT


@pytest.mark.search
@pytest.mark.parametrize("order", [SortOrder.ASCENDING, SortOrder.DESCENDING])
def test_browse_order_by_title(
    test_opensearch,
    monkeypatch,
    client,
    user_token_headers,
    order,
):
    """Make sure that empty search terms return no results."""
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    response = client.post(
        "/api/v1/searches",
        json={
            "query_string": "",
            "sort_field": "title",
            "sort_order": order.value,
        },
        headers=user_token_headers,
    )
    assert response.status_code == 200

    response_body = response.json()
    documents = response_body["documents"]
    assert len(documents) == _TOTAL_DOCUMENT_COUNT

    t = None
    for d in documents:
        new_t = d["document_name"]
        if t is not None:
            if order == SortOrder.DESCENDING:
                assert new_t <= t
            if order == SortOrder.ASCENDING:
                assert new_t >= t
        t = new_t


@pytest.mark.search
@pytest.mark.parametrize("order", [SortOrder.ASCENDING, SortOrder.DESCENDING])
def test_browse_order_by_date(
    test_opensearch,
    monkeypatch,
    client,
    user_token_headers,
    order,
):
    """Make sure that empty search terms return no results."""
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    response = client.post(
        "/api/v1/searches",
        json={
            "query_string": "",
            "sort_field": "date",
            "sort_order": order.value,
        },
        headers=user_token_headers,
    )
    assert response.status_code == 200

    response_body = response.json()
    documents = response_body["documents"]
    assert len(documents) == _TOTAL_DOCUMENT_COUNT

    dt = None
    for d in documents:
        new_dt = datetime.strptime(d["document_date"], "%d/%m/%Y")
        if dt is not None:
            if order == SortOrder.DESCENDING:
                assert new_dt <= dt
            if order == SortOrder.ASCENDING:
                assert new_dt >= dt
        dt = new_dt


@pytest.mark.search
@pytest.mark.parametrize("limit", [1, 4, 7, 10])
@pytest.mark.parametrize("offset", [0, 1, 7, 10])
def test_browse_limit_offset(
    test_opensearch,
    monkeypatch,
    client,
    user_token_headers,
    limit,
    offset,
):
    """Make sure that empty search terms return no results."""
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    response = client.post(
        "/api/v1/searches",
        json={"query_string": "", "limit": limit, "offset": offset},
        headers=user_token_headers,
    )
    assert response.status_code == 200

    response_body = response.json()
    documents = response_body["documents"]
    assert len(documents) == min(limit, max(0, _TOTAL_DOCUMENT_COUNT - offset))


@pytest.mark.search
def test_browse_filters(
    test_opensearch, monkeypatch, client, user_token_headers, mocker
):
    """Check that multiple filters are successfully applied"""
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    query_spy = mocker.spy(search._OPENSEARCH_CONNECTION, "raw_query")
    response = client.post(
        "/api/v1/searches",
        json={
            "query_string": "",
            "keyword_filters": {
                "countries": ["Kenya"],
                "sources": ["CCLW"],
            },
            "year_range": (1900, 2020),
        },
        headers=user_token_headers,
    )
    assert response.status_code == 200
    assert query_spy.call_count == 1
    query_body = query_spy.mock_calls[0].args[0]

    assert {
        "terms": {_FILTER_FIELD_MAP[FilterField("countries")]: ["Kenya"]}
    } in query_body["query"]["bool"]["filter"]
    assert {
        "terms": {_FILTER_FIELD_MAP[FilterField("sources")]: ["CCLW"]}
    } in query_body["query"]["bool"]["filter"]
    assert {
        "range": {"document_date": {"gte": "01/01/1900", "lte": "31/12/2020"}}
    } in query_body["query"]["bool"]["filter"]

    response_body = response.json()
    documents = response_body["documents"]
    assert len(documents) == 0
