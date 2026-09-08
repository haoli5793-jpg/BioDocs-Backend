"""认证接口。"""

from typing import Annotated

import fastapi
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token
from app.db.session import get_db
from app.schemas.user import TokenResponse, UserLogin
from app.services.auth import authenticate_user

router = fastapi.APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(
    user_login: UserLogin,
    session: Annotated[AsyncSession, fastapi.Depends(get_db)],
) -> TokenResponse:
    """验证账号密码并返回访问令牌。"""
    user = await authenticate_user(session, user_login)
    return TokenResponse(access_token=create_access_token(user.id))
