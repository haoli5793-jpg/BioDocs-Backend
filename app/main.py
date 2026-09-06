from fastapi import FastAPI

from app.api.v1.router import api_router

app = FastAPI(title="BioDocs Backend", version="0.1.0")

# 将版本化 API 路由注册到 FastAPI 应用。
app.include_router(api_router, prefix="/api/v1")