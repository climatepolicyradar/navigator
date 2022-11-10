import dataclasses
import time
from datetime import datetime

import fastapi
import pytest

import app.core
import app.core.jit_query_wrapper
from app.api.api_v1.routers import search
from app.api.api_v1.schemas.search import (
    JitQuery,
    SearchRequestBody,
    SortOrder,
    FilterField,
)
from app.core.search import _FILTER_FIELD_MAP, OpenSearchQueryConfig
from app.db.models import Geography


@pytest.mark.search
def test_simple_pagination(test_opensearch, monkeypatch, client):
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    page1_response = client.post(
        "/api/v1/searches",
        json={
            "query_string": "climate",
            "exact_match": False,
            "limit": 2,
            "offset": 0,
        },
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
    )
    assert page2_response.status_code == 200

    page2_response_body = page2_response.json()
    page2_documents = page2_response_body["documents"]
    assert len(page2_documents) == 2

    # Sanity check that we really do have 4 different documents
    document_slugs = {d["document_slug"] for d in page1_documents} | {
        d["document_slug"] for d in page2_documents
    }
    assert len(document_slugs) == 4

    for d in page1_documents:
        assert d not in page2_documents


@pytest.mark.search
def test_search_result_schema(caplog, test_opensearch, monkeypatch, client):
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    expected_search_result_schema = sorted(
        [
            "document_name",
            "document_postfix",
            "document_geography",
            "document_source",
            "document_sectors",
            "document_date",
            "document_id",
            "document_slug",
            "document_description",
            "document_type",
            "document_category",
            "document_source_url",
            "document_url",
            "document_content_type",
            "document_title_match",
            "document_description_match",
            "document_passage_matches",
        ]
    )
    page1_response = client.post(
        "/api/v1/searches",
        json={
            "query_string": "climate",
            "exact_match": False,
            "limit": 100,
            "offset": 0,
        },
    )
    assert page1_response.status_code == 200

    page1_response_body = page1_response.json()
    page1_documents = page1_response_body["documents"]
    assert len(page1_documents) > 0

    for d in page1_documents:
        assert sorted(list(d.keys())) == expected_search_result_schema

    assert "Document ids missing" in caplog.text


@pytest.mark.search
def test_pagination_overlap(test_opensearch, monkeypatch, client):
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    page1_response = client.post(
        "/api/v1/searches",
        json={
            "query_string": "climate",
            "exact_match": False,
            "limit": 2,
            "offset": 0,
        },
    )
    assert page1_response.status_code == 200

    page1_response_body = page1_response.json()
    page1_documents = page1_response_body["documents"]
    assert len(page1_documents) > 1

    page2_response = client.post(
        "/api/v1/searches",
        json={
            "query_string": "climate",
            "exact_match": False,
            "limit": 2,
            "offset": 1,
        },
    )
    assert page2_response.status_code == 200

    page2_response_body = page2_response.json()
    page2_documents = page2_response_body["documents"]
    assert len(page2_documents) > 0

    # Check that page 2 documents are different to page 1 documents
    assert len(
        {d["document_slug"] for d in page1_documents}
        | {d["document_slug"] for d in page2_documents}
    ) > len({d["document_slug"] for d in page1_documents})

    assert page1_documents[-1] == page2_documents[0]


@pytest.mark.search
def test_search_body_valid(test_opensearch, monkeypatch, client):
    """Test a simple known valid search responds with success."""
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    response = client.post(
        "/api/v1/searches",
        json={"query_string": "disaster", "exact_match": False},
    )
    assert response.status_code == 200

    response = client.post(
        "/api/v1/searches",
        json={"query_string": "disaster", "exact_match": True},
    )
    assert response.status_code == 200


@pytest.mark.search
def test_jit_query_is_default(test_opensearch, monkeypatch, client, mocker):
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)
    jit_query_spy = mocker.spy(app.core.jit_query_wrapper, "jit_query")  # noqa
    background_task_spy = mocker.spy(fastapi.BackgroundTasks, "add_task")

    response = client.post(
        "/api/v1/searches",
        json={
            "query_string": "climate",
            "exact_match": True,
        },
    )

    assert response.status_code == 200

    # Check the jit query called by checking the background task has been added
    assert jit_query_spy.call_count == 1 or jit_query_spy.call_count == 2
    assert background_task_spy.call_count == 1


