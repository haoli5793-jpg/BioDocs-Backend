"""密码安全相关工具。"""

from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from pwdlib import PasswordHash

from app.core.config import settings

password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """将明文密码转换为不可逆的哈希值。"""
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """校验明文密码是否与数据库中的哈希值匹配。"""
    return password_hasher.verify(password, password_hash)


def _get_jwt_secret_key() -> str:
    """获取签发和校验 JWT 所需的密钥。"""
    if settings.jwt_secret_key is None:
        raise RuntimeError("使用 JWT 前必须设置 JWT_SECRET_KEY。")
    return settings.jwt_secret_key


def create_access_token(user_id: int) -> str:
    """为指定用户创建有过期时间的访问令牌。"""
    now = datetime.now(UTC)
    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(minutes=settings.access_token_expire_minutes),
    }
    return jwt.encode(
        payload,
        _get_jwt_secret_key(),
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> dict[str, Any]:
    """校验并解析访问令牌。令牌无效或过期时会抛出异常。"""
    return jwt.decode(
        token,
        _get_jwt_secret_key(),
        algorithms=[settings.jwt_algorithm],
    )
