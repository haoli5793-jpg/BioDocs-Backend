"""用户登录业务。"""

import fastapi
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_password
from app.models.user import User
from app.repositories.user import get_user_by_email
from app.schemas.user import UserLogin


async def authenticate_user(session: AsyncSession, user_login: UserLogin) -> User:
    """验证邮箱和密码，验证成功后返回对应用户。"""
    user = await get_user_by_email(session, str(user_login.email))
    if user is None or not verify_password(user_login.password, user.password_hash):
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误。",
        )
    return user
