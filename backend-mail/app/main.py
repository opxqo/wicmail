"""WicMail Backend - FastAPI 应用入口"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import select

from app.config import settings
from app.database import create_tables, async_session_factory
from app.models.user import User
from app.routers import inbound, emails, auth


async def ensure_default_admin():
    """启动时确保默认管理员存在"""
    async with async_session_factory() as session:
        result = await session.execute(select(User).where(User.username == "admin"))
        user = result.scalar_one_or_none()
        if user is None:
            admin = User(
                username="admin",
                email=None,
                is_active=True,
                is_admin=True,
            )
            admin.set_password("admin123456")
            session.add(admin)
            await session.commit()
            print("✅ 已创建默认管理员账号: admin / admin123456")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期：启动时自动建表 + 创建默认管理员"""
    await create_tables()
    await ensure_default_admin()
    yield


app = FastAPI(
    title=settings.app_name,
    version="0.3.0",
    lifespan=lifespan,
)

app.include_router(inbound.router)
app.include_router(emails.router)
app.include_router(auth.router)


@app.get("/health")
async def health_check():
    return {"status": "ok", "app": settings.app_name}
