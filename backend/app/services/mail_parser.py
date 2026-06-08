"""邮件解析服务 - 解析 raw MIME 邮件"""
import email
from email import policy
from email.header import decode_header
from typing import Optional

from app.schemas.inbound import AttachmentMeta, ParsedEmail


def _decode_header_value(value: Optional[str]) -> Optional[str]:
    """解码 MIME 编码的邮件头（如 =?UTF-8?B?...?= ）"""
    if not value:
        return None
    parts = decode_header(value)
    decoded_parts = []
    for part, charset in parts:
        if isinstance(part, bytes):
            decoded_parts.append(part.decode(charset or "utf-8", errors="replace"))
        else:
            decoded_parts.append(part)
    return "".join(decoded_parts)


def _get_body_text(msg: email.message.Message) -> Optional[str]:
    """提取 text/plain 正文"""
    body = msg.get_body(preferencelist=("plain",))
    if body is None:
        return None
    content = body.get_content()
    if isinstance(content, bytes):
        charset = body.get_content_charset() or "utf-8"
        return content.decode(charset, errors="replace")
    return content


def _get_body_html(msg: email.message.Message) -> Optional[str]:
    """提取 text/html 正文"""
    body = msg.get_body(preferencelist=("html",))
    if body is None:
        return None
    content = body.get_content()
    if isinstance(content, bytes):
        charset = body.get_content_charset() or "utf-8"
        return content.decode(charset, errors="replace")
    return content


def _get_attachments(msg: email.message.Message) -> list[AttachmentMeta]:
    """提取附件元数据"""
    attachments = []
    for part in msg.walk():
        content_disposition = part.get("Content-Disposition", "")
        if content_disposition and "attachment" in content_disposition.lower():
            filename = part.get_filename() or "unnamed"
            filename = _decode_header_value(filename) or "unnamed"
            content_type = part.get_content_type()
            payload = part.get_payload(decode=True)
            size = len(payload) if payload else 0
            attachments.append(AttachmentMeta(
                filename=filename,
                content_type=content_type,
                size=size,
            ))
    return attachments


def parse_raw_email(raw_bytes: bytes) -> ParsedEmail:
    """
    解析 raw MIME 邮件字节，返回 ParsedEmail。

    Args:
        raw_bytes: 原始邮件字节（base64 解码后）

    Returns:
        ParsedEmail: 解析后的邮件结构
    """
    msg = email.message_from_bytes(raw_bytes, policy=policy.default)

    subject = _decode_header_value(msg.get("Subject"))
    from_addr = _decode_header_value(msg.get("From"))
    to_addr = _decode_header_value(msg.get("To"))
    cc_addr = _decode_header_value(msg.get("Cc"))
    reply_to = _decode_header_value(msg.get("Reply-To"))

    text_body = _get_body_text(msg)
    html_body = _get_body_html(msg)
    attachments = _get_attachments(msg)

    return ParsedEmail(
        subject=subject,
        **{"from": from_addr},
        to=to_addr,
        cc=cc_addr,
        reply_to=reply_to,
        text_body=text_body,
        html_body=html_body,
        attachments=attachments,
    )
