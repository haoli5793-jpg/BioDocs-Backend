"""文档接口的数据格式。"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DocumentCreate(BaseModel):
    """创建文档记录时客户端提交的数据。"""

    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    file_path: str | None = Field(default=None, max_length=512)


class DocumentUpdate(BaseModel):
    """修改文档记录时允许提交的数据。"""

    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    file_path: str | None = Field(default=None, max_length=512)


class DocumentResponse(BaseModel):
    """接口返回给客户端的文档信息。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    file_path: str | None
    status: str
    owner_id: int
    created_at: datetime
    updated_at: datetime
