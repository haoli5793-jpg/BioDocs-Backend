"""认证安全工具的基础测试。"""

from app.core.config import settings
from app.core.security import create_access_token, decode_access_token


def test_create_access_token_contains_user_id(monkeypatch) -> None:
    """签发的令牌应能解析出对应的用户 ID。"""
    monkeypatch.setattr(settings, "jwt_secret_key", "test-secret-key-at-least-32-bytes")

    token = create_access_token(user_id=123)
    payload = decode_access_token(token)

    assert payload["sub"] == "123"
    assert "exp" in payload
