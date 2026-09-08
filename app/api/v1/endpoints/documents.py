"""文档接口。"""

from typing import Annotated

import fastapi
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.repositories.document import list_documents
from app.schemas.document import DocumentCreate, DocumentResponse, DocumentUpdate
from app.services.document import (
    create_document_for_user,
    delete_document_for_user,
    get_document_for_user,
    update_document_for_user,
)

router = fastapi.APIRouter(prefix="/documents", tags=["documents"])


@router.post(
    "", response_model=DocumentResponse, status_code=fastapi.status.HTTP_201_CREATED
)
async def create_document(
    document_create: DocumentCreate,
    session: Annotated[AsyncSession, fastapi.Depends(get_db)],
    current_user: Annotated[User, fastapi.Depends(get_current_user)],
) -> DocumentResponse:
    """为当前登录用户创建文档记录。"""
    document = await create_document_for_user(session, document_create, current_user)
    return DocumentResponse.model_validate(document)


@router.get("", response_model=list[DocumentResponse])
async def get_documents(
    session: Annotated[AsyncSession, fastapi.Depends(get_db)],
    current_user: Annotated[User, fastapi.Depends(get_current_user)],
) -> list[DocumentResponse]:
    """获取当前用户的文档；管理员可获取全部文档。"""
    documents = await list_documents(session, current_user)
    return [DocumentResponse.model_validate(document) for document in documents]


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: int,
    session: Annotated[AsyncSession, fastapi.Depends(get_db)],
    current_user: Annotated[User, fastapi.Depends(get_current_user)],
) -> DocumentResponse:
    """获取一篇有权限查看的文档。"""
    document = await get_document_for_user(session, document_id, current_user)
    return DocumentResponse.model_validate(document)


@router.patch("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: int,
    document_update: DocumentUpdate,
    session: Annotated[AsyncSession, fastapi.Depends(get_db)],
    current_user: Annotated[User, fastapi.Depends(get_current_user)],
) -> DocumentResponse:
    """修改一篇有权限操作的文档。"""
    document = await update_document_for_user(
        session, document_id, document_update, current_user
    )
    return DocumentResponse.model_validate(document)


@router.delete("/{document_id}", status_code=fastapi.status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: int,
    session: Annotated[AsyncSession, fastapi.Depends(get_db)],
    current_user: Annotated[User, fastapi.Depends(get_current_user)],
) -> None:
    """删除一篇有权限操作的文档。"""
    await delete_document_for_user(session, document_id, current_user)
