"""邮件查询接口 - 需要 JWT 认证"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.email import EmailMessage
from app.models.user import User
from app.schemas.email import EmailDetail, EmailListResponse, EmailSummary, AttachmentOut
from app.services.auth import get_current_user

router = APIRouter()


@router.get("/api/emails", response_model=EmailListResponse)
async def list_emails(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """分页查询邮件列表（需要登录）"""
    # 总数
    count_result = await db.execute(select(func.count(EmailMessage.id)))
    total = count_result.scalar()

    # 分页查询，附带附件数量
    offset = (page - 1) * page_size
    result = await db.execute(
        select(EmailMessage)
        .options(selectinload(EmailMessage.attachments))
        .order_by(EmailMessage.received_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    messages = result.scalars().all()

    emails = []
    for msg in messages:
        emails.append(EmailSummary(
            id=msg.id,
            subject=msg.subject,
            header_from=msg.header_from,
            header_to=msg.header_to,
            envelope_from=msg.envelope_from,
            envelope_to=msg.envelope_to,
            received_at=msg.received_at,
            is_read=msg.is_read,
            attachment_count=len(msg.attachments),
        ))

    return EmailListResponse(
        total=total,
        page=page,
        page_size=page_size,
        emails=emails,
    )


@router.get("/api/emails/{email_id}", response_model=EmailDetail)
async def get_email_detail(
    email_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """获取邮件详情（需要登录，不自动标记已读）"""
    result = await db.execute(
        select(EmailMessage)
        .options(selectinload(EmailMessage.attachments))
        .where(EmailMessage.id == email_id)
    )
    msg = result.scalar_one_or_none()

    if msg is None:
        raise HTTPException(status_code=404, detail="邮件不存在")

    return EmailDetail(
        id=msg.id,
        subject=msg.subject,
        header_from=msg.header_from,
        header_to=msg.header_to,
        header_cc=msg.header_cc,
        header_reply_to=msg.header_reply_to,
        envelope_from=msg.envelope_from,
        envelope_to=msg.envelope_to,
        message_id=msg.message_id,
        sent_at=msg.sent_at,
        received_at=msg.received_at,
        raw_size=msg.raw_size,
        body_text=msg.body_text,
        body_html=msg.body_html,
        parse_status=msg.parse_status,
        is_read=msg.is_read,
        attachments=[
            AttachmentOut(
                id=att.id,
                filename=att.filename,
                content_type=att.content_type,
                size=att.size,
            )
            for att in msg.attachments
        ],
    )


@router.patch("/api/emails/{email_id}/read")
async def mark_as_read(
    email_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """标记邮件为已读"""
    result = await db.execute(
        select(EmailMessage).where(EmailMessage.id == email_id)
    )
    msg = result.scalar_one_or_none()

    if msg is None:
        raise HTTPException(status_code=404, detail="邮件不存在")

    msg.is_read = True
    await db.flush()
    return {"status": "ok", "email_id": email_id, "is_read": True}


@router.patch("/api/emails/{email_id}/unread")
async def mark_as_unread(
    email_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """标记邮件为未读"""
    result = await db.execute(
        select(EmailMessage).where(EmailMessage.id == email_id)
    )
    msg = result.scalar_one_or_none()

    if msg is None:
        raise HTTPException(status_code=404, detail="邮件不存在")

    msg.is_read = False
    await db.flush()
    return {"status": "ok", "email_id": email_id, "is_read": False}
