"""管理员路由 - 管理员账号管理"""
from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.services.auth import get_admin_user

router = APIRouter(prefix="/api/admin/admins", tags=["管理员-账号"])


class AdminInfo(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    real_name: Optional[str] = None
    is_active: bool
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class AddAdminRequest(BaseModel):
    username: str = Field(..., min_length=1)


class RoleUpdateRequest(BaseModel):
    is_admin: bool


@router.get("", response_model=List[AdminInfo])
async def list_admins(
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    """管理员列表"""
    result = await db.execute(
        select(User).where(User.is_admin == True).order_by(User.created_at)
    )
    admins = result.scalars().all()
    return [
        AdminInfo(
            id=u.id, username=u.username, email=u.email,
            real_name=u.real_name, is_active=u.is_active,
            created_at=u.created_at,
        )
        for u in admins
    ]


@router.post("", response_model=AdminInfo, status_code=201)
async def add_admin(
    req: AddAdminRequest,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    """添加管理员"""
    result = await db.execute(select(User).where(User.username == req.username))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    if user.is_admin:
        raise HTTPException(status_code=400, detail="该用户已经是管理员")

    user.is_admin = True
    await db.flush()

    return AdminInfo(
        id=user.id, username=user.username, email=user.email,
        real_name=user.real_name, is_active=user.is_active,
        created_at=user.created_at,
    )


@router.delete("/{admin_id}")
async def remove_admin(
    admin_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    """移除管理员权限"""
    result = await db.execute(select(User).where(User.id == admin_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    if not user.is_admin:
        raise HTTPException(status_code=400, detail="该用户不是管理员")
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="不能移除自己的管理员权限")

    # 检查是否只剩一个管理员
    count_result = await db.execute(
        select(User).where(User.is_admin == True)
    )
    admin_count = len(count_result.scalars().all())
    if admin_count <= 1:
        raise HTTPException(status_code=400, detail="至少需要保留一个管理员")

    user.is_admin = False
    await db.flush()

    return {"status": "ok", "message": f"已移除 {user.username} 的管理员权限"}


@router.patch("/{admin_id}/role")
async def update_admin_role(
    admin_id: int,
    req: RoleUpdateRequest,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    """分配角色权限"""
    result = await db.execute(select(User).where(User.id == admin_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="用户不存在")

    if not req.is_admin and user.id == admin.id:
        raise HTTPException(status_code=400, detail="不能修改自己的角色")

    # 如果取消管理员，检查是否只剩一个
    if not req.is_admin and user.is_admin:
        count_result = await db.execute(select(User).where(User.is_admin == True))
        admin_count = len(count_result.scalars().all())
        if admin_count <= 1:
            raise HTTPException(status_code=400, detail="至少需要保留一个管理员")

    user.is_admin = req.is_admin
    await db.flush()

    role = "管理员" if user.is_admin else "普通用户"
    return {"status": "ok", "message": f"已将 {user.username} 设为{role}"}