@pytest.mark.search
def test_with_jit(test_opensearch, monkeypatch, client, mocker):
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)
    jit_query_spy = mocker.spy(app.core.jit_query_wrapper, "jit_query")
    background_task_spy = mocker.spy(fastapi.BackgroundTasks, "add_task")

    response = client.post(
        "/api/v1/searches",
        json={
            "query_string": "climate",
            "exact_match": True,
        },
    )

    assert response.status_code == 200

    # Check the jit query call
    assert jit_query_spy.call_count == 1 or jit_query_spy.call_count == 2
    actual_search_body = jit_query_spy.mock_calls[0].args[1]
    actual_config = jit_query_spy.mock_calls[0].args[2]

    expected_search_body = SearchRequestBody(
        query_string="climate",
        exact_match=True,
        max_passages_per_doc=10,
        keyword_filters=None,
        year_range=None,
        sort_field=None,
        sort_order=SortOrder.DESCENDING,
        jit_query=JitQuery.ENABLED,
        limit=10,
        offset=0,
    )
    assert actual_search_body == expected_search_body

    # Check the first call has overriden the default config
    overrides = {
        "max_doc_count": 20,
    }
    expected_config = dataclasses.replace(OpenSearchQueryConfig(), **overrides)
    assert actual_config == expected_config

    # Check the background query call
    assert background_task_spy.call_count == 1
    actual_bkg_search_body = background_task_spy.mock_calls[0].args[3]

    expected_bkg_search_body = SearchRequestBody(
        query_string="climate",
        exact_match=True,
        max_passages_per_doc=10,
        keyword_filters=None,
        year_range=None,
        sort_field=None,
        sort_order=SortOrder.DESCENDING,
        jit_query=JitQuery.ENABLED,
        limit=10,
        offset=0,
    )
    assert actual_bkg_search_body == expected_bkg_search_body

    # Check the background call is run with default config
    actual_bkg_config = background_task_spy.mock_calls[0].args[4]
    assert actual_bkg_config == OpenSearchQueryConfig()


@pytest.mark.search
def test_without_jit(test_opensearch, monkeypatch, client, mocker):
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)
    query_spy = mocker.spy(search._OPENSEARCH_CONNECTION, "query")
    background_task_spy = mocker.spy(fastapi.BackgroundTasks, "add_task")

    response = client.post(
        "/api/v1/searches",
        json={
            "query_string": "climate",
            "exact_match": True,
            "jit_query": "disabled",
        },
    )
    assert response.status_code == 200
    # Ensure nothing has/is going on in the background
    assert background_task_spy.call_count == 0
    assert query_spy.call_count == 1  # Called once as not using jit search

    actual_search_body = query_spy.mock_calls[0].args[0]

    expected_search_body = SearchRequestBody(
        query_string="climate",
        exact_match=True,
        max_passages_per_doc=10,
        keyword_filters=None,
        year_range=None,
        sort_field=None,
        sort_order=SortOrder.DESCENDING,
        jit_query=JitQuery.DISABLED,
        limit=10,
        offset=0,
    )
    assert actual_search_body == expected_search_body

    # Check default config is used
    actual_config = query_spy.mock_calls[0].args[1]
    expected_config = OpenSearchQueryConfig()
    assert actual_config == expected_config


@pytest.mark.search
def test_keyword_filters(test_opensearch, client, test_db, monkeypatch, mocker):
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    ssa = Geography(
        display_value="Sub-Saharan Africa",
        slug="sub-saharan-africa",
        value="Sub-Saharan Africa",
        type="region",
    )
    test_db.add(ssa)
    test_db.flush()
    test_db.add(
        Geography(
            display_value="Kenya",
            slug="kenya",
            value="KEN",
            type="country",
            parent_id=ssa.id,
        )
    )
    test_db.commit()

    query_spy = mocker.spy(search._OPENSEARCH_CONNECTION, "raw_query")
    response = client.post(
        "/api/v1/searches",
        json={
            "query_string": "climate",
            "exact_match": False,
            "keyword_filters": {"countries": ["kenya"]},
            "jit_query": "disabled",
        },
    )
    assert response.status_code == 200
    assert query_spy.call_count == 1
    query_body = query_spy.mock_calls[0].args[0]

    assert {
        "terms": {_FILTER_FIELD_MAP[FilterField("countries")]: ["KEN"]}
    } in query_body["query"]["bool"]["filter"]


