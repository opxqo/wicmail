"""管理员审计日志服务"""
from __future__ import annotations

from typing import Optional

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.admin_log import AdminLog
from app.models.user import User


def get_client_ip(request: Optional[Request]) -> Optional[str]:
    """获取客户端 IP，优先读取反向代理头。"""
    if request is None:
        return None
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip
    return request.client.host if request.client else None


def add_admin_log(
    db: AsyncSession,
    admin: User,
    action: str,
    target_type: str,
    *,
    target_id: Optional[int] = None,
    target_name: Optional[str] = None,
    detail: Optional[str] = None,
    request: Optional[Request] = None,
) -> AdminLog:
    """写入管理员操作审计日志。"""
    log = AdminLog(
        admin_id=admin.id,
        admin_username=admin.username,
        action=action,
        target_type=target_type,
        target_id=target_id,
        target_name=target_name,
        detail=detail,
        ip_address=get_client_ip(request),
    )
    db.add(log)
    return log
