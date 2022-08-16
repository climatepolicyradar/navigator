from datetime import date
from http.client import OK, UNAUTHORIZED
from unicodedata import category
from app.api.api_v1.routers.documents import document_browse
from app.db.models.document import Document
from .test_document_browse_data import doc_browse_data

URL_UNDER_TEST = f"/api/v1/documents"


def test_document_browse_security(client):
    response = client.get(URL_UNDER_TEST)
    assert response.status_code == UNAUTHORIZED


def test_endpoint_returns_ok(client, user_token_headers, test_db):
    """Test the endpoint returns an empty set with no data"""
    test_db.flush()
    response = client.get(
        URL_UNDER_TEST,
        headers=user_token_headers,
    )
    assert response.status_code == OK


def test_no_filters_returns_all(client, user_token_headers, doc_browse_data):
    """Test that all the data is returned without any filters"""
    response = client.get(
        URL_UNDER_TEST,
        headers=user_token_headers,
    )
    docs = response.json()
    assert response.status_code == OK
    assert len(docs) == 3


def test_country_code(client, user_token_headers, doc_browse_data):
    """Test that the country code filter returns relevant data"""
    test_geo = doc_browse_data["geos"][0]
    response = client.get(
        f"{URL_UNDER_TEST}?country_code={test_geo.value}",
        headers=user_token_headers,
    )
    docs = response.json()
    assert response.status_code == OK
    assert len(docs) == 1
    assert docs[0]["country_code"] == test_geo.value
