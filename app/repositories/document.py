"""文档表的数据库读写。"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document
from app.models.user import User


def create_document(
    session: AsyncSession,
    *,
    title: str,
    description: str | None,
    file_path: str | None,
    owner_id: int,
) -> Document:
    """创建文档对象并加入当前数据库会话。"""
    document = Document(
        title=title,
        description=description,
        file_path=file_path,
        owner_id=owner_id,
    )
    session.add(document)
    return document


async def get_document_by_id(
    session: AsyncSession, document_id: int
) -> Document | None:
    """按文档 ID 查询文档。"""
    return await session.get(Document, document_id)


async def list_documents(session: AsyncSession, user: User) -> list[Document]:
    """普通用户只查自己的文档，管理员可查全部文档。"""
    statement = select(Document).order_by(Document.id.desc())
    if not user.is_admin:
        statement = statement.where(Document.owner_id == user.id)

    result = await session.execute(statement)
    return list(result.scalars().all())
