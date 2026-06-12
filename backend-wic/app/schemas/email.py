"""邮件响应模型"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class AttachmentOut(BaseModel):
    id: int
    filename: str
    content_type: str
    size: int

    model_config = {"from_attributes": True}


class EmailSummary(BaseModel):
    id: int
    mailbox_address: Optional[str] = None
    subject: Optional[str] = None
    header_from: Optional[str] = None
    header_to: Optional[str] = None
    envelope_from: str
    envelope_to: str
    received_at: Optional[datetime] = None
    is_read: bool = False
    attachment_count: int = 0

    model_config = {"from_attributes": True}


class EmailDetail(BaseModel):
    id: int
    mailbox_address: Optional[str] = None
    subject: Optional[str] = None
    header_from: Optional[str] = None
    header_to: Optional[str] = None
    header_cc: Optional[str] = None
    header_reply_to: Optional[str] = None
    envelope_from: str
    envelope_to: str
    message_id: Optional[str] = None
    sent_at: Optional[datetime] = None
    received_at: Optional[datetime] = None
    raw_size: Optional[int] = None
    body_text: Optional[str] = None
    body_html: Optional[str] = None
    parse_status: str
    is_read: bool = False
    attachments: List[AttachmentOut] = []

    model_config = {"from_attributes": True}


class EmailListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    emails: List[EmailSummary]


class UnreadCountResponse(BaseModel):
    unread_count: int
