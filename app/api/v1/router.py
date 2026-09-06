import fastapi

from app.api.v1.endpoints.health import router as health_router

api_router = fastapi.APIRouter()
api_router.include_router(health_router)
