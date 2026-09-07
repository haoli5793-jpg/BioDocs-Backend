"""密码安全相关工具。"""

from pwdlib import PasswordHash

password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """将明文密码转换为不可逆的哈希值。"""
    return password_hasher.hash(password)
