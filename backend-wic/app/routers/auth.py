"""认证路由 - 注册/登录/资料管理"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.auth import (
    RegisterRequest, LoginRequest, TokenResponse,
    UserResponse, ProfileResponse, ProfileUpdateRequest,
    ChangePasswordRequest,
)
from app.services.jwt_utils import create_access_token
from app.services.auth import get_current_user

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(req: RegisterRequest, db: AsyncSession = Depends(get_db)):
    """注册新用户（用户名 + 学号 + 密码）"""
    # 检查用户名是否已存在
    result = await db.execute(select(User).where(User.username == req.username))
    if result.scalar_one_or_none() is not None:
        raise HTTPException(status_code=400, detail="用户名已存在")

    # 检查学号是否已注册
    result = await db.execute(select(User).where(User.student_id == req.student_id))
    if result.scalar_one_or_none() is not None:
        raise HTTPException(status_code=400, detail="该学号已被注册")

    user = User(
        username=req.username,
        student_id=req.student_id,
        is_active=True,
        is_admin=False,
    )
    user.set_password(req.password)

    db.add(user)
    await db.flush()

    return UserResponse.model_validate(user)


@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    """登录，返回 JWT"""
    result = await db.execute(select(User).where(User.username == req.username))
    user = result.scalar_one_or_none()

    if user is None or not user.verify_password(req.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="账号已被禁用")

    token = create_access_token(subject=user.id)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """获取当前登录用户基本信息"""
    return UserResponse.model_validate(current_user)


# --- 资料管理 ---

@router.get("/profile", response_model=ProfileResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    """查看完整个人资料"""
    return ProfileResponse(
        id=current_user.id,
        username=current_user.username,
        student_id=current_user.student_id,
        email=current_user.email,
        avatar_url=current_user.avatar_url,
        real_name=current_user.real_name,
        department=current_user.department,
        major=current_user.major,
        class_name=current_user.class_name,
        grade=current_user.grade,
        profile_complete=current_user.profile_complete,
        missing_fields=current_user.get_missing_fields(),
        is_active=current_user.is_active,
        is_admin=current_user.is_admin,
    )


@router.patch("/profile", response_model=ProfileResponse)
async def update_profile(
    req: ProfileUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """更新个人资料（支持单字段或多字段更新）"""
    update_data = req.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="未提供任何更新字段")

    # 邮箱唯一性检查
    if "email" in update_data and update_data["email"] != current_user.email:
        result = await db.execute(
            select(User).where(
                User.email == update_data["email"],
                User.id != current_user.id,
            )
        )
        if result.scalar_one_or_none() is not None:
            raise HTTPException(status_code=400, detail="该邮箱已被其他用户使用")

    # 逐字段更新
    for field, value in update_data.items():
        setattr(current_user, field, value)

    await db.flush()

    return ProfileResponse(
        id=current_user.id,
        username=current_user.username,
        student_id=current_user.student_id,
        email=current_user.email,
        avatar_url=current_user.avatar_url,
        real_name=current_user.real_name,
        department=current_user.department,
        major=current_user.major,
        class_name=current_user.class_name,
        grade=current_user.grade,
        profile_complete=current_user.profile_complete,
        missing_fields=current_user.get_missing_fields(),
        is_active=current_user.is_active,
        is_admin=current_user.is_admin,
    )


# --- 修改密码 ---

@router.post("/change-password")
async def change_password(
    req: ChangePasswordRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """修改密码（需验证旧密码）"""
    if not current_user.verify_password(req.old_password):
        raise HTTPException(status_code=400, detail="旧密码错误")

    if req.old_password == req.new_password:
        raise HTTPException(status_code=400, detail="新密码不能与旧密码相同")

    current_user.set_password(req.new_password)
    await db.flush()

    return {"status": "ok", "message": "密码修改成功"}
