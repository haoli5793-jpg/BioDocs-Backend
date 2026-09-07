from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

if settings.database_url is None:
    raise RuntimeError("初始化数据库连接前必须设置 DATABASE_URL。")


engine = create_async_engine(settings.database_url)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """为一次接口请求提供数据库会话。"""
    async with async_session_factory() as session:
        yield session
