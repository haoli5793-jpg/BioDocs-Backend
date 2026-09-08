"""文档业务和权限判断。"""

import fastapi
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document
from app.models.user import User
from app.repositories.document import (
    create_document,
    get_document_by_id,
)
from app.schemas.document import DocumentCreate, DocumentUpdate


async def create_document_for_user(
    session: AsyncSession, document_create: DocumentCreate, current_user: User
) -> Document:
    """为当前用户创建一条文档记录。"""
    document = create_document(
        session,
        title=document_create.title,
        description=document_create.description,
        file_path=document_create.file_path,
        owner_id=current_user.id,
    )
    await session.commit()
    await session.refresh(document)
    return document


async def get_document_for_user(
    session: AsyncSession, document_id: int, current_user: User
) -> Document:
    """获取文档，并判断当前用户是否有查看权限。"""
    document = await get_document_by_id(session, document_id)
    if document is None:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="文档不存在。",
        )

    if not current_user.is_admin and document.owner_id != current_user.id:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_403_FORBIDDEN,
            detail="你没有操作此文档的权限。",
        )
    return document


async def update_document_for_user(
    session: AsyncSession,
    document_id: int,
    document_update: DocumentUpdate,
    current_user: User,
) -> Document:
    """修改当前用户有权限操作的文档。"""
    document = await get_document_for_user(session, document_id, current_user)
    update_data = document_update.model_dump(exclude_unset=True)
    if not update_data:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="至少需要提供一个要修改的字段。",
        )

    for field, value in update_data.items():
        setattr(document, field, value)

    await session.commit()
    await session.refresh(document)
    return document


async def delete_document_for_user(
    session: AsyncSession, document_id: int, current_user: User
) -> None:
    """删除当前用户有权限操作的文档。"""
    document = await get_document_for_user(session, document_id, current_user)
    await session.delete(document)
    await session.commit()
