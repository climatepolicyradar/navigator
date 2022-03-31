import enum


class EmailType(enum.Enum):  # noqa: D101
    account_new = "account_new"
    account_changed = "account_changed"
    password_changed = "password_changed"  # "your password changed. If this wasn't you, contact support, blah blah"
    password_reset_requested = "password_reset_requested"


def send_email(type: EmailType, *args, **kwargs):
    # TODO implement
    pass
