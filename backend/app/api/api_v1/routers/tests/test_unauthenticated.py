import datetime
from unittest.mock import patch

import pytest

from app.api.api_v1.routers.admin import ACCOUNT_ACTIVATION_EXPIRE_MINUTES
from app.core.security import verify_password
from app.db.models import User, PasswordResetToken
from app.api.api_v1.routers.unauthenticated import limiter


@pytest.mark.parametrize(
    "password", ["simple-password", "ManyClas5es$", "dodgy%23encode"]
)
@patch("app.api.api_v1.routers.unauthenticated.send_password_changed_email")
def test_reset_password(
    mock_send_email,
    password,
    client,
    test_inactive_user,
    test_db,
    test_password_reset_token,
):
    # reset the rate limiter so we do not see unexpected 429 responses
    limiter.reset()
    response = client.post(
        "/api/v1/activations",
        json={
            "token": test_password_reset_token.token,
            "password": password,
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
    assert verify_password(password, db_user.hashed_password)

    mock_send_email.assert_called_once_with(db_user)


@patch("app.api.api_v1.routers.unauthenticated.send_password_changed_email")
def test_reset_password_nonexistent(
    mock_send_email, client, test_inactive_user, test_db, test_password_reset_token
):
    # reset the rate limiter so we do not see unexpected 429 responses
    limiter.reset()
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
    # reset the rate limiter so we do not see unexpected 429 responses
    limiter.reset()
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
    # reset the rate limiter so we do not see unexpected 429 responses
    limiter.reset()
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
    # reset the rate limiter so we do not see unexpected 429 responses
    limiter.reset()
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
def test_password_reset_after_activation(
    mock_send_email,
    mock_get_password_reset_token_expiry_ts,
    client,
    test_user,
    test_db,
    test_password_reset_token,
):
    # reset the rate limiter so we do not see unexpected 429 responses
    limiter.reset()
    # Start with an old token from account creation (should not be returned as valid)
    test_password_reset_token.expiry_ts = (
        datetime.datetime.utcnow() + datetime.timedelta(minutes=500)
    )
    test_password_reset_token.user_id = test_user.id
    test_password_reset_token.is_redeemed = True
    test_db.commit()

    mock_get_password_reset_token_expiry_ts.return_value = datetime.datetime(2099, 1, 1)
    response = client.post(
        f"/api/v1/password-reset/{test_user.email}",
    )
    assert response.status_code == 200
    assert response.json()

    # Make sure we've removed redeemed tokens
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


@patch("app.db.crud.password_reset.get_password_reset_token_expiry_ts")
@patch("app.api.api_v1.routers.unauthenticated.send_password_reset_email")
def test_password_reset_active_token_too_close_to_expiry(
    mock_send_email,
    mock_get_password_reset_token_expiry_ts,
    client,
    test_user,
    test_db,
    test_password_reset_token,
):
    # reset the rate limiter so we do not see unexpected 429 responses
    limiter.reset()
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

    # Make sure we've removed tokens with too little life left
    assert len(test_db.query(PasswordResetToken).all()) == 1

    # Validate that the token we received is what we expected
    prt: PasswordResetToken = test_db.query(PasswordResetToken).first()
    assert prt.user_id == 1
    assert prt.expiry_ts == datetime.datetime(2099, 1, 1)
    assert not prt.is_redeemed
    mock_get_password_reset_token_expiry_ts.assert_called_once_with(minutes=None)
    mock_send_email.assert_called_once_with(test_user, prt)


def test_password_reset_rate_limit(
    client,
    test_user,
    test_db,
):
    # reset the rate limiter so we do not see unexpected 429 responses
    limiter.reset()

    # Make sure we rate limit requests
    max_requests_per_minute = 6
    for i in range(max_requests_per_minute + 2):
        response = client.post(
            f"/api/v1/password-reset/{test_user.email}",
        )
        if i < max_requests_per_minute:
            assert response.status_code == 200
            assert response.json()
        else:
            assert response.status_code == 429

    # Just make sure we're not polluting the db with extra tokens
    assert len(test_db.query(PasswordResetToken).all()) == 1


NEW_USER_1 = {
    "email": "newemail1@email.com",
    "names": "Joe Smith 1",
    "password": "new_password1",
}
NEW_USER_2 = {
    "email": "newemail2@email.com",
    "is_active": True,
    "is_superuser": True,
    "names": "Joe Smith 2",
    "password": "new_password2",
}


@pytest.mark.parametrize("new_user", [NEW_USER_1, NEW_USER_2])
@patch("app.db.crud.password_reset.get_password_reset_token_expiry_ts")
@patch("app.api.api_v1.routers.unauthenticated.send_new_account_email")
@patch("app.api.api_v1.routers.unauthenticated.ENABLE_SELF_REGISTRATION", True)
def test_register_user(
    mock_send_email,
    mock_get_password_reset_token_expiry_ts,
    new_user,
    client,
    test_db,
    test_user,
):
    # reset the rate limiter so we do not see unexpected 429 responses
    limiter.reset()

    mock_get_password_reset_token_expiry_ts.return_value = datetime.datetime(2099, 1, 1)

    response = client.post(
        "/api/v1/registrations",
        json=new_user,
    )
    assert response.status_code == 200
    assert response.json() is True

    prt: PasswordResetToken = test_db.query(PasswordResetToken).first()
    assert prt.user_id == 2
    assert prt.expiry_ts == datetime.datetime(2099, 1, 1)
    assert not prt.is_redeemed
    mock_get_password_reset_token_expiry_ts.assert_called_once_with(
        minutes=ACCOUNT_ACTIVATION_EXPIRE_MINUTES
    )

    db_user = test_db.query(User).filter(User.id == 2).first()
    # No matter what settings were requested, active/superuser should be ignored
    assert not db_user.is_active
    assert not db_user.is_superuser
    mock_send_email.assert_called_once_with(db_user, prt)


@pytest.mark.parametrize("new_user", [NEW_USER_1, NEW_USER_2])
@patch("app.api.api_v1.routers.unauthenticated.ENABLE_SELF_REGISTRATION", False)
def test_register_user_disabled(
    new_user,
    client,
    test_db,
    test_user,
):
    # reset the rate limiter so we do not see unexpected 429 responses
    limiter.reset()

    response = client.post(
        "/api/v1/registrations",
        json=new_user,
    )
    assert response.status_code == 405
    assert response.json() == {"detail": "User registration is disabled"}
