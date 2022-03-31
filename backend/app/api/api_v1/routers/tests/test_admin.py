import datetime

from app.core.email import EmailType
from app.db.models import User, PasswordResetToken
from unittest.mock import patch


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


def test_deactivate_user(client, test_superuser, test_db, superuser_token_headers):
    response = client.delete(
        f"/api/v1/admin/users/{test_superuser.id}", headers=superuser_token_headers
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


def test_edit_user_not_found(client, test_db, superuser_token_headers):
    new_user = {
        "email": "newemail@email.com",
        "is_active": False,
        "is_superuser": False,
        "password": "new_password",
    }
    response = client.put(
        "/api/v1/admin/users/1234", json=new_user, headers=superuser_token_headers
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
    assert response.status_code == 403
    response = client.get("/api/v1/admin/users/123", headers=user_token_headers)
    assert response.status_code == 403


@patch("app.db.crud.user.get_password_reset_token_expiry_ts")
@patch("app.api.api_v1.routers.admin.send_email")
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
    mock_get_password_reset_token_expiry_ts.assert_called_once()

    db_user = test_db.query(User).filter(User.id == 2).first()
    mock_send_email.assert_called_once_with(EmailType.account_new, db_user, prt)


@patch("app.db.crud.user.get_password_reset_token_expiry_ts")
@patch("app.api.api_v1.routers.admin.send_email")
def test_reset_password(
    mock_send_email,
    mock_get_password_reset_token_expiry_ts,
    client,
    superuser_token_headers,
    test_db,
    test_user,
):
    mock_get_password_reset_token_expiry_ts.return_value = datetime.datetime(2099, 1, 1)

    response = client.delete(
        f"/api/v1/admin/passwords/{test_user.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert response.json()

    prt: PasswordResetToken = test_db.query(PasswordResetToken).first()
    assert prt.user_id == test_user.id
    assert prt.expiry_ts == datetime.datetime(2099, 1, 1)
    assert not prt.is_redeemed
    mock_get_password_reset_token_expiry_ts.assert_called_once()

    mock_send_email.assert_called_once_with(
        EmailType.password_reset_requested, test_user, prt
    )
