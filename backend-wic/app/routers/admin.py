"""管理员路由 - 审核申请 + 用户管理"""
from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.user import User
from app.models.mailbox import Mailbox, MailboxApplication
from app.services.auth import get_admin_user

router = APIRouter(prefix="/api/admin", tags=["管理员"])


# --- Schemas ---
class ReviewRequest(BaseModel):
    comment: Optional[str] = None


class ApplicationDetail(BaseModel):
    id: int
    user_id: int
    username: Optional[str] = None
    requested_address: str
    display_name: Optional[str] = None
    status: str
    reason: Optional[str] = None
    review_comment: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class AdminUserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    is_active: bool
    is_admin: bool
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# --- 申请审核 ---

@router.get("/applications", response_model=List[ApplicationDetail])
async def list_applications(
    status: Optional[str] = Query(None, description="筛选状态: pending/approved/rejected"),
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    """查看申请列表"""
    query = select(MailboxApplication).options(selectinload(MailboxApplication.user))

    if status:
        query = query.where(MailboxApplication.status == status)

    query = query.order_by(MailboxApplication.created_at.desc())

    result = await db.execute(query)
    apps = result.scalars().all()

    return [
        ApplicationDetail(
            id=a.id,
            user_id=a.user_id,
            username=a.user.username if a.user else None,
            requested_address=a.requested_address,
            display_name=a.display_name,
            status=a.status,
            reason=a.reason,
            review_comment=a.review_comment,
            reviewed_at=a.reviewed_at,
            created_at=a.created_at,
        )
        for a in apps
    ]


@router.patch("/applications/{app_id}/approve")
async def approve_application(
    app_id: int,
    req: Optional[ReviewRequest] = None,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    """批准申请 → 创建邮箱"""
    result = await db.execute(
        select(MailboxApplication).where(MailboxApplication.id == app_id)
    )
    app = result.scalar_one_or_none()
    if app is None:
        raise HTTPException(status_code=404, detail="申请不存在")

    if app.status != "pending":
        raise HTTPException(status_code=400, detail=f"申请已处理（当前状态: {app.status}）")

    # 创建邮箱
    mailbox = Mailbox(
        address=app.requested_address,
        display_name=app.display_name,
        is_active=True,
    )
    db.add(mailbox)
    await db.flush()

    # 更新申请状态
    app.status = "approved"
    app.reviewed_by = admin.id
    app.reviewed_at = datetime.utcnow()
    app.review_comment = req.comment if req else None
    app.mailbox_id = mailbox.id
    await db.flush()

    return {"status": "ok", "message": f"已批准: {app.requested_address}", "mailbox_id": mailbox.id}


@router.patch("/applications/{app_id}/reject")
async def reject_application(
    app_id: int,
    req: Optional[ReviewRequest] = None,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    """拒绝申请"""
    result = await db.execute(
        select(MailboxApplication).where(MailboxApplication.id == app_id)
    )
    app = result.scalar_one_or_none()
    if app is None:
        raise HTTPException(status_code=404, detail="申请不存在")

    if app.status != "pending":
        raise HTTPException(status_code=400, detail=f"申请已处理（当前状态: {app.status}）")

    app.status = "rejected"
    app.reviewed_by = admin.id
    app.reviewed_at = datetime.utcnow()
    app.review_comment = req.comment if req else None
    await db.flush()

    return {"status": "ok", "message": f"已拒绝: {app.requested_address}"}


# --- 用户管理 ---

@router.get("/users", response_model=List[AdminUserResponse])
async def list_users(
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    """用户列表"""
    result = await db.execute(
        select(User).order_by(User.created_at.desc())
    )
    users = result.scalars().all()
    return [AdminUserResponse.model_validate(u) for u in users]


@router.patch("/users/{user_id}/toggle-active")
async def toggle_user_active(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    """启用/禁用用户"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="用户不存在")

    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="不能禁用自己")

    user.is_active = not user.is_active
    await db.flush()

    action = "启用" if user.is_active else "禁用"
    return {"status": "ok", "message": f"已{action}用户: {user.username}", "is_active": user.is_active}
