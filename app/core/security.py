from datetime import datetime, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.identity.models import APIKey, Role, User
from app.identity.security import decode_access_token, hash_token


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login",
    auto_error=False,
)
api_key_scheme = APIKeyHeader(name="X-API-Key", auto_error=False)


async def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    api_key: str | None = Depends(api_key_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Resolve the authenticated principal from JWT bearer or API key."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate authentication credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user_id: int | None = None

    if token:
        try:
            payload = decode_access_token(token)
            if payload.get("type") != "access":
                raise credentials_exception
            subject = payload.get("sub")
            if subject is None:
                raise credentials_exception
            user_id = int(subject)
        except (InvalidTokenError, ValueError, TypeError):
            raise credentials_exception

    elif api_key:
        result = await db.execute(
            select(APIKey).where(APIKey.key_hash == hash_token(api_key))
        )
        record = result.scalar_one_or_none()
        now = datetime.now(timezone.utc)
        if (
            record is None
            or record.revoked_at is not None
            or (record.expires_at is not None and record.expires_at <= now)
        ):
            raise credentials_exception
        record.last_used_at = now
        user_id = record.user_id
    else:
        raise credentials_exception

    result = await db.execute(
        select(User)
        .options(selectinload(User.roles).selectinload(Role.permissions))
        .where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive.",
        )

    if api_key:
        await db.commit()

    return user
