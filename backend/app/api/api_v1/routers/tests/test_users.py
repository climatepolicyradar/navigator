import datetime
from unittest.mock import patch

from app.core.email import EmailType
from app.db.models import User, PasswordResetToken


def test_authenticated_user_me(client, user_token_headers):
    response = client.get("/api/v1/users/me", headers=user_token_headers)
    assert response.status_code == 200


def test_unauthenticated_routes(client):
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401


@patch("app.api.api_v1.routers.users.send_email")
def test_edit_user(mock_send_email, client, test_user, user_token_headers, test_db):
    response = client.put(
        "/api/v1/users/me",
        json={
            "email": test_user.email,
            "names": "New name",
            "is_active": test_user.is_active,  # TODO prevent user from setting these flags
            "is_superuser": test_user.is_superuser,  # TODO prevent user from setting these flags
        },
        headers=user_token_headers,
    )
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["names"] == "New name"

    db_user = test_db.query(User).filter(User.id == test_user.id).first()
    assert db_user.names == "New name"
    mock_send_email.assert_called_once_with(EmailType.account_changed, db_user)


@patch("app.db.crud.user.get_password_reset_token_expiry_ts")
@patch("app.api.api_v1.routers.users.send_email")
def test_password_reset_request(
    mock_send_email,
    mock_get_password_reset_token_expiry_ts,
    client,
    test_user,
    user_token_headers,
    test_db,
):
    mock_get_password_reset_token_expiry_ts.return_value = datetime.datetime(2099, 1, 1)
    response = client.delete(
        "/api/v1/passwords/me",
        headers=user_token_headers,
    )
    assert response.status_code == 200
    assert response.json()

    prt: PasswordResetToken = test_db.query(PasswordResetToken).first()
    assert prt.user_id == 1
    assert prt.expiry_ts == datetime.datetime(2099, 1, 1)
    assert not prt.is_redeemed
    mock_get_password_reset_token_expiry_ts.assert_called_once()

    mock_send_email.assert_called_once_with(
        EmailType.password_reset_requested, test_user, prt
    )
