"""用户表的数据库读写。"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    """按邮箱查询用户。"""
    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    """按用户 ID 查询用户。"""
    return await session.get(User, user_id)


def create_user(session: AsyncSession, email: str, password_hash: str) -> User:
    """创建用户对象并加入当前数据库会话。"""
    user = User(email=email, password_hash=password_hash)
    session.add(user)
    return user