@pytest.mark.search
def test_keyword_filters_region(test_opensearch, test_db, monkeypatch, client, mocker):
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    region = Geography(
        display_value="South Asia",
        slug="south-asia",
        value="South Asia",
        type="region",
    )
    test_db.add(region)
    test_db.flush()
    afghanistan = Geography(
        display_value="Afghanistan",
        slug="afghanistan",
        value="AFG",
        type="country",
        parent_id=region.id,
    )
    test_db.add(afghanistan)
    test_db.add(
        Geography(
            display_value="Bhutan",
            slug="bhutan",
            value="BTN",
            type="country",
            parent_id=region.id,
        )
    )
    test_db.flush()
    test_db.add(
        Geography(
            display_value="Kabul",
            slug="kabul",
            value="Kabul",
            type="city",
            parent_id=afghanistan.id,
        )
    )
    test_db.commit()

    query_spy = mocker.spy(search._OPENSEARCH_CONNECTION, "raw_query")
    response = client.post(
        "/api/v1/searches",
        json={
            "query_string": "climate",
            "exact_match": False,
            "keyword_filters": {"regions": ["south-asia"]},
            "jit_query": "disabled",
        },
    )
    assert response.status_code == 200
    assert query_spy.call_count == 1
    query_body = query_spy.mock_calls[0].args[0]

    assert {
        "terms": {_FILTER_FIELD_MAP[FilterField.COUNTRY]: ["AFG", "BTN"]}
    } in query_body["query"]["bool"]["filter"]

    # Only country filters should be added
    query_term_keys = []
    for d in query_body["query"]["bool"]["filter"]:
        search_term_dict = d["terms"]
        query_term_keys.extend(search_term_dict.keys())

    assert [_FILTER_FIELD_MAP[FilterField.COUNTRY]] == query_term_keys


@pytest.mark.search
def test_keyword_filters_region_invalid(test_opensearch, monkeypatch, client, mocker):
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    query_spy = mocker.spy(search._OPENSEARCH_CONNECTION, "raw_query")
    response = client.post(
        "/api/v1/searches",
        json={
            "query_string": "climate",
            "exact_match": False,
            "keyword_filters": {"regions": ["daves-region"]},
            "jit_query": "disabled",
        },
    )
    assert response.status_code == 200
    assert query_spy.call_count == 1
    query_body = query_spy.mock_calls[0].args[0]

    # The region is invalid, so no filters should be applied
    assert "filter" not in query_body["query"]["bool"]


@pytest.mark.search
def test_invalid_keyword_filters(test_opensearch, test_db, monkeypatch, client):
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    ssa = Geography(
        display_value="Sub-Saharan Africa",
        slug="sub-saharan-africa",
        value="Sub-Saharan Africa",
        type="region",
    )
    test_db.add(ssa)
    test_db.flush()
    test_db.add(
        Geography(
            display_value="Kenya",
            slug="kenya",
            value="KEN",
            type="country",
            parent_id=ssa.id,
        )
    )
    test_db.commit()

    response = client.post(
        "/api/v1/searches",
        json={
            "query_string": "disaster",
            "exact_match": False,
            "keyword_filters": {
                "geographies": ["kenya"],
                "unknown_filter_no1": ["BOOM"],
            },
        },
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
            "jit_query": "disabled",
        },
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
def test_multiple_filters(test_opensearch, test_db, monkeypatch, client, mocker):
    """Check that multiple filters are successfully applied"""
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    ssa = Geography(
        display_value="Sub-Saharan Africa",
        slug="sub-saharan-africa",
        value="Sub-Saharan Africa",
        type="region",
    )
    test_db.add(ssa)
    test_db.flush()
    test_db.add(
        Geography(
            display_value="Kenya",
            slug="kenya",
            value="KEN",
            type="country",
            parent_id=ssa.id,
        )
    )
    test_db.commit()

    query_spy = mocker.spy(search._OPENSEARCH_CONNECTION, "raw_query")
    response = client.post(
        "/api/v1/searches",
        json={
            "query_string": "disaster",
            "exact_match": False,
            "keyword_filters": {
                "countries": ["kenya"],
                "sources": ["CCLW"],
            },
            "year_range": (1900, 2020),
            "jit_query": "disabled",
        },
    )
    assert response.status_code == 200
    assert query_spy.call_count == 1
    query_body = query_spy.mock_calls[0].args[0]

    assert {
        "terms": {_FILTER_FIELD_MAP[FilterField("countries")]: ["KEN"]}
    } in query_body["query"]["bool"]["filter"]
    assert {
        "terms": {_FILTER_FIELD_MAP[FilterField("sources")]: ["CCLW"]}
    } in query_body["query"]["bool"]["filter"]
    assert {
        "range": {"document_date": {"gte": "01/01/1900", "lte": "31/12/2020"}}
    } in query_body["query"]["bool"]["filter"]


