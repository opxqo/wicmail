"""管理员路由 - 系统配置"""
import asyncio
import socket
from typing import Optional, List, Dict

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.models.system_config import SystemConfig
from app.services.auth import get_admin_user

router = APIRouter(prefix="/api/admin/config", tags=["管理员-配置"])

# 默认配置项
DEFAULT_CONFIGS = {
    "mailbox_domain": ("wic.edu.kg", "邮箱域名"),
    "application_enabled": ("true", "是否开放申请"),
    "max_mailboxes_per_user": ("3", "每人最大邮箱数"),
    "max_attachment_size_mb": ("10", "单附件大小限制(MB)"),
    "application_require_profile": ("true", "申请前是否需完善资料"),
}


class ConfigItem(BaseModel):
    key: str
    value: str
    description: Optional[str] = None


class ConfigUpdateRequest(BaseModel):
    configs: Dict[str, str]


async def _ensure_defaults(db: AsyncSession):
    """确保默认配置存在"""
    result = await db.execute(select(SystemConfig))
    existing = {c.key for c in result.scalars().all()}
    for key, (value, desc) in DEFAULT_CONFIGS.items():
        if key not in existing:
            db.add(SystemConfig(key=key, value=value, description=desc))
    await db.flush()


@router.get("", response_model=List[ConfigItem])
async def get_config(
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    """获取当前配置"""
    await _ensure_defaults(db)
    result = await db.execute(select(SystemConfig).order_by(SystemConfig.key))
    configs = result.scalars().all()
    return [ConfigItem(key=c.key, value=c.value, description=c.description) for c in configs]


@router.patch("")
async def update_config(
    req: ConfigUpdateRequest,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    """更新配置"""
    await _ensure_defaults(db)
    updated = []
    for key, value in req.configs.items():
        result = await db.execute(select(SystemConfig).where(SystemConfig.key == key))
        config = result.scalar_one_or_none()
        if config is None:
            raise HTTPException(status_code=400, detail=f"未知配置项: {key}")
        config.value = value
        updated.append(key)
    await db.flush()
    return {"status": "ok", "updated": updated}


@router.post("/test-cloudflare")
async def test_cloudflare(
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    """测试 Cloudflare Email Worker 连通性"""
    import httpx
    from app.config import settings

    # 通过 Cloudflare Email Routing 发一封测试邮件到 backend-mail
    test_email = f"healthcheck@{settings.mailbox_domain}"
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            # 模拟 Cloudflare Worker 转发请求到 backend-mail
            resp = await client.post(
                "http://localhost:8000/api/inbound/cloudflare",
                headers={
                    "X-Secret-Key": settings.cloudflare_email_secret_key if hasattr(settings, "cloudflare_email_secret_key") else "test",
                    "Content-Type": "application/json",
                },
                json={
                    "from": f"test@{settings.mailbox_domain}",
                    "to": test_email,
                    "subject": "Health Check",
                    "text": "This is a health check email.",
                },
            )
            if resp.status_code in (200, 201):
                return {"status": "ok", "message": "Cloudflare Email Worker 服务可达", "data": resp.json()}
            return {"status": "warning", "message": f"服务返回状态码: {resp.status_code}", "detail": resp.text[:500]}
    except Exception as e:
        return {"status": "error", "message": f"无法连接邮件服务: {str(e)}"}


@router.get("/domain-check")
async def domain_check(
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    """检查域名 DNS 状态"""
    await _ensure_defaults(db)
    result = await db.execute(select(SystemConfig).where(SystemConfig.key == "mailbox_domain"))
    config = result.scalar_one_or_none()
    domain = config.value if config else "wic.edu.kg"

    checks = {}

    # 同步 DNS 查询包装为异步
    def _resolve_mx():
        import dns.resolver
        answers = dns.resolver.resolve(domain, "MX")
        return [f"{r.preference} {r.exchange}" for r in answers]

    def _resolve_a():
        import dns.resolver
        answers = dns.resolver.resolve(domain, "A")
        return [str(r) for r in answers]

    def _resolve_ip():
        return socket.gethostbyname(domain)

    # MX 记录
    try:
        checks["mx"] = await asyncio.to_thread(_resolve_mx)
    except Exception as e:
        checks["mx"] = f"查询失败: {str(e)}"

    # A 记录
    try:
        checks["a"] = await asyncio.to_thread(_resolve_a)
    except Exception as e:
        checks["a"] = f"查询失败: {str(e)}"

    # 基础连通性
    try:
        ip = await asyncio.to_thread(_resolve_ip)
        checks["resolved_ip"] = ip
    except Exception:
        checks["resolved_ip"] = "解析失败"

    return {"domain": domain, "checks": checks}
