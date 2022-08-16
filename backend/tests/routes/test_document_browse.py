from dateutil import parser
from http.client import OK, UNAUTHORIZED

URL_UNDER_TEST = "/api/v1/documents"


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


def test_response_is_ordered(client, user_token_headers, doc_browse_data):
    """Test that all the data is returned ordered by date descending"""
    response = client.get(
        URL_UNDER_TEST,
        headers=user_token_headers,
    )
    docs = response.json()
    assert response.status_code == OK
    assert len(docs) == 3
    assert docs[0]["name"] == "doc3"
    assert docs[1]["name"] == "doc2"
    assert docs[2]["name"] == "doc1"


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


def test_start_year(client, user_token_headers, doc_browse_data):
    """Test that the start_year filter returns relevant data"""
    start_year = 2000
    response = client.get(
        f"{URL_UNDER_TEST}?start_year={start_year}",
        headers=user_token_headers,
    )
    docs = response.json()
    assert response.status_code == OK
    assert len(docs) == 2
    year1 = parser.parse(docs[0]["publication_ts"]).year
    year2 = parser.parse(docs[1]["publication_ts"]).year
    assert year1 >= start_year
    assert year2 >= start_year
    assert docs[0]["name"] == "doc3"
    assert docs[1]["name"] == "doc2"


def test_end_year(client, user_token_headers, doc_browse_data):
    """Test that the end_year filter returns relevant data"""
    end_year = 2000
    response = client.get(
        f"{URL_UNDER_TEST}?end_year={end_year}",
        headers=user_token_headers,
    )
    docs = response.json()
    assert response.status_code == OK
    assert len(docs) == 1
    year1 = parser.parse(docs[0]["publication_ts"]).year
    assert year1 <= end_year
    assert docs[0]["name"] == "doc1"


def test_start_andend_year(client, user_token_headers, doc_browse_data):
    """Test that the start_year and end_year filter returns relevant data"""
    start_year = 2000
    end_year = 2008
    response = client.get(
        f"{URL_UNDER_TEST}?start_year={start_year}&end_year={end_year}",
        headers=user_token_headers,
    )
    docs = response.json()
    assert response.status_code == OK
    assert len(docs) == 1
    year1 = parser.parse(docs[0]["publication_ts"]).year
    assert year1 <= end_year
    assert year1 >= start_year
    assert docs[0]["name"] == "doc2"
