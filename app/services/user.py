"""用户注册业务。"""

import fastapi
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.user import User
from app.repositories.user import create_user, get_user_by_email
from app.schemas.user import UserCreate


async def register_user(session: AsyncSession, user_create: UserCreate) -> User:
    """校验用户邮箱、哈希密码并保存用户。"""
    email = str(user_create.email)
    existing_user = await get_user_by_email(session, email)

    if existing_user is not None:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_409_CONFLICT,
            detail="该邮箱已被注册。",
        )

    user = create_user(
        session,
        email=email,
        password_hash=hash_password(user_create.password),
    )

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_409_CONFLICT,
            detail="该邮箱已被注册。",
        ) from None

    await session.refresh(user)
    return user
