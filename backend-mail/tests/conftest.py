"""pytest 配置 - 测试用数据库会话和初始化"""
import asyncio

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.config import settings
from app.database import get_db, Base
from app.main import app
from app.models.user import User

# 测试专用引擎：NullPool 避免跨 event loop 连接复用问题
test_engine = create_async_engine(
    settings.database_url,
    poolclass=NullPool,
)

test_session_factory = async_sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


async def override_get_db():
    async with test_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


app.dependency_overrides[get_db] = override_get_db


async def _ensure_test_admin():
    """确保测试数据库中存在 admin 用户"""
    from sqlalchemy import select
    async with test_session_factory() as session:
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


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """确保测试数据库表存在 + 默认管理员"""
    asyncio.get_event_loop().run_until_complete(_ensure_test_admin())
    yield