@pytest.mark.search
def test_result_order_score(test_opensearch, monkeypatch, client, mocker):
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    query_spy = mocker.spy(search._OPENSEARCH_CONNECTION, "raw_query")
    response = client.post(
        "/api/v1/searches",
        json={
            "query_string": "disaster",
            "exact_match": False,
        },
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
def test_result_order_date(test_opensearch, monkeypatch, client, order):
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    response = client.post(
        "/api/v1/searches",
        json={
            "query_string": "climate",
            "exact_match": False,
            "sort_field": "date",
            "sort_order": order.value,
        },
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
def test_result_order_title(test_opensearch, monkeypatch, client, order):
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    response = client.post(
        "/api/v1/searches",
        json={
            "query_string": "climate",
            "exact_match": False,
            "sort_field": "title",
            "sort_order": order.value,
        },
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
def test_invalid_request(test_opensearch, monkeypatch, client):
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    response = client.post(
        "/api/v1/searches",
        json={"exact_match": False},
    )
    assert response.status_code == 422

    response = client.post(
        "/api/v1/searches",
        json={"limit": 1, "offset": 2},
    )
    assert response.status_code == 422

    response = client.post(
        "/api/v1/searches",
        json={},
    )
    assert response.status_code == 422


@pytest.mark.search
def test_case_insensitivity(test_opensearch, monkeypatch, client):
    """Make sure that query string results are not affected by case."""
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    response1 = client.post(
        "/api/v1/searches",
        json={"query_string": "climate", "exact_match": False},
    )
    response2 = client.post(
        "/api/v1/searches",
        json={"query_string": "climate", "exact_match": False},
    )
    response3 = client.post(
        "/api/v1/searches",
        json={"query_string": "climate", "exact_match": False},
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
def test_punctuation_ignored(test_opensearch, monkeypatch, client):
    """Make sure that punctuation in query strings is ignored."""
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    response1 = client.post(
        "/api/v1/searches",
        json={"query_string": "climate.", "exact_match": False},
    )
    response2 = client.post(
        "/api/v1/searches",
        json={"query_string": "climate, ", "exact_match": False},
    )
    response3 = client.post(
        "/api/v1/searches",
        json={"query_string": ";climate", "exact_match": False},
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
def test_sensitive_queries(test_opensearch, monkeypatch, client):
    """Make sure that queries in the list of sensitive queries only return results containing that term, and not KNN results."""
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    response1 = client.post(
        "/api/v1/searches",
        json={"query_string": "spain", "exact_match": False},
    )

    response2 = client.post(
        "/api/v1/searches",
        json={"query_string": "clean energy strategy", "exact_match": False},
    )

    # In this example the sensitive term is less than half the length of the query, so KNN results should be returned
    response3 = client.post(
        "/api/v1/searches",
        json={"query_string": "spanish ghg emissions", "exact_match": False},
    )

    response1_json = response1.json()
    response2_json = response2.json()
    response3_json = response3.json()

    # If the queries above return no results then the tests below are meaningless
    assert len(response1_json["documents"]) > 0
    assert len(response2_json["documents"]) > 0
    assert len(response3_json["documents"]) > 0

    assert all(
        [
            "spain" in passage_match["text"].lower()
            for document in response1_json["documents"]
            for passage_match in document["document_passage_matches"]
        ]
    )
    assert not all(
        [
            "clean energy strategy" in passage_match["text"].lower()
            for document in response2_json["documents"]
            for passage_match in document["document_passage_matches"]
        ]
    )
    assert not all(
        [
            "spanish ghg emissions" in passage_match["text"].lower()
            for document in response3_json["documents"]
            for passage_match in document["document_passage_matches"]
        ]
    )


@pytest.mark.search
def test_accents_ignored(test_opensearch, monkeypatch, client):
    """Make sure that accents in query strings are ignored."""
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    response1 = client.post(
        "/api/v1/searches",
        json={"query_string": "climàte", "exact_match": False},
    )
    response2 = client.post(
        "/api/v1/searches",
        json={"query_string": "climatë", "exact_match": False},
    )
    response3 = client.post(
        "/api/v1/searches",
        json={"query_string": "climàtë", "exact_match": False},
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
def test_time_taken(test_opensearch, monkeypatch, client):
    """Make sure that query time taken is sensible."""
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    start = time.time()
    response = client.post(
        "/api/v1/searches",
        json={"query_string": "disaster", "exact_match": False},
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
):
    """Make sure that empty search term returns results in browse mode."""
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    response = client.post(
        "/api/v1/searches",
        json={"query_string": ""},
    )
    assert response.status_code == 200
    assert response.json()["hits"] > 0
    assert len(response.json()["documents"]) > 0


@pytest.mark.search
@pytest.mark.parametrize("order", [SortOrder.ASCENDING, SortOrder.DESCENDING])
def test_browse_order_by_title(
    test_opensearch,
    monkeypatch,
    client,
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
    )
    assert response.status_code == 200

    response_body = response.json()
    documents = response_body["documents"]
    assert len(documents) > 0

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
    )
    assert response.status_code == 200

    response_body = response.json()
    documents = response_body["documents"]
    assert len(documents) > 0

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
def test_browse_limit_offset(
    test_opensearch,
    monkeypatch,
    client,
    limit,
):
    """Make sure that the offset parameter in browse mode works."""
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    response_offset_0 = client.post(
        "/api/v1/searches",
        json={"query_string": "", "limit": limit, "offset": 0},
    )
    response_offset_2 = client.post(
        "/api/v1/searches",
        json={"query_string": "", "limit": limit, "offset": 2},
    )

    assert response_offset_0.status_code == 200
    assert response_offset_2.status_code == 200

    response_offset_0_body = response_offset_0.json()
    documents = response_offset_0_body["documents"]
    assert len(documents) <= limit

    response_offset_2_body = response_offset_2.json()
    documents = response_offset_2_body["documents"]
    assert len(documents) <= limit

    assert (
        response_offset_0_body["documents"][
            2 : len(response_offset_2_body["documents"])
        ]
        == response_offset_2_body["documents"][:-2]
    )


@pytest.mark.search
def test_browse_filters(test_opensearch, test_db, monkeypatch, client, mocker):
    """Check that multiple filters are successfully applied"""
    monkeypatch.setattr(search, "_OPENSEARCH_CONNECTION", test_opensearch)

    ssa = Geography(
        display_value="Sub-Saharan Africa",
        slug="sub-saharan-africa",
        value="Sub-Saharan Africa",
        type="region",
    )
    test_db.add(ssa)
    test_db.flush()
    test_db.add(
        Geography(
            display_value="Kenya",
            slug="kenya",
            value="KEN",
            type="country",
            parent_id=ssa.id,
        )
    )
    test_db.commit()

    query_spy = mocker.spy(search._OPENSEARCH_CONNECTION, "raw_query")
    response = client.post(
        "/api/v1/searches",
        json={
            "query_string": "",
            "keyword_filters": {
                "countries": ["kenya"],
                "sources": ["CCLW"],
            },
            "year_range": (1900, 2020),
            "jit_query": "disabled",
        },
    )
    assert response.status_code == 200
    assert query_spy.call_count == 1
    query_body = query_spy.mock_calls[0].args[0]

    assert {
        "terms": {_FILTER_FIELD_MAP[FilterField("countries")]: ["KEN"]}
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
