"""用户接口。"""

from typing import Annotated

import fastapi
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user import register_user as register_user_service

router = fastapi.APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse, status_code=fastapi.status.HTTP_201_CREATED)
async def register_user(
    user_create: UserCreate,
    session: Annotated[AsyncSession, fastapi.Depends(get_db)],
) -> UserResponse:
    """注册新用户。"""
    user = await register_user_service(session, user_create)
    return UserResponse.model_validate(user)
    
