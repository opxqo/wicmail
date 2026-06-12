"""邮件入库服务"""
from datetime import datetime
from typing import Optional, Tuple

from email.utils import parsedate_to_datetime
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.email import Mailbox, EmailMessage, Attachment
from app.schemas.inbound import CloudflareInboundEmail, ParsedEmail


async def get_or_create_mailbox(
    session: AsyncSession, address: str
) -> Mailbox:
    """获取或创建邮箱"""
    result = await session.execute(
        select(Mailbox).where(Mailbox.address == address)
    )
    mailbox = result.scalar_one_or_none()

    if mailbox is None:
        mailbox = Mailbox(address=address, is_active=True)
        session.add(mailbox)
        await session.flush()

    return mailbox


def parse_sent_at(date_str: Optional[str]) -> Optional[datetime]:
    """解析邮件日期头为 datetime"""
    if not date_str:
        return None
    try:
        return parsedate_to_datetime(date_str)
    except Exception:
        return None


async def save_inbound_email(
    session: AsyncSession,
    payload: CloudflareInboundEmail,
    parsed: Optional[ParsedEmail] = None,
    parse_error: Optional[str] = None,
) -> Tuple[EmailMessage, bool]:
    """
    保存入站邮件到数据库。

    Returns:
        (EmailMessage, is_new): 邮件记录和是否为新插入
    """
    # 先获取或创建邮箱
    mailbox = await get_or_create_mailbox(session, payload.envelope_to)

    # 去重检查：mailbox_id + raw_sha256
    if payload.raw_sha256:
        result = await session.execute(
            select(EmailMessage).where(
                and_(
                    EmailMessage.mailbox_id == mailbox.id,
                    EmailMessage.raw_sha256 == payload.raw_sha256,
                )
            )
        )
        existing = result.scalar_one_or_none()
        if existing:
            return existing, False

    # 去重检查：mailbox_id + message_id（非空时）
    if payload.message_id:
        result = await session.execute(
            select(EmailMessage).where(
                and_(
                    EmailMessage.mailbox_id == mailbox.id,
                    EmailMessage.message_id == payload.message_id,
                )
            )
        )
        existing = result.scalar_one_or_none()
        if existing:
            return existing, False

    # 创建邮件记录
    email_msg = EmailMessage(
        mailbox_id=mailbox.id,
        request_id=payload.request_id,
        message_id=payload.message_id,
        raw_sha256=payload.raw_sha256,
        envelope_from=payload.envelope_from,
        envelope_to=payload.envelope_to,
        header_from=parsed.from_ if parsed else payload.header_from,
        header_to=parsed.to if parsed else payload.header_to,
        header_cc=parsed.cc if parsed else payload.header_cc,
        header_reply_to=parsed.reply_to if parsed else payload.header_reply_to,
        subject=parsed.subject if parsed else payload.subject,
        sent_at=parse_sent_at(payload.date),
        raw_size=payload.raw_size,
        raw_too_large=payload.raw_too_large,
        headers_json=payload.headers,
        parse_status="parsed" if parsed else ("failed" if parse_error else "received"),
        parse_error=parse_error,
    )

    # 填入解析后的正文
    if parsed:
        email_msg.body_text = parsed.text_body
        email_msg.body_html = parsed.html_body

    session.add(email_msg)
    await session.flush()

    # 保存附件元数据：优先使用 Worker 已上传到 R2 的结果
    if payload.attachments:
        for att in payload.attachments:
            attachment = Attachment(
                email_id=email_msg.id,
                filename=att.filename,
                content_type=att.content_type,
                size=att.size,
                storage_path=att.r2_key,
                storage_backend="r2",
                content_sha256=att.content_sha256,
                is_inline=att.is_inline,
                content_id=att.content_id,
            )
            session.add(attachment)
        await session.flush()
    elif parsed and parsed.attachments:
        for att in parsed.attachments:
            attachment = Attachment(
                email_id=email_msg.id,
                filename=att.filename,
                content_type=att.content_type,
                size=att.size,
            )
            session.add(attachment)
        await session.flush()

    return email_msg, True
