"""管理员路由 - 统计仪表盘"""
from datetime import datetime, timedelta
from typing import Optional, List

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import select, func, case
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.models.mailbox import Mailbox, MailboxApplication
from app.models.email import EmailMessage, Attachment
from app.services.auth import get_admin_user

router = APIRouter(prefix="/api/admin/stats", tags=["管理员-统计"])


class OverviewResponse(BaseModel):
    total_users: int
    active_users: int
    total_mailboxes: int
    active_mailboxes: int
    total_emails: int
    unread_emails: int
    total_applications: int
    pending_applications: int
    total_attachments: int
    today_new_users: int
    today_new_emails: int


class TrendItem(BaseModel):
    date: str
    count: int


class StatusDistribution(BaseModel):
    status: str
    count: int


class MailboxUsage(BaseModel):
    id: int
    address: str
    email_count: int
    unread_count: int


class StorageStats(BaseModel):
    total_size_bytes: int
    total_size_mb: float
    total_attachments: int
    avg_email_size_bytes: int


@router.get("/overview", response_model=OverviewResponse)
async def get_overview(
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    """总览数据"""
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

    total_users = (await db.execute(select(func.count(User.id)))).scalar() or 0
    active_users = (await db.execute(
        select(func.count(User.id)).where(User.is_active == True)
    )).scalar() or 0
    total_mailboxes = (await db.execute(select(func.count(Mailbox.id)))).scalar() or 0
    active_mailboxes = (await db.execute(
        select(func.count(Mailbox.id)).where(Mailbox.is_active == True)
    )).scalar() or 0
    total_emails = (await db.execute(select(func.count(EmailMessage.id)))).scalar() or 0
    unread_emails = (await db.execute(
        select(func.count(EmailMessage.id)).where(EmailMessage.is_read == False)
    )).scalar() or 0
    total_applications = (await db.execute(
        select(func.count(MailboxApplication.id))
    )).scalar() or 0
    pending_applications = (await db.execute(
        select(func.count(MailboxApplication.id)).where(MailboxApplication.status == "pending")
    )).scalar() or 0
    total_attachments = (await db.execute(
        select(func.count(Attachment.id))
    )).scalar() or 0
    today_new_users = (await db.execute(
        select(func.count(User.id)).where(User.created_at >= today)
    )).scalar() or 0
    today_new_emails = (await db.execute(
        select(func.count(EmailMessage.id)).where(EmailMessage.received_at >= today)
    )).scalar() or 0

    return OverviewResponse(
        total_users=total_users, active_users=active_users,
        total_mailboxes=total_mailboxes, active_mailboxes=active_mailboxes,
        total_emails=total_emails, unread_emails=unread_emails,
        total_applications=total_applications, pending_applications=pending_applications,
        total_attachments=total_attachments,
        today_new_users=today_new_users, today_new_emails=today_new_emails,
    )


@router.get("/users", response_model=List[TrendItem])
async def user_registration_trend(
    days: int = Query(30, ge=1, le=365, description="统计天数"),
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    """用户注册趋势"""
    since = datetime.utcnow() - timedelta(days=days)
    result = await db.execute(
        select(
            func.date(User.created_at).label("date"),
            func.count(User.id).label("count"),
        )
        .where(User.created_at >= since)
        .group_by(func.date(User.created_at))
        .order_by(func.date(User.created_at))
    )
    return [TrendItem(date=str(row.date), count=row.count) for row in result.all()]


@router.get("/emails", response_model=List[TrendItem])
async def email_receive_trend(
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    """邮件接收趋势"""
    since = datetime.utcnow() - timedelta(days=days)
    result = await db.execute(
        select(
            func.date(EmailMessage.received_at).label("date"),
            func.count(EmailMessage.id).label("count"),
        )
        .where(EmailMessage.received_at >= since)
        .group_by(func.date(EmailMessage.received_at))
        .order_by(func.date(EmailMessage.received_at))
    )
    return [TrendItem(date=str(row.date), count=row.count) for row in result.all()]


@router.get("/applications", response_model=List[StatusDistribution])
async def application_status_distribution(
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    """申请状态分布"""
    result = await db.execute(
        select(
            MailboxApplication.status,
            func.count(MailboxApplication.id).label("count"),
        )
        .group_by(MailboxApplication.status)
    )
    return [StatusDistribution(status=row.status, count=row.count) for row in result.all()]


@router.get("/mailboxes", response_model=List[MailboxUsage])
async def mailbox_usage_ranking(
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    """邮箱使用量排行"""
    result = await db.execute(
        select(
            Mailbox.id, Mailbox.address,
            func.count(EmailMessage.id).label("email_count"),
            func.sum(case((EmailMessage.is_read == False, 1), else_=0)).label("unread_count"),
        )
        .outerjoin(EmailMessage, EmailMessage.mailbox_id == Mailbox.id)
        .group_by(Mailbox.id, Mailbox.address)
        .order_by(func.count(EmailMessage.id).desc())
        .limit(limit)
    )
    return [
        MailboxUsage(id=row.id, address=row.address, email_count=row.email_count, unread_count=row.unread_count or 0)
        for row in result.all()
    ]


@router.get("/storage", response_model=StorageStats)
async def storage_stats(
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    """存储占用统计"""
    # raw_size 包含完整邮件（含附件），不再重复加附件大小
    total_email_size = (await db.execute(
        select(func.coalesce(func.sum(EmailMessage.raw_size), 0))
    )).scalar() or 0
    total_att = (await db.execute(
        select(func.count(Attachment.id))
    )).scalar() or 0
    total_email_count = (await db.execute(
        select(func.count(EmailMessage.id))
    )).scalar() or 0

    avg_size = (total_email_size // total_email_count) if total_email_count > 0 else 0

    return StorageStats(
        total_size_bytes=total_email_size,
        total_size_mb=round(total_email_size / 1024 / 1024, 2),
        total_attachments=total_att,
        avg_email_size_bytes=avg_size,
    )
