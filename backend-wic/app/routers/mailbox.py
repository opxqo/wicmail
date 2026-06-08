"""邮箱管理路由 - 申请/列表"""
import re

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import settings
from app.database import get_db
from app.models.user import User
from app.models.mailbox import Mailbox, MailboxApplication
from app.schemas.mailbox import (
    MailboxApplyRequest,
    MailboxApplicationResponse,
    MailboxResponse,
    ApplicationListResponse,
)
from app.services.auth import get_current_user

router = APIRouter(prefix="/api/mailbox", tags=["邮箱"])

# 邮箱前缀格式：字母数字点横下划线，3-30 字符
PREFIX_PATTERN = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._-]{2,29}$")


@router.post("/apply", response_model=MailboxApplicationResponse, status_code=201)
async def apply_mailbox(
    req: MailboxApplyRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """申请邮箱"""
    prefix = req.prefix.lower().strip()

    # 校验前缀格式
    if not PREFIX_PATTERN.match(prefix):
        raise HTTPException(
            status_code=400,
            detail="邮箱前缀只能包含字母、数字、点、横杠、下划线，3-30 字符，且不能以特殊字符开头",
        )

    full_address = f"{prefix}@{settings.mailbox_domain}"

    # 检查地址是否已被申请
    result = await db.execute(
        select(MailboxApplication).where(MailboxApplication.requested_address == full_address)
    )
    if result.scalar_one_or_none() is not None:
        raise HTTPException(status_code=400, detail="该邮箱地址已被申请")

    # 检查地址是否已存在
    result = await db.execute(
        select(Mailbox).where(Mailbox.address == full_address)
    )
    if result.scalar_one_or_none() is not None:
        raise HTTPException(status_code=400, detail="该邮箱地址已存在")

    application = MailboxApplication(
        user_id=current_user.id,
        requested_address=full_address,
        display_name=req.display_name,
        reason=req.reason,
        status="pending",
    )
    db.add(application)
    await db.flush()

    return MailboxApplicationResponse.model_validate(application)


@router.get("/applications", response_model=ApplicationListResponse)
async def list_my_applications(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """查看我的申请列表"""
    result = await db.execute(
        select(MailboxApplication)
        .where(MailboxApplication.user_id == current_user.id)
        .order_by(MailboxApplication.created_at.desc())
    )
    apps = result.scalars().all()

    return ApplicationListResponse(
        total=len(apps),
        applications=[MailboxApplicationResponse.model_validate(a) for a in apps],
    )


@router.get("", response_model=list[MailboxResponse])
async def list_my_mailboxes(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """查看我的已批准邮箱"""
    result = await db.execute(
        select(MailboxApplication)
        .where(
            and_(
                MailboxApplication.user_id == current_user.id,
                MailboxApplication.status == "approved",
                MailboxApplication.mailbox_id.isnot(None),
            )
        )
        .options(selectinload(MailboxApplication.mailbox))
    )
    apps = result.scalars().all()

    return [
        MailboxResponse.model_validate(app.mailbox)
        for app in apps
        if app.mailbox is not None
    ]
