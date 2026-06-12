"""管理员路由 - 用户管理 + 申请审核"""
from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.user import User
from app.models.mailbox import Mailbox, MailboxApplication
from app.models.admin_log import AdminLog
from app.services.auth import get_admin_user

router = APIRouter(prefix="/api/admin", tags=["管理员"])


# ==================== Schemas ====================

class ReviewRequest(BaseModel):
    comment: Optional[str] = None


class BatchIdsRequest(BaseModel):
    ids: List[int] = Field(..., min_length=1)
    comment: Optional[str] = None


class AdminUserResponse(BaseModel):
    id: int
    username: str
    student_id: Optional[str] = None
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    real_name: Optional[str] = None
    department: Optional[str] = None
    major: Optional[str] = None
    class_name: Optional[str] = None
    grade: Optional[str] = None
    is_active: bool
    is_admin: bool
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class AdminUserDetail(BaseModel):
    id: int
    username: str
    student_id: Optional[str] = None
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    real_name: Optional[str] = None
    department: Optional[str] = None
    major: Optional[str] = None
    class_name: Optional[str] = None
    grade: Optional[str] = None
    is_active: bool
    is_admin: bool
    profile_complete: bool
    missing_fields: List[str]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    mailbox_count: int = 0
    application_count: int = 0

    model_config = {"from_attributes": True}


class UserUpdateRequest(BaseModel):
    email: Optional[str] = None
    real_name: Optional[str] = Field(None, min_length=1, max_length=50)
    department: Optional[str] = Field(None, min_length=1, max_length=100)
    major: Optional[str] = Field(None, min_length=1, max_length=100)
    class_name: Optional[str] = Field(None, min_length=1, max_length=50)
    grade: Optional[str] = Field(None, min_length=1, max_length=10)
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None


class ResetPasswordRequest(BaseModel):
    new_password: str = Field(..., min_length=6, max_length=100)


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


class ApplicationDetailFull(ApplicationDetail):
    reviewed_by: Optional[int] = None
    mailbox_id: Optional[int] = None
    user_email: Optional[str] = None
    user_real_name: Optional[str] = None
    user_student_id: Optional[str] = None


class PaginatedUsers(BaseModel):
    total: int
    page: int
    page_size: int
    users: List[AdminUserResponse]


# ==================== 用户管理 ====================

@router.get("/users", response_model=PaginatedUsers)
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    q: Optional[str] = Query(None, description="搜索用户名/姓名/学号/邮箱"),
    is_active: Optional[bool] = Query(None),
    is_admin: Optional[bool] = Query(None),
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    """用户列表（搜索/筛选/分页）"""
    conditions = []
    if q:
        keyword = f"%{q}%"
        conditions.append(or_(
            User.username.like(keyword),
            User.real_name.like(keyword),
            User.student_id.like(keyword),
            User.email.like(keyword),
        ))
    if is_active is not None:
        conditions.append(User.is_active == is_active)
    if is_admin is not None:
        conditions.append(User.is_admin == is_admin)

    where_clause = and_(*conditions) if conditions else True

    count_result = await db.execute(
        select(func.count(User.id)).where(where_clause)
    )
    total = count_result.scalar()

    offset = (page - 1) * page_size
    result = await db.execute(
        select(User).where(where_clause)
        .order_by(User.created_at.desc())
        .offset(offset).limit(page_size)
    )
    users = result.scalars().all()

    return PaginatedUsers(
        total=total, page=page, page_size=page_size,
        users=[AdminUserResponse.model_validate(u) for u in users],
    )


@router.get("/users/{user_id}", response_model=AdminUserDetail)
async def get_user_detail(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    """用户详情"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 统计邮箱和申请数
    mb_count = await db.execute(
        select(func.count(MailboxApplication.id)).where(
            and_(MailboxApplication.user_id == user_id, MailboxApplication.status == "approved")
        )
    )
    app_count = await db.execute(
        select(func.count(MailboxApplication.id)).where(MailboxApplication.user_id == user_id)
    )

    return AdminUserDetail(
        id=user.id, username=user.username, student_id=user.student_id,
        email=user.email, avatar_url=user.avatar_url, real_name=user.real_name,
        department=user.department, major=user.major,
        class_name=user.class_name, grade=user.grade,
        is_active=user.is_active, is_admin=user.is_admin,
        profile_complete=user.profile_complete,
        missing_fields=user.get_missing_fields(),
        created_at=user.created_at, updated_at=user.updated_at,
        mailbox_count=mb_count.scalar() or 0,
        application_count=app_count.scalar() or 0,
    )


@router.patch("/users/{user_id}", response_model=AdminUserResponse)
async def update_user(
    user_id: int,
    req: UserUpdateRequest,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    """修改用户信息"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="用户不存在")

    update_data = req.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="未提供任何更新字段")

    for field, value in update_data.items():
        setattr(user, field, value)
    await db.flush()

    return AdminUserResponse.model_validate(user)


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


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    """删除用户（硬删除）"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="不能删除自己")
    if user.is_admin:
        raise HTTPException(status_code=400, detail="不能删除管理员账户")

    # 审核过的申请 reviewed_by 置空
    reviewed_result = await db.execute(
        select(MailboxApplication).where(MailboxApplication.reviewed_by == user_id)
    )
    for reviewed_app in reviewed_result.scalars().all():
        reviewed_app.reviewed_by = None

    # 清理该用户的操作日志外键
    logs_result = await db.execute(
        select(AdminLog).where(AdminLog.admin_id == user_id)
    )
    for log in logs_result.scalars().all():
        log.admin_id = 0  # 设为系统占位 ID

    # 停用已批准的邮箱并删除申请记录
    apps_result = await db.execute(
        select(MailboxApplication).where(MailboxApplication.user_id == user_id)
    )
    user_apps = apps_result.scalars().all()
    for app in user_apps:
        if app.mailbox_id:
            mb_result = await db.execute(select(Mailbox).where(Mailbox.id == app.mailbox_id))
            mailbox = mb_result.scalar_one_or_none()
            if mailbox:
                mailbox.is_active = False
        await db.delete(app)

    await db.delete(user)
    await db.flush()

    return {"status": "ok", "message": f"已删除用户: {user.username}"}


@router.post("/users/{user_id}/reset-password")
async def reset_user_password(
    user_id: int,
    req: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    """重置用户密码"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="用户不存在")

    user.set_password(req.new_password)
    await db.flush()

    return {"status": "ok", "message": f"已重置用户 {user.username} 的密码"}


