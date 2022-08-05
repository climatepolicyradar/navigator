# TODO: re-enable when we have account updated email
# from unittest.mock import patch

from app.db.models import User


def test_authenticated_user_me(client, user_token_headers):
    response = client.get("/api/v1/users/me", headers=user_token_headers)
    assert response.status_code == 200
    assert response.headers.get("Cache-Control") == "no-cache, no-store, private"


def test_unauthenticated_routes(client):
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401


# TODO: re-enable when we have account updated email
# @patch("app.api.api_v1.routers.users.send_email")
def test_edit_user(client, test_user, user_token_headers, test_db):
    response = client.put(
        "/api/v1/users/me",
        json={
            "email": test_user.email,
            "names": "New name",
            "is_active": not test_user.is_active,  # will be ignored
            "is_superuser": not test_user.is_superuser,  # will be ignored
            "affiliation_organisation": "org",
            "affiliation_type": ["type 1", "type 2"],
        },
        headers=user_token_headers,
    )
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["names"] == "New name"

    db_user = test_db.query(User).filter(User.id == test_user.id).first()
    assert db_user.names == "New name"
    assert db_user.is_active == test_user.is_active  # original value maintained
    assert db_user.is_superuser == test_user.is_superuser  # original value maintained
    assert db_user.affiliation_organisation == "org"
    assert db_user.affiliation_type == ["type 1", "type 2"]
    assert response.headers.get("Cache-Control") == "no-cache, no-store, private"
    # mock_send_email.assert_called_once_with(EmailType.account_changed, db_user)
