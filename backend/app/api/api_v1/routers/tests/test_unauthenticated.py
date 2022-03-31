import datetime
from unittest.mock import patch

from app.core.email import EmailType
from app.db.models import User


@patch("app.api.api_v1.routers.unauthenticated.send_email")
def test_reset_password(
    mock_send_email, client, test_inactive_user, test_db, test_password_reset_token
):
    response = client.post(
        "/api/v1/activations",
        json={
            "token": test_password_reset_token.token,
            "password": "some-password",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "email": test_inactive_user.email,
        "id": test_inactive_user.id,
        "is_active": True,
        "is_superuser": test_inactive_user.is_superuser,
    }

    db_user = test_db.query(User).filter(User.id == test_inactive_user.id).first()
    assert db_user.is_active
    assert db_user.hashed_password is not None

    mock_send_email.assert_called_once_with(EmailType.password_changed, db_user)


@patch("app.api.api_v1.routers.unauthenticated.send_email")
def test_reset_password_nonexistent(
    mock_send_email, client, test_inactive_user, test_db, test_password_reset_token
):
    response = client.post(
        "/api/v1/activations",
        json={
            "token": "some-rubbish",
            "password": "some-password",
        },
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Token not found"

    mock_send_email.assert_not_called()


@patch("app.api.api_v1.routers.unauthenticated.send_email")
def test_reset_password_too_late(
    mock_send_email, client, test_inactive_user, test_db, test_password_reset_token
):
    test_password_reset_token.expiry_ts = datetime.datetime(2010, 1, 1)
    test_db.add(test_password_reset_token)
    test_db.commit()

    response = client.post(
        "/api/v1/activations",
        json={
            "token": test_password_reset_token.token,
            "password": "some-password",
        },
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Token expired"

    mock_send_email.assert_not_called()


@patch("app.api.api_v1.routers.unauthenticated.send_email")
def test_reset_password_used_token(
    mock_send_email, client, test_inactive_user, test_db, test_password_reset_token
):
    test_password_reset_token.is_redeemed = True
    test_db.add(test_password_reset_token)
    test_db.commit()

    response = client.post(
        "/api/v1/activations",
        json={
            "token": test_password_reset_token.token,
            "password": "some-password",
        },
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Token already redeemed"

    mock_send_email.assert_not_called()
