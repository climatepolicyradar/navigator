import datetime
from unittest.mock import patch

from app.db.models import User, PasswordResetToken
from app.api.api_v1.routers.admin import ACCOUNT_ACTIVATION_EXPIRE_MINUTES


def test_get_users(client, test_superuser, superuser_token_headers):
    response = client.get("/api/v1/admin/users", headers=superuser_token_headers)
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": test_superuser.id,
            "email": test_superuser.email,
            "is_active": test_superuser.is_active,
            "is_superuser": test_superuser.is_superuser,
        }
    ]
    assert response.headers.get("Cache-Control") == "no-cache, no-store, private"


def test_deactivate_user(client, test_superuser, test_db, superuser_token_headers):
    response = client.delete(
        f"/api/v1/admin/users/{test_superuser.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": test_superuser.id,
        "email": test_superuser.email,
        "is_active": False,
        "is_superuser": test_superuser.is_superuser,
    }

    user_in_db = test_db.query(User).first()
    assert not user_in_db.is_active


def test_delete_user_not_found(client, superuser_token_headers):
    response = client.delete(
        "/api/v1/admin/users/4321", headers=superuser_token_headers
    )
    assert response.status_code == 404


# TODO: re-enable when account updated email is available
# @patch("app.api.api_v1.routers.admin.send_email")
def test_edit_user(client, test_superuser, superuser_token_headers):
    new_user = {
        "email": "newemail@email.com",
        "is_active": False,
        "is_superuser": True,
        "names": "Joe Smith",
    }

    response = client.put(
        f"/api/v1/admin/users/{test_superuser.id}",
        json=new_user,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    new_user["id"] = test_superuser.id
    assert response.json() == new_user
    assert response.headers.get("Cache-Control") == "no-cache, no-store, private"
    # mock_send_email.assert_called_with(EmailType.account_changed, test_superuser)


# TODO: re-enable when account updated email is available
# @patch("app.api.api_v1.routers.admin.send_email")
def test_edit_other_user(
    client,
    superuser_token_headers,
    test_user,
):
    old_is_active = test_user.is_active

    response = client.put(
        f"/api/v1/admin/users/{test_user.id}",
        json={
            "email": test_user.email,
            "is_active": not test_user.is_active,
        },
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert test_user.is_active is not old_is_active
    assert response.headers.get("Cache-Control") == "no-cache, no-store, private"
    # mock_send_email.assert_called_with(EmailType.account_changed, test_user)


def test_edit_user_not_found(client, superuser_token_headers):
    new_user = {
        "email": "newemail@email.com",
        "is_active": False,
        "is_superuser": False,
        "password": "new_password",
    }
    response = client.put(
        "/api/v1/admin/users/1234",
        json=new_user,
        headers=superuser_token_headers,
    )
    assert response.status_code == 404


def test_get_user(
    client,
    test_user,
    superuser_token_headers,
):
    response = client.get(
        f"/api/v1/admin/users/{test_user.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": test_user.id,
        "email": test_user.email,
        "is_active": bool(test_user.is_active),
        "is_superuser": test_user.is_superuser,
    }
    assert response.headers.get("Cache-Control") == "no-cache, no-store, private"


def test_user_not_found(client, superuser_token_headers):
    response = client.get("/api/v1/admin/users/123", headers=superuser_token_headers)
    assert response.status_code == 404


def test_unauthenticated_routes(client):
    response = client.get("/api/v1/admin/users")
    assert response.status_code == 401
    response = client.get("/api/v1/admin/users/123")
    assert response.status_code == 401
    response = client.put("/api/v1/admin/users/123")
    assert response.status_code == 401
    response = client.delete("/api/v1/admin/users/123")
    assert response.status_code == 401


def test_unauthorized_routes(client, user_token_headers):
    response = client.get("/api/v1/admin/users", headers=user_token_headers)
    assert response.status_code == 404
    response = client.get("/api/v1/admin/users/123", headers=user_token_headers)
    assert response.status_code == 404


@patch("app.db.crud.password_reset.get_password_reset_token_expiry_ts")
@patch("app.api.api_v1.routers.admin.send_new_account_email")
def test_create_user(
    mock_send_email,
    mock_get_password_reset_token_expiry_ts,
    client,
    superuser_token_headers,
    test_db,
):
    mock_get_password_reset_token_expiry_ts.return_value = datetime.datetime(2099, 1, 1)
    new_user = {
        "email": "newemail@email.com",
        "is_active": False,
        "is_superuser": True,
        "names": "Joe Smith",
        "password": "new_password",
    }

    response = client.post(
        "/api/v1/admin/users",
        json=new_user,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 2,
        "is_active": False,
        "is_superuser": True,
        "names": new_user["names"],
        "email": new_user["email"],
    }

    prt: PasswordResetToken = test_db.query(PasswordResetToken).first()
    assert prt.user_id == 2
    assert prt.expiry_ts == datetime.datetime(2099, 1, 1)
    assert not prt.is_redeemed
    mock_get_password_reset_token_expiry_ts.assert_called_once_with(
        minutes=ACCOUNT_ACTIVATION_EXPIRE_MINUTES
    )

    db_user = test_db.query(User).filter(User.id == 2).first()
    mock_send_email.assert_called_once_with(db_user, prt)


@patch("app.db.crud.password_reset.get_password_reset_token_expiry_ts")
@patch("app.api.api_v1.routers.admin.send_password_reset_email")
def test_reset_password(
    mock_send_email,
    mock_get_password_reset_token_expiry_ts,
    client,
    superuser_token_headers,
    test_db,
    test_user,
):
    mock_get_password_reset_token_expiry_ts.return_value = datetime.datetime(2099, 1, 1)

    response = client.post(
        f"/api/v1/admin/password-reset/{test_user.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert response.json()

    prt: PasswordResetToken = test_db.query(PasswordResetToken).first()
    assert prt.user_id == test_user.id
    assert prt.expiry_ts == datetime.datetime(2099, 1, 1)
    assert not prt.is_redeemed
    assert not prt.is_cancelled

    mock_send_email.assert_called_with(test_user, prt)

    # initiating a new request will cancel the existing token, create a new token, and send a new email
    response = client.post(
        f"/api/v1/admin/password-reset/{test_user.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert response.json()

    prt_old: PasswordResetToken = (
        test_db.query(PasswordResetToken)
        .filter(PasswordResetToken.id == prt.id)
        .first()
    )
    assert prt_old.is_cancelled

    prt_new: PasswordResetToken = (
        test_db.query(PasswordResetToken)
        .filter(PasswordResetToken.id == prt.id + 1)
        .first()
    )
    assert prt_new.user_id == test_user.id
    assert prt_new.expiry_ts == datetime.datetime(2099, 1, 1)
    assert not prt_new.is_redeemed
    assert not prt_new.is_cancelled

    assert mock_get_password_reset_token_expiry_ts.call_count == 2
    mock_send_email.assert_called_with(test_user, prt_new)
    assert mock_send_email.call_count == 2
