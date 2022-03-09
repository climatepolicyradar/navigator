import enum

import sqlalchemy as sa
from app.db.session import Base
from sqlalchemy import SmallInteger
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship


class DocumentInvalidReason(enum.Enum):
    """Reasons why a document might be invalid."""

    unsupported_content_type = "unsupported_content_type"
    net_ssl_error = "net_ssl_error"
    net_read_error = "net_read_error"
    net_connection_error = "net_connection_error"
    net_too_many_redirects = "net_too_many_redirects"


class Document(Base):  # noqa: D101
    __tablename__ = "document"

    document_id = sa.Column(
        sa.INTEGER(), primary_key=True, autoincrement=True, nullable=False
    )
    action_id = sa.Column(
        sa.INTEGER(), sa.ForeignKey("action.action_id"), nullable=False
    )
    document_date = sa.Column(
        postgresql.TIMESTAMP(), autoincrement=False, nullable=False
    )
    name = sa.Column(sa.VARCHAR(length=255), autoincrement=False, nullable=False)
    source_url = sa.Column(sa.VARCHAR(length=1024), autoincrement=False, nullable=True)
    s3_url = sa.Column(sa.VARCHAR(length=1024), autoincrement=False, nullable=True)
    language_id = sa.Column(
        SmallInteger, sa.ForeignKey("language.language_id"), nullable=True
    )
    document_mod_date = sa.Column(
        postgresql.TIMESTAMP(),
        autoincrement=False,
        nullable=True,
    )
    is_valid = sa.Column(sa.Boolean, nullable=False)
    invalid_reason = sa.Column(sa.Enum(DocumentInvalidReason))

    action = relationship("Action", back_populates="documents")
