from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(title=settings.app_name, version="0.1.0")

# 将版本化 API 路由注册到 FastAPI 应用。
app.include_router(api_router, prefix=settings.api_v1_prefix)