# ==================== 申请审核 ====================

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
            id=a.id, user_id=a.user_id,
            username=a.user.username if a.user else None,
            requested_address=a.requested_address,
            display_name=a.display_name, status=a.status,
            reason=a.reason, review_comment=a.review_comment,
            reviewed_at=a.reviewed_at, created_at=a.created_at,
        )
        for a in apps
    ]


@router.get("/applications/{app_id}", response_model=ApplicationDetailFull)
async def get_application_detail(
    app_id: int,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    """申请详情"""
    result = await db.execute(
        select(MailboxApplication).options(selectinload(MailboxApplication.user))
        .where(MailboxApplication.id == app_id)
    )
    app = result.scalar_one_or_none()
    if app is None:
        raise HTTPException(status_code=404, detail="申请不存在")

    user = app.user
    return ApplicationDetailFull(
        id=app.id, user_id=app.user_id,
        username=user.username if user else None,
        requested_address=app.requested_address,
        display_name=app.display_name, status=app.status,
        reason=app.reason, review_comment=app.review_comment,
        reviewed_at=app.reviewed_at, created_at=app.created_at,
        reviewed_by=app.reviewed_by, mailbox_id=app.mailbox_id,
        user_email=user.email if user else None,
        user_real_name=user.real_name if user else None,
        user_student_id=user.student_id if user else None,
    )


async def _approve_one(db: AsyncSession, admin: User, app_id: int):
    """内部：批准单个申请"""
    result = await db.execute(
        select(MailboxApplication).where(MailboxApplication.id == app_id).with_for_update()
    )
    app = result.scalar_one_or_none()
    if app is None or app.status != "pending":
        return None

    mailbox = Mailbox(address=app.requested_address, display_name=app.display_name, is_active=True)
    db.add(mailbox)
    await db.flush()

    app.status = "approved"
    app.reviewed_by = admin.id
    app.reviewed_at = datetime.utcnow()
    app.mailbox_id = mailbox.id
    return app.requested_address


async def _reject_one(db: AsyncSession, admin: User, app_id: int, comment: Optional[str]):
    """内部：拒绝单个申请"""
    result = await db.execute(
        select(MailboxApplication).where(MailboxApplication.id == app_id).with_for_update()
    )
    app = result.scalar_one_or_none()
    if app is None or app.status != "pending":
        return None

    app.status = "rejected"
    app.reviewed_by = admin.id
    app.reviewed_at = datetime.utcnow()
    app.review_comment = comment
    return app.requested_address


@router.patch("/applications/{app_id}/approve")
async def approve_application(
    app_id: int,
    req: Optional[ReviewRequest] = None,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    """批准申请 → 创建邮箱"""
    address = await _approve_one(db, admin, app_id)
    if address is None:
        raise HTTPException(status_code=400, detail="申请不存在或已处理")
    await db.flush()
    return {"status": "ok", "message": f"已批准: {address}"}


@router.patch("/applications/{app_id}/reject")
async def reject_application(
    app_id: int,
    req: Optional[ReviewRequest] = None,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    """拒绝申请"""
    comment = req.comment if req else None
    address = await _reject_one(db, admin, app_id, comment)
    if address is None:
        raise HTTPException(status_code=400, detail="申请不存在或已处理")
    await db.flush()
    return {"status": "ok", "message": f"已拒绝: {address}"}


@router.post("/applications/batch-approve")
async def batch_approve(
    req: BatchIdsRequest,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    """批量批准"""
    approved = []
    for app_id in req.ids:
        address = await _approve_one(db, admin, app_id)
        if address:
            approved.append(address)
    await db.flush()
    return {"status": "ok", "approved": approved, "count": len(approved)}


@router.post("/applications/batch-reject")
async def batch_reject(
    req: BatchIdsRequest,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    """批量拒绝"""
    rejected = []
    for app_id in req.ids:
        address = await _reject_one(db, admin, app_id, req.comment)
        if address:
            rejected.append(address)
    await db.flush()
    return {"status": "ok", "rejected": rejected, "count": len(rejected)}
