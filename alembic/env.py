"""Alembic 迁移运行配置。"""

import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine, async_engine_from_config

from alembic import context
from app.core.config import settings
from app.db.base import Base
from app.models.document import Document  # noqa: F401
from app.models.user import User  # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

database_url = settings.database_url

if database_url is None:
    raise RuntimeError("执行数据库迁移前必须设置 DATABASE_URL。")

# Alembic 通过 Base.metadata 识别当前项目的所有数据表。
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """生成 SQL 文本，不直接连接数据库。"""
    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """在 Alembic 使用的同步连接中执行迁移步骤。"""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """创建异步数据库连接并执行迁移。"""
    config.set_main_option("sqlalchemy.url", database_url)
    connectable: AsyncEngine = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """以异步方式连接数据库并执行迁移。"""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
