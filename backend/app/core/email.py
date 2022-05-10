import logging
import os
from typing import Optional

from python_http_client.client import Response
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import DynamicTemplateData, From, Mail, TemplateId, To

from app.db.models import User, PasswordResetToken

_LOGGER = logging.getLogger(__name__)

_SENDGRID_FROM_ENV = "SENDGRID_FROM_EMAIL"
_LINK_BASE_ENV = "PUBLIC_APP_URL"

if _SENDGRID_FROM_ENV not in os.environ:
    _LOGGER.error(
        "Sent emails will not be configured correctly and may fail "
        f"because {_SENDGRID_FROM_ENV} is not set."
    )

if _LINK_BASE_ENV not in os.environ:
    _LOGGER.error(
        f"Email contents will not contain valid links because {_LINK_BASE_ENV} is "
        "not set."
    )

_SENDGRID_ENABLED: bool = os.getenv("SENDGRID_ENABLED", "False").lower() == "true"
_SENDGRID = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))

_SENDGRID_NEW_ACCOUNT_TEMPLATE_ID = "d-b3be8dbb3946456da225a02e0081087a"
_SENDGRID_PASSWORD_CHANGED_TEMPLATE_ID = "d-c83af83f157d4bf6af82d8cbbce386e8"
_SENDGRID_PASSWORD_RESET_TEMPLATE_ID = "d-85d7a1be19bb40bea2d80783fe2d1be3"

# TODO: account updated emails
# _SENDGRID_ACCOUNT_UPDATED_TEMPLATE_ID = None


def _get_auth_link(action: str, activation_token: PasswordResetToken) -> str:
    base_url = os.environ[_LINK_BASE_ENV].rstrip("/")
    activation_url = f"{base_url}/auth/{action}"
    return f"{activation_url}?token={activation_token.token}"


def _get_email_base(user: User, template_id: TemplateId) -> Mail:
    mail = Mail()
    mail.to = To(
        email=user.email,
        name=user.names,
    )
    mail.from_email = From(email=os.environ[_SENDGRID_FROM_ENV])
    mail.template_id = template_id
    return mail


def _send_email(mail: Mail) -> Optional[Response]:
    if _SENDGRID_ENABLED:
        return _SENDGRID.send(message=mail)

    _LOGGER.info("Not sending email because sendgrid is disabled by env var")
    return None


def send_new_account_email(user: User, activation_token: PasswordResetToken) -> None:
    mail = _get_email_base(
        user,
        template_id=TemplateId(_SENDGRID_NEW_ACCOUNT_TEMPLATE_ID),
    )
    mail.dynamic_template_data = DynamicTemplateData(
        dynamic_template_data={
            "name": user.names,
            "link": _get_auth_link("activate-account", activation_token),
        },
    )
    _send_email(mail)


def send_password_reset_email(user: User, reset_token: PasswordResetToken) -> None:
    mail = _get_email_base(
        user,
        template_id=TemplateId(_SENDGRID_PASSWORD_RESET_TEMPLATE_ID),
    )
    mail.dynamic_template_data = DynamicTemplateData(
        dynamic_template_data={
            "name": user.names,
            "link": _get_auth_link("reset-password", reset_token),
        },
    )
    _send_email(mail)


def send_password_changed_email(user: User) -> None:
    mail = _get_email_base(
        user,
        template_id=TemplateId(_SENDGRID_PASSWORD_CHANGED_TEMPLATE_ID),
    )
    mail.dynamic_template_data = DynamicTemplateData(
        dynamic_template_data={"name": user.names},
    )
    _send_email(mail)
