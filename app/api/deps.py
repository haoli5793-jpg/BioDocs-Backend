"""多个接口共用的依赖项。"""

from typing import Annotated

import fastapi
import jwt
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User
from app.repositories.user import get_user_by_id

bearer_scheme = HTTPBearer(auto_error=False)


def _credentials_exception() -> fastapi.HTTPException:
    """生成统一的未登录或令牌无效响应。"""
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
        detail="登录状态无效或已过期。",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_user(
    session: Annotated[AsyncSession, fastapi.Depends(get_db)],
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        fastapi.Depends(bearer_scheme),
    ],
) -> User:
    """从 Bearer Token 中解析出当前登录用户。"""
    if credentials is None:
        raise _credentials_exception()

    try:
        payload = decode_access_token(credentials.credentials)
        user_id = int(payload["sub"])
    except (jwt.PyJWTError, KeyError, TypeError, ValueError):
        raise _credentials_exception() from None

    user = await get_user_by_id(session, user_id)
    if user is None:
        raise _credentials_exception()
    return user
