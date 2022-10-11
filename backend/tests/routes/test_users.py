# TODO: re-enable when we have account updated email
# from unittest.mock import patch


def test_authenticated_user_me(client):
    response = client.get(
        "/api/v1/users/me",
    )
    assert response.status_code == 401


def test_unauthenticated_routes(client):
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401


# TODO: re-enable when we have account updated email
# @patch("app.api.api_v1.routers.users.send_email")
def test_edit_user(client, test_user, test_db):
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
    )
    assert response.status_code == 401
