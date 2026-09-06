from fastapi import APIRouter, status

router = APIRouter(tags=["health"])


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> dict[str, str]:
    """返回 FastAPI 应用的存活状态。"""
    return {"status": "ok"}
