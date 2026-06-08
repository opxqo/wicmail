from typing import Any, Optional
from pydantic import BaseModel, Field


class CloudflareInboundEmail(BaseModel):
    """Cloudflare Email Worker 推送的邮件 payload"""
    source: Optional[str] = None
    worker_version: Optional[str] = None
    request_id: str

    envelope_from: str
    envelope_to: str

    header_from: Optional[str] = None
    header_to: Optional[str] = None
    header_cc: Optional[str] = None
    header_reply_to: Optional[str] = None

    subject: Optional[str] = None
    message_id: Optional[str] = None
    date: Optional[str] = None

    headers: dict[str, Any] = Field(default_factory=dict)

    raw_size: Optional[int] = None
    raw: Optional[str] = None
    raw_encoding: Optional[str] = None
    raw_sha256: Optional[str] = None
    raw_too_large: bool = False

    received_at: Optional[str] = None


class AttachmentMeta(BaseModel):
    """附件元数据"""
    filename: str
    content_type: str
    size: int


class ParsedEmail(BaseModel):
    """解析后的邮件内容"""
    subject: Optional[str] = None
    from_: Optional[str] = Field(None, alias="from")
    to: Optional[str] = None
    cc: Optional[str] = None
    reply_to: Optional[str] = None
    text_body: Optional[str] = None
    html_body: Optional[str] = None
    attachments: list[AttachmentMeta] = Field(default_factory=list)

    model_config = {"populate_by_name": True}


class InboundResponse(BaseModel):
    """入站接口返回格式"""
    status: str
    request_id: str
    raw_too_large: bool = False
    parsed: Optional[ParsedEmail] = None
