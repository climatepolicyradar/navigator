import datetime
from unittest.mock import patch

from app.db.models import User, PasswordResetToken


@patch("app.api.api_v1.routers.unauthenticated.send_password_changed_email")
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

    mock_send_email.assert_called_once_with(db_user)


@patch("app.api.api_v1.routers.unauthenticated.send_password_changed_email")
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


@patch("app.api.api_v1.routers.unauthenticated.send_password_changed_email")
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


@patch("app.api.api_v1.routers.unauthenticated.send_password_changed_email")
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


@patch("app.api.api_v1.routers.unauthenticated.send_password_changed_email")
def test_reset_password_cancelled_token(
    mock_send_email, client, test_inactive_user, test_db, test_password_reset_token
):
    test_password_reset_token.is_cancelled = True
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
    assert response.json()["detail"] == "Token is not valid"

    mock_send_email.assert_not_called()


@patch("app.db.crud.password_reset.get_password_reset_token_expiry_ts")
@patch("app.api.api_v1.routers.unauthenticated.send_password_reset_email")
def test_password_reset_request(
    mock_send_email,
    mock_get_password_reset_token_expiry_ts,
    client,
    test_user,
    test_db,
    test_password_reset_token,
):
    # Start with an old token from account creation (should not be returned as valid)
    test_password_reset_token.expiry_ts = (
        datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    )
    test_password_reset_token.user_id = test_user.id
    test_db.commit()

    mock_get_password_reset_token_expiry_ts.return_value = datetime.datetime(2099, 1, 1)
    response = client.post(
        f"/api/v1/password-reset/{test_user.email}",
    )
    assert response.status_code == 200
    assert response.json()

    # Make sure we've removed old stale tokens
    assert len(test_db.query(PasswordResetToken).all()) == 1

    # Validate that the token we received is what we expected
    prt: PasswordResetToken = test_db.query(PasswordResetToken).first()
    assert prt.user_id == 1
    assert prt.expiry_ts == datetime.datetime(2099, 1, 1)
    assert not prt.is_redeemed
    mock_get_password_reset_token_expiry_ts.assert_called_once_with(minutes=None)

    mock_send_email.assert_called_once_with(test_user, prt)

    # Make sure we don't regenerate reset tokens unnecessarily
    response = client.post(
        f"/api/v1/password-reset/{test_user.email}",
    )
    assert response.status_code == 200
    assert response.json()

    assert prt == test_db.query(PasswordResetToken).first()
    assert mock_send_email.call_count == 2  # resend reset email

    # calling it more in quick succession limits the rate
    # i = 0,1,2,3 plus the original 2 calls in this test = 6
    # i = 4 is the seventh call, which will be limited
    for i in range(4):
        response = client.post(
            f"/api/v1/password-reset/{test_user.email}",
        )
        if i < 4:
            assert response.status_code == 200
            assert response.json()
        else:
            assert response.status_code == 429
