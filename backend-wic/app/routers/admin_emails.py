"""管理员路由 - 邮件管理"""
from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.user import User
from app.models.mailbox import Mailbox
from app.models.email import EmailMessage
from app.schemas.email import AttachmentOut
from app.services.auth import get_admin_user

router = APIRouter(prefix="/api/admin/emails", tags=["管理员-邮件"])


class AdminEmailSummary(BaseModel):
    id: int
    mailbox_address: Optional[str] = None
    subject: Optional[str] = None
    header_from: Optional[str] = None
    header_to: Optional[str] = None
    received_at: Optional[datetime] = None
    is_read: bool = False
    attachment_count: int = 0

    model_config = {"from_attributes": True}


class AdminEmailDetail(BaseModel):
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


class AdminEmailListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    emails: List[AdminEmailSummary]


class BatchDeleteRequest(BaseModel):
    ids: List[int] = Field(..., min_length=1)


@router.get("", response_model=AdminEmailListResponse)
async def list_all_emails(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    q: Optional[str] = Query(None, description="搜索关键词"),
    sender: Optional[str] = Query(None),
    is_read: Optional[bool] = Query(None),
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    """所有邮件（跨用户）"""
    conditions = []
    if q:
        keyword = f"%{q}%"
        conditions.append(or_(
            EmailMessage.header_from.like(keyword),
            EmailMessage.subject.like(keyword),
            EmailMessage.body_text.like(keyword),
        ))
    if sender:
        conditions.append(EmailMessage.header_from.like(f"%{sender}%"))
    if is_read is not None:
        conditions.append(EmailMessage.is_read == is_read)

    where_clause = and_(*conditions) if conditions else True

    total = (await db.execute(
        select(func.count(EmailMessage.id)).where(where_clause)
    )).scalar() or 0

    offset = (page - 1) * page_size
    result = await db.execute(
        select(EmailMessage)
        .options(selectinload(EmailMessage.mailbox), selectinload(EmailMessage.attachments))
        .where(where_clause)
        .order_by(EmailMessage.received_at.desc())
        .offset(offset).limit(page_size)
    )
    messages = result.scalars().all()

    emails = [
        AdminEmailSummary(
            id=msg.id,
            mailbox_address=msg.mailbox.address if msg.mailbox else None,
            subject=msg.subject, header_from=msg.header_from,
            header_to=msg.header_to, received_at=msg.received_at,
            is_read=msg.is_read, attachment_count=len(msg.attachments),
        )
        for msg in messages
    ]
    return AdminEmailListResponse(total=total, page=page, page_size=page_size, emails=emails)


@router.get("/search", response_model=AdminEmailListResponse)
async def search_emails(
    q: str = Query(..., min_length=1, description="搜索关键词"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    """全文搜索"""
    keyword = f"%{q}%"
    where_clause = or_(
        EmailMessage.header_from.like(keyword),
        EmailMessage.subject.like(keyword),
        EmailMessage.body_text.like(keyword),
        EmailMessage.body_html.like(keyword),
        EmailMessage.envelope_from.like(keyword),
    )

    total = (await db.execute(
        select(func.count(EmailMessage.id)).where(where_clause)
    )).scalar() or 0

    offset = (page - 1) * page_size
    result = await db.execute(
        select(EmailMessage)
        .options(selectinload(EmailMessage.mailbox), selectinload(EmailMessage.attachments))
        .where(where_clause)
        .order_by(EmailMessage.received_at.desc())
        .offset(offset).limit(page_size)
    )
    messages = result.scalars().all()

    emails = [
        AdminEmailSummary(
            id=msg.id,
            mailbox_address=msg.mailbox.address if msg.mailbox else None,
            subject=msg.subject, header_from=msg.header_from,
            header_to=msg.header_to, received_at=msg.received_at,
            is_read=msg.is_read, attachment_count=len(msg.attachments),
        )
        for msg in messages
    ]
    return AdminEmailListResponse(total=total, page=page, page_size=page_size, emails=emails)


@router.get("/{email_id}", response_model=AdminEmailDetail)
async def get_email_detail(
    email_id: int,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    """邮件详情"""
    result = await db.execute(
        select(EmailMessage)
        .options(selectinload(EmailMessage.mailbox), selectinload(EmailMessage.attachments))
        .where(EmailMessage.id == email_id)
    )
    msg = result.scalar_one_or_none()
    if msg is None:
        raise HTTPException(status_code=404, detail="邮件不存在")

    return AdminEmailDetail(
        id=msg.id, mailbox_address=msg.mailbox.address if msg.mailbox else None,
        subject=msg.subject, header_from=msg.header_from,
        header_to=msg.header_to, header_cc=msg.header_cc,
        header_reply_to=msg.header_reply_to,
        envelope_from=msg.envelope_from, envelope_to=msg.envelope_to,
        message_id=msg.message_id, sent_at=msg.sent_at,
        received_at=msg.received_at, raw_size=msg.raw_size,
        body_text=msg.body_text, body_html=msg.body_html,
        parse_status=msg.parse_status, is_read=msg.is_read,
        attachments=[AttachmentOut(id=a.id, filename=a.filename, content_type=a.content_type, size=a.size) for a in msg.attachments],
    )


@router.delete("/{email_id}")
async def delete_email(
    email_id: int,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    """删除邮件"""
    result = await db.execute(select(EmailMessage).where(EmailMessage.id == email_id))
    msg = result.scalar_one_or_none()
    if msg is None:
        raise HTTPException(status_code=404, detail="邮件不存在")

    # 删除附件
    for att in msg.attachments:
        await db.delete(att)
    await db.delete(msg)
    await db.flush()

    return {"status": "ok", "message": f"已删除邮件 #{email_id}"}


@router.post("/batch-delete")
async def batch_delete_emails(
    req: BatchDeleteRequest,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    """批量删除邮件"""
    deleted = []
    for email_id in req.ids:
        result = await db.execute(select(EmailMessage).where(EmailMessage.id == email_id))
        msg = result.scalar_one_or_none()
        if msg:
            for att in msg.attachments:
                await db.delete(att)
            await db.delete(msg)
            deleted.append(email_id)
    await db.flush()

    return {"status": "ok", "deleted": deleted, "count": len(deleted)}
