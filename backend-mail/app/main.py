"""WicMail Backend - FastAPI 应用入口"""
import traceback
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import select

from app.config import settings
from app.database import create_tables, async_session_factory
from app.models.user import User
from app.routers import inbound, emails, auth


async def ensure_default_admin():
    """启动时确保默认管理员存在"""
    try:
        async with async_session_factory() as session:
            result = await session.execute(select(User).where(User.username == settings.default_admin_username))
            user = result.scalar_one_or_none()
            if user is None:
                admin = User(
                    username=settings.default_admin_username,
                    email=None,
                    is_active=True,
                    is_admin=True,
                )
                admin.set_password(settings.default_admin_password)
                session.add(admin)
                await session.commit()
                print(f"✅ 已创建默认管理员账号: {settings.default_admin_username}")
            else:
                print(f"✅ 管理员账号已存在: {settings.default_admin_username}")
    except Exception as e:
        print(f"⚠️ 创建管理员失败: {e}")
        traceback.print_exc()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期：启动时自动建表 + 创建默认管理员"""
    print(f"🚀 WicMail Backend 启动中... (env={settings.app_env})")
    print(f"📦 DATABASE_URL={settings.database_url[:50]}...")

    try:
        print("📋 创建数据库表...")
        await create_tables()
        print("✅ 数据库表创建成功")
    except Exception as e:
        print(f"❌ 数据库表创建失败: {e}")
        traceback.print_exc()
        # 不抛出异常，让服务继续启动，只是数据库功能不可用

    try:
        print("👤 检查默认管理员...")
        await ensure_default_admin()
    except Exception as e:
        print(f"⚠️ 管理员检查失败: {e}")
        traceback.print_exc()

    print("✅ WicMail Backend 启动完成")
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
