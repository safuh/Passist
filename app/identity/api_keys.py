"""API-key lifecycle and authentication."""

from datetime import datetime, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.identity.models import APIKey, User
from app.identity.security import create_api_key, hash_token

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def get_current_user_from_api_key(
    raw_key: str | None = Depends(api_key_header),
    db: AsyncSession = Depends(get_db),
) -> User:
    if not raw_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is required.",
        )

    result = await db.execute(
        select(APIKey)
        .where(APIKey.key_hash == hash_token(raw_key))
    )
    api_key = result.scalar_one_or_none()

    now = datetime.now(timezone.utc)
    if (
        api_key is None
        or api_key.revoked_at is not None
        or (api_key.expires_at is not None and api_key.expires_at <= now)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired API key.",
        )

    api_key.last_used_at = now
    user_result = await db.execute(select(User).where(User.id == api_key.user_id))
    user = user_result.scalar_one_or_none()

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key owner is unavailable.",
        )

    await db.commit()
    return user


async def issue_api_key(
    db: AsyncSession,
    *,
    user_id: int,
    name: str,
    expires_at: datetime | None = None,
) -> tuple[APIKey, str]:
    raw_key, prefix, key_hash = create_api_key()
    record = APIKey(
        user_id=user_id,
        name=name,
        key_prefix=prefix,
        key_hash=key_hash,
        expires_at=expires_at,
    )
    db.add(record)
    await db.flush()
    await db.refresh(record)
    return record, raw_key
