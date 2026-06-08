"""WicMail User Service - FastAPI 入口"""
import traceback
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings
from app.routers import auth, mailbox, emails, admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"🚀 {settings.app_name} 启动中... (env={settings.app_env})")
    print(f"📦 邮箱域名: {settings.mailbox_domain}")
    yield
    print("✅ 服务已关闭")


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(auth.router)
app.include_router(mailbox.router)
app.include_router(emails.router)
app.include_router(admin.router)


@app.get("/health")
async def health_check():
    return {"status": "ok", "app": settings.app_name}
