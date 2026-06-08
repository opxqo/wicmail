"""邮箱模型 - 共享 mailboxes 表 + 新建 mailbox_applications 表"""
from __future__ import annotations

from datetime import datetime
from typing import Optional, List

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Mailbox(Base):
    """共享的邮箱表（backend-mail 也读写此表）"""
    __tablename__ = "mailboxes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    display_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    messages: Mapped[List["EmailMessage"]] = relationship(back_populates="mailbox")


class MailboxApplication(Base):
    """邮箱申请表（backend-wic 专用）"""
    __tablename__ = "mailbox_applications"
    __table_args__ = (
        Index("ix_mailbox_app_user", "user_id"),
        Index("ix_mailbox_app_status", "status"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    requested_address: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    display_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending/approved/rejected
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # 审核信息
    reviewed_by: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    review_comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # 批准后的邮箱 ID
    mailbox_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("mailboxes.id"), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # 关系
    user: Mapped["User"] = relationship("User", foreign_keys=[user_id])
    reviewer: Mapped[Optional["User"]] = relationship("User", foreign_keys=[reviewed_by])
    mailbox: Mapped[Optional["Mailbox"]] = relationship("Mailbox")
