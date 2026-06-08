"""入站邮件接收接口"""
import base64

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.schemas.inbound import CloudflareInboundEmail, ParsedEmail
from app.services.mail_parser import parse_raw_email
from app.services.email_storage import save_inbound_email

router = APIRouter()


@router.post("/api/inbound/cloudflare")
async def receive_inbound_email(
    payload: CloudflareInboundEmail,
    x_secret_key: str = Header(..., alias="X-Secret-Key"),
    db: AsyncSession = Depends(get_db),
):
    # 校验密钥
    if x_secret_key != settings.cloudflare_email_secret_key:
        raise HTTPException(status_code=403, detail="Invalid secret key")

    # raw 过大，仅元数据模式
    if payload.raw_too_large and not payload.raw:
        email_msg, is_new = await save_inbound_email(db, payload)
        return {
            "status": "metadata_only",
            "request_id": payload.request_id,
            "raw_too_large": True,
            "email_id": email_msg.id,
            "is_new": is_new,
        }

    # 解码并解析 raw 邮件
    if not payload.raw:
        email_msg, is_new = await save_inbound_email(db, payload)
        return {
            "status": "no_raw",
            "request_id": payload.request_id,
            "raw_too_large": payload.raw_too_large,
            "email_id": email_msg.id,
            "is_new": is_new,
        }

    try:
        if payload.raw_encoding == "base64":
            raw_bytes = base64.b64decode(payload.raw)
        else:
            raw_bytes = payload.raw.encode("utf-8")

        parsed = parse_raw_email(raw_bytes)

        # 入库
        email_msg, is_new = await save_inbound_email(db, payload, parsed)

        return {
            "status": "ok",
            "request_id": payload.request_id,
            "raw_too_large": payload.raw_too_large,
            "email_id": email_msg.id,
            "is_new": is_new,
            "parsed": parsed.model_dump(by_alias=True),
        }
    except Exception as e:
        # 解析失败也保存元数据
        email_msg, _ = await save_inbound_email(
            db, payload, parse_error=str(e)
        )
        raise HTTPException(
            status_code=422,
            detail={
                "error": f"邮件解析失败: {e}",
                "email_id": email_msg.id,
            },
        )
