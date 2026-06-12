"""用户邮件查看路由 - 限自己的邮箱"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.user import User
from app.models.mailbox import MailboxApplication
from app.models.email import EmailMessage
from app.schemas.email import EmailDetail, EmailListResponse, EmailSummary, AttachmentOut, UnreadCountResponse
from app.services.auth import get_current_user

router = APIRouter(prefix="/api/emails", tags=["邮件"])


async def _get_user_mailbox_ids(db: AsyncSession, user: User) -> list[int]:
    """获取用户所有已批准邮箱的 ID 列表"""
    result = await db.execute(
        select(MailboxApplication.mailbox_id).where(
            and_(
                MailboxApplication.user_id == user.id,
                MailboxApplication.status == "approved",
                MailboxApplication.mailbox_id.isnot(None),
            )
        )
    )
    return [row[0] for row in result.all()]


@router.get("", response_model=EmailListResponse)
async def list_emails(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    q: Optional[str] = Query(None, description="搜索关键词（匹配发件人、主题、正文）"),
    sender: Optional[str] = Query(None, description="按发件人筛选"),
    is_read: Optional[bool] = Query(None, description="按已读/未读筛选"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """我的邮件列表（支持搜索和筛选）"""
    mailbox_ids = await _get_user_mailbox_ids(db, current_user)

    if not mailbox_ids:
        return EmailListResponse(total=0, page=page, page_size=page_size, emails=[])

    # 基础条件：属于用户的邮箱
    conditions = [EmailMessage.mailbox_id.in_(mailbox_ids)]

    # 关键词搜索：匹配发件人、主题、正文
    if q:
        keyword = f"%{q}%"
        conditions.append(or_(
            EmailMessage.header_from.like(keyword),
            EmailMessage.subject.like(keyword),
            EmailMessage.body_text.like(keyword),
        ))

    # 按发件人筛选
    if sender:
        conditions.append(EmailMessage.header_from.like(f"%{sender}%"))

    # 按已读/未读筛选
    if is_read is not None:
        conditions.append(EmailMessage.is_read == is_read)

    where_clause = and_(*conditions)

    # 总数
    count_result = await db.execute(
        select(func.count(EmailMessage.id)).where(where_clause)
    )
    total = count_result.scalar()

    # 分页
    offset = (page - 1) * page_size
    result = await db.execute(
        select(EmailMessage)
        .options(selectinload(EmailMessage.mailbox), selectinload(EmailMessage.attachments))
        .where(where_clause)
        .order_by(EmailMessage.received_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    messages = result.scalars().all()

    emails = []
    for msg in messages:
        emails.append(EmailSummary(
            id=msg.id,
            mailbox_address=msg.mailbox.address if msg.mailbox else None,
            subject=msg.subject,
            header_from=msg.header_from,
            header_to=msg.header_to,
            envelope_from=msg.envelope_from,
            envelope_to=msg.envelope_to,
            received_at=msg.received_at,
            is_read=msg.is_read,
            attachment_count=len(msg.attachments),
        ))

    return EmailListResponse(total=total, page=page, page_size=page_size, emails=emails)


@router.get("/unread-count", response_model=UnreadCountResponse)
async def get_unread_count(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """未读邮件数量"""
    mailbox_ids = await _get_user_mailbox_ids(db, current_user)

    if not mailbox_ids:
        return UnreadCountResponse(unread_count=0)

    result = await db.execute(
        select(func.count(EmailMessage.id)).where(
            and_(
                EmailMessage.mailbox_id.in_(mailbox_ids),
                EmailMessage.is_read == False,
            )
        )
    )
    return UnreadCountResponse(unread_count=result.scalar() or 0)


@router.get("/{email_id}", response_model=EmailDetail)
async def get_email_detail(
    email_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """邮件详情"""
    mailbox_ids = await _get_user_mailbox_ids(db, current_user)

    result = await db.execute(
        select(EmailMessage)
        .options(selectinload(EmailMessage.mailbox), selectinload(EmailMessage.attachments))
        .where(
            and_(EmailMessage.id == email_id, EmailMessage.mailbox_id.in_(mailbox_ids))
        )
    )
    msg = result.scalar_one_or_none()

    if msg is None:
        raise HTTPException(status_code=404, detail="邮件不存在")

    return EmailDetail(
        id=msg.id,
        mailbox_address=msg.mailbox.address if msg.mailbox else None,
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
            AttachmentOut(id=a.id, filename=a.filename, content_type=a.content_type, size=a.size)
            for a in msg.attachments
        ],
    )


@router.patch("/{email_id}/read")
async def mark_as_read(
    email_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """标记已读"""
    mailbox_ids = await _get_user_mailbox_ids(db, current_user)

    result = await db.execute(
        select(EmailMessage).where(
            and_(EmailMessage.id == email_id, EmailMessage.mailbox_id.in_(mailbox_ids))
        )
    )
    msg = result.scalar_one_or_none()
    if msg is None:
        raise HTTPException(status_code=404, detail="邮件不存在")

    msg.is_read = True
    await db.flush()
    return {"status": "ok", "email_id": email_id, "is_read": True}


@router.patch("/{email_id}/unread")
async def mark_as_unread(
    email_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """标记未读"""
    mailbox_ids = await _get_user_mailbox_ids(db, current_user)

    result = await db.execute(
        select(EmailMessage).where(
            and_(EmailMessage.id == email_id, EmailMessage.mailbox_id.in_(mailbox_ids))
        )
    )
    msg = result.scalar_one_or_none()
    if msg is None:
        raise HTTPException(status_code=404, detail="邮件不存在")

    msg.is_read = False
    await db.flush()
    return {"status": "ok", "email_id": email_id, "is_read": False}
