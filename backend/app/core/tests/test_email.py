import os
from dataclasses import dataclass
from unittest.mock import patch, MagicMock

from sendgrid.helpers.mail import Mail

from app.core.email import (
    _send_email,
    send_new_account_email,
    send_password_changed_email,
    send_password_reset_email,
    _SENDGRID_NEW_ACCOUNT_TEMPLATE_ID,
    _SENDGRID_FROM_ENV,
    _SENDGRID_PASSWORD_CHANGED_TEMPLATE_ID,
    _SENDGRID_PASSWORD_RESET_TEMPLATE_ID,
    _LINK_BASE_ENV,
)


@patch("app.core.email._SENDGRID")
@patch("app.core.email._SENDGRID_ENABLED", True)
def test_sendgrid_enabled(sendgrid_mock):
    mock_mail = MagicMock(spec=Mail)
    mock_mail.get.return_value = {}

    _send_email(mock_mail)

    assert sendgrid_mock.send.called_once_with({})


@patch("app.core.email._SENDGRID")
@patch("app.core.email._SENDGRID_ENABLED", False)
def test_sendgrid_disabled(sendgrid_mock):
    mock_mail = MagicMock(spec=Mail)
    mock_mail.get.return_value = {}

    _send_email(mock_mail)

    assert not sendgrid_mock.send.called


@dataclass
class _MockUser:
    names: str
    email: str


@dataclass
class _MockToken:
    token: str


@patch.dict(
    os.environ,
    {
        _LINK_BASE_ENV: "http://example.org",
        _SENDGRID_FROM_ENV: "agent@example.org",
    },
)
@patch("app.core.email.Mail")
@patch("app.core.email._send_email")
def test_activation_template(mock_send, mock_mail):
    mocked_mail_instance = MagicMock(spec=Mail)
    mock_mail.return_value = mocked_mail_instance
    send_new_account_email(
        user=_MockUser(names="Barry Chuckle", email="barry@chuckle.bros"),  # type: ignore
        activation_token=_MockToken(token="HelloBarry"),  # type: ignore
    )

    assert (
        mocked_mail_instance.template_id.template_id
        == _SENDGRID_NEW_ACCOUNT_TEMPLATE_ID
    )
    assert mocked_mail_instance.to.email == "barry@chuckle.bros"
    assert mocked_mail_instance.to.name == "Barry Chuckle"
    assert mocked_mail_instance.from_email.email == "agent@example.org"
    assert (
        mocked_mail_instance.dynamic_template_data.dynamic_template_data["name"]
        == "Barry Chuckle"
    )
    assert (
        mocked_mail_instance.dynamic_template_data.dynamic_template_data["link"]
        == "http://example.org/auth/activate-account?token=HelloBarry"
    )
    assert mocked_mail_instance.from_email.email == "agent@example.org"

    assert mock_send.called_with(mocked_mail_instance)


@patch.dict(
    os.environ,
    {
        _LINK_BASE_ENV: "http://example.org",
        _SENDGRID_FROM_ENV: "agent@example.org",
    },
)
@patch("app.core.email.Mail")
@patch("app.core.email._send_email")
def test_reset_template(mock_send, mock_mail):
    mocked_mail_instance = MagicMock(spec=Mail)
    mock_mail.return_value = mocked_mail_instance
    send_password_reset_email(
        user=_MockUser(names="Barry Chuckle", email="barry@chuckle.bros"),  # type: ignore
        reset_token=_MockToken(token="HelloBarry"),  # type: ignore
    )

    assert (
        mocked_mail_instance.template_id.template_id
        == _SENDGRID_PASSWORD_RESET_TEMPLATE_ID
    )
    assert mocked_mail_instance.to.email == "barry@chuckle.bros"
    assert mocked_mail_instance.to.name == "Barry Chuckle"
    assert mocked_mail_instance.from_email.email == "agent@example.org"
    assert (
        mocked_mail_instance.dynamic_template_data.dynamic_template_data["name"]
        == "Barry Chuckle"
    )
    assert (
        mocked_mail_instance.dynamic_template_data.dynamic_template_data["link"]
        == "http://example.org/auth/reset-password?token=HelloBarry"
    )
    assert mocked_mail_instance.from_email.email == "agent@example.org"

    assert mock_send.called_with(mocked_mail_instance)


@patch.dict(
    os.environ,
    {
        _LINK_BASE_ENV: "http://example.org",
        _SENDGRID_FROM_ENV: "agent@example.org",
    },
)
@patch("app.core.email.Mail")
@patch("app.core.email._send_email")
def test_changed_template(mock_send, mock_mail):
    mocked_mail_instance = MagicMock(spec=Mail)
    mock_mail.return_value = mocked_mail_instance
    send_password_changed_email(
        user=_MockUser(names="Barry Chuckle", email="barry@chuckle.bros"),  # type: ignore
    )

    assert (
        mocked_mail_instance.template_id.template_id
        == _SENDGRID_PASSWORD_CHANGED_TEMPLATE_ID
    )
    assert mocked_mail_instance.to.email == "barry@chuckle.bros"
    assert mocked_mail_instance.to.name == "Barry Chuckle"
    assert mocked_mail_instance.from_email.email == "agent@example.org"
    assert (
        mocked_mail_instance.dynamic_template_data.dynamic_template_data["name"]
        == "Barry Chuckle"
    )
    assert mocked_mail_instance.from_email.email == "agent@example.org"

    assert mock_send.called_with(mocked_mail_instance)
