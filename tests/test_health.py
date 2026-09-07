import pytest
from httpx import ASGITransport, AsyncClient

from app.core.config import settings
from app.main import app


@pytest.mark.anyio
async def test_health_check_returns_ok() -> None:
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(f"{settings.api_v1_prefix}/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
