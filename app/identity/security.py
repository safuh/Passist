import hashlib
import secrets
from datetime import datetime, timedelta, timezone

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from app.core.config import settings


password_hasher = PasswordHasher()

JWT_ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(
    password: str,
    password_hash: str,
) -> bool:
    try:
        return password_hasher.verify(
            password_hash,
            password,
        )
    except VerifyMismatchError:
        return False


def create_access_token(
    user_id: int,
) -> str:
    now = datetime.now(timezone.utc)

    expires = now + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {
        "sub": str(user_id),
        "type": "access",
        "iat": now,
        "exp": expires,
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> dict:
    return jwt.decode(
        token,
        settings.secret_key,
        algorithms=[JWT_ALGORITHM],
    )


def create_refresh_token() -> str:
    return secrets.token_urlsafe(64)


def hash_token(token: str) -> str:
    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()


def create_api_key() -> tuple[str, str, str]:
    """
    Returns:
        raw_key
        prefix
        hash
    """

    random_part = secrets.token_urlsafe(32)

    raw_key = f"pa_{random_part}"

    prefix = raw_key[:12]

    key_hash = hash_token(raw_key)

    return raw_key, prefix, key_hash