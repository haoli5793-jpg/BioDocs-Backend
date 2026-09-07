"""数据库模型模块。"""

# 运行时加载所有有关联关系的 Model，供 SQLAlchemy 解析 relationship 使用。
from app.models.document import Document  # noqa: F401
from app.models.user import User  # noqa: F401
