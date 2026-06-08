"""邮件模型 - 引用共享的 email_messages 和 attachments 表"""
from __future__ import annotations

from datetime import datetime
from typing import Optional, List, Dict

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, JSON, Index
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class EmailMessage(Base):
    __tablename__ = "email_messages"
    __table_args__ = (
        Index("ix_email_messages_mailbox_received", "mailbox_id", "received_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    mailbox_id: Mapped[int] = mapped_column(Integer, ForeignKey("mailboxes.id"), nullable=False)
    request_id: Mapped[str] = mapped_column(String(255), nullable=False)
    message_id: Mapped[Optional[str]] = mapped_column(String(512), nullable=True, index=True)
    raw_sha256: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)

    envelope_from: Mapped[str] = mapped_column(String(255), nullable=False)
    envelope_to: Mapped[str] = mapped_column(String(255), nullable=False)
    header_from: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    header_to: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    header_cc: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    header_reply_to: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)

    subject: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    received_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    raw_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    raw_too_large: Mapped[bool] = mapped_column(Boolean, default=False)
    headers_json: Mapped[Optional[Dict]] = mapped_column(JSON, nullable=True)

    body_text: Mapped[Optional[str]] = mapped_column(LONGTEXT, nullable=True)
    body_html: Mapped[Optional[str]] = mapped_column(LONGTEXT, nullable=True)

    parse_status: Mapped[str] = mapped_column(String(20), default="received")
    parse_error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    mailbox: Mapped["Mailbox"] = relationship("Mailbox", back_populates="messages")
    attachments: Mapped[List["Attachment"]] = relationship(back_populates="email_message")


class Attachment(Base):
    __tablename__ = "attachments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email_id: Mapped[int] = mapped_column(Integer, ForeignKey("email_messages.id"), nullable=False, index=True)
    filename: Mapped[str] = mapped_column(String(500), nullable=False)
    content_type: Mapped[str] = mapped_column(String(255), nullable=False)
    size: Mapped[int] = mapped_column(Integer, nullable=False)
    storage_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    storage_backend: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    content_sha256: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    is_inline: Mapped[bool] = mapped_column(Boolean, default=False)
    content_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    email_message: Mapped["EmailMessage"] = relationship(back_populates="attachments")
