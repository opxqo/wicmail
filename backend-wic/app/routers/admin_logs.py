"""管理员路由 - 操作日志"""
import csv
import io
from datetime import datetime, timedelta
from typing import Optional, List

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.models.admin_log import AdminLog
from app.services.auth import get_admin_user

router = APIRouter(prefix="/api/admin/logs", tags=["管理员-日志"])


class LogResponse(BaseModel):
    id: int
    admin_id: int
    admin_username: str
    action: str
    target_type: str
    target_id: Optional[int] = None
    target_name: Optional[str] = None
    detail: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class LogListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    logs: List[LogResponse]


@router.get("", response_model=LogListResponse)
async def list_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    action: Optional[str] = Query(None),
    target_type: Optional[str] = Query(None),
    admin_username: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None, description="开始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD"),
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    """日志列表"""
    conditions = []
    if action:
        conditions.append(AdminLog.action == action)
    if target_type:
        conditions.append(AdminLog.target_type == target_type)
    if admin_username:
        conditions.append(AdminLog.admin_username.like(f"%{admin_username}%"))
    if start_date:
        conditions.append(AdminLog.created_at >= datetime.strptime(start_date, "%Y-%m-%d"))
    if end_date:
        conditions.append(AdminLog.created_at < datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1))

    where_clause = and_(*conditions) if conditions else True

    total = (await db.execute(
        select(func.count(AdminLog.id)).where(where_clause)
    )).scalar() or 0

    offset = (page - 1) * page_size
    result = await db.execute(
        select(AdminLog).where(where_clause)
        .order_by(AdminLog.created_at.desc())
        .offset(offset).limit(page_size)
    )
    logs = result.scalars().all()

    return LogListResponse(
        total=total, page=page, page_size=page_size,
        logs=[LogResponse.model_validate(l) for l in logs],
    )


@router.get("/export")
async def export_logs(
    action: Optional[str] = Query(None),
    target_type: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    """导出日志（CSV）"""
    conditions = []
    if action:
        conditions.append(AdminLog.action == action)
    if target_type:
        conditions.append(AdminLog.target_type == target_type)
    if start_date:
        conditions.append(AdminLog.created_at >= datetime.strptime(start_date, "%Y-%m-%d"))
    if end_date:
        conditions.append(AdminLog.created_at < datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1))

    where_clause = and_(*conditions) if conditions else True

    result = await db.execute(
        select(AdminLog).where(where_clause)
        .order_by(AdminLog.created_at.desc())
        .limit(10000)
    )
    logs = result.scalars().all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "操作人", "操作类型", "目标类型", "目标ID", "目标名称", "详情", "IP", "时间"])
    for l in logs:
        writer.writerow([l.id, l.admin_username, l.action, l.target_type, l.target_id, l.target_name, l.detail, l.ip_address, l.created_at])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=admin_logs_{datetime.utcnow().strftime('%Y%m%d')}.csv"},
    )


@router.get("/{log_id}", response_model=LogResponse)
async def get_log_detail(
    log_id: int,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    """日志详情"""
    result = await db.execute(select(AdminLog).where(AdminLog.id == log_id))
    log = result.scalar_one_or_none()
    if log is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="日志不存在")
    return LogResponse.model_validate(log)
