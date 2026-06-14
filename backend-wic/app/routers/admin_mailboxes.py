"""管理员路由 - 邮箱管理"""
from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel, Field
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.user import User
from app.models.mailbox import Mailbox, MailboxApplication
from app.services.admin_audit import add_admin_log
from app.services.auth import get_admin_user

router = APIRouter(prefix="/api/admin/mailboxes", tags=["管理员-邮箱"])


class MailboxResponse(BaseModel):
    id: int
    address: str
    display_name: Optional[str] = None
    is_active: bool
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class MailboxDetail(MailboxResponse):
    email_count: int = 0
    unread_count: int = 0
    owner_username: Optional[str] = None
    owner_user_id: Optional[int] = None


class CreateMailboxRequest(BaseModel):
    address: str = Field(..., min_length=3, max_length=255)
    display_name: Optional[str] = None


@router.get("", response_model=List[MailboxResponse])
async def list_mailboxes(
    q: Optional[str] = Query(None, description="搜索邮箱地址"),
    is_active: Optional[bool] = Query(None),
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    """所有邮箱列表"""
    conditions = []
    if q:
        conditions.append(Mailbox.address.like(f"%{q}%"))
    if is_active is not None:
        conditions.append(Mailbox.is_active == is_active)

    query = select(Mailbox)
    if conditions:
        query = query.where(and_(*conditions))
    query = query.order_by(Mailbox.created_at.desc())

    result = await db.execute(query)
    return [MailboxResponse.model_validate(m) for m in result.scalars().all()]


@router.get("/{mailbox_id}", response_model=MailboxDetail)
async def get_mailbox_detail(
    mailbox_id: int,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    """邮箱详情"""
    from app.models.email import EmailMessage

    result = await db.execute(select(Mailbox).where(Mailbox.id == mailbox_id))
    mailbox = result.scalar_one_or_none()
    if mailbox is None:
        raise HTTPException(status_code=404, detail="邮箱不存在")

    email_count = await db.execute(
        select(func.count(EmailMessage.id)).where(EmailMessage.mailbox_id == mailbox_id)
    )
    unread_count = await db.execute(
        select(func.count(EmailMessage.id)).where(
            and_(EmailMessage.mailbox_id == mailbox_id, EmailMessage.is_read == False)
        )
    )

    # 查找拥有者
    owner_result = await db.execute(
        select(MailboxApplication).where(
            and_(MailboxApplication.mailbox_id == mailbox_id, MailboxApplication.status == "approved")
        ).options(selectinload(MailboxApplication.user))
    )
    owner_app = owner_result.scalar_one_or_none()

    return MailboxDetail(
        id=mailbox.id, address=mailbox.address,
        display_name=mailbox.display_name, is_active=mailbox.is_active,
        created_at=mailbox.created_at,
        email_count=email_count.scalar() or 0,
        unread_count=unread_count.scalar() or 0,
        owner_username=owner_app.user.username if owner_app and owner_app.user else None,
        owner_user_id=owner_app.user_id if owner_app else None,
    )


@router.post("", response_model=MailboxResponse, status_code=201)
async def create_mailbox(
    req: CreateMailboxRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    """手动创建邮箱"""
    existing = await db.execute(
        select(Mailbox).where(Mailbox.address == req.address)
    )
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(status_code=400, detail="该邮箱地址已存在")

    mailbox = Mailbox(address=req.address, display_name=req.display_name, is_active=True)
    db.add(mailbox)
    await db.flush()
    add_admin_log(
        db, admin, "创建邮箱", "mailbox",
        target_id=mailbox.id,
        target_name=mailbox.address,
        detail=f"手动创建邮箱: {mailbox.address}",
        request=request,
    )

    return MailboxResponse.model_validate(mailbox)


@router.patch("/{mailbox_id}/toggle-active")
async def toggle_mailbox_active(
    mailbox_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    """启停邮箱"""
    result = await db.execute(select(Mailbox).where(Mailbox.id == mailbox_id))
    mailbox = result.scalar_one_or_none()
    if mailbox is None:
        raise HTTPException(status_code=404, detail="邮箱不存在")

    mailbox.is_active = not mailbox.is_active
    action = "启用" if mailbox.is_active else "停用"
    add_admin_log(
        db, admin, action, "mailbox",
        target_id=mailbox.id,
        target_name=mailbox.address,
        detail=f"{action}邮箱: {mailbox.address}",
        request=request,
    )
    await db.flush()

    return {"status": "ok", "message": f"已{action}邮箱: {mailbox.address}", "is_active": mailbox.is_active}


@router.delete("/{mailbox_id}")
async def delete_mailbox(
    mailbox_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    """删除邮箱"""
    result = await db.execute(select(Mailbox).where(Mailbox.id == mailbox_id))
    mailbox = result.scalar_one_or_none()
    if mailbox is None:
        raise HTTPException(status_code=404, detail="邮箱不存在")
    deleted_address = mailbox.address

    # 解除申请关联
    apps_result = await db.execute(
        select(MailboxApplication).where(MailboxApplication.mailbox_id == mailbox_id)
    )
    for app in apps_result.scalars().all():
        app.mailbox_id = None

    await db.delete(mailbox)
    add_admin_log(
        db, admin, "删除邮箱", "mailbox",
        target_id=mailbox_id,
        target_name=deleted_address,
        detail=f"删除邮箱: {deleted_address}",
        request=request,
    )
    await db.flush()

    return {"status": "ok", "message": f"已删除邮箱: {deleted_address}"}
