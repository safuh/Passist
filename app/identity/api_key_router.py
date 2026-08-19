from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.identity.api_key_schemas import (
    APIKeyCreateRequest,
    APIKeyCreateResponse,
    APIKeyResponse,
)
from app.identity.api_keys import issue_api_key
from app.identity.authorization import require_permission
from app.identity.models import APIKey, User
from app.identity.permissions import Permission

router = APIRouter(prefix="/auth/api-keys", tags=["API Keys"])


@router.post(
    "",
    response_model=APIKeyCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_api_key(
    data: APIKeyCreateRequest,
    current_user: User = Depends(require_permission(Permission.API_KEYS_CREATE)),
    db: AsyncSession = Depends(get_db),
):
    if data.expires_at is not None and data.expires_at <= datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="API key expiration must be in the future.",
        )

    record, raw_key = await issue_api_key(
        db,
        user_id=current_user.id,
        name=data.name,
        expires_at=data.expires_at,
    )
    await db.commit()

    return APIKeyCreateResponse(
        id=record.id,
        name=record.name,
        key_prefix=record.key_prefix,
        api_key=raw_key,
        expires_at=record.expires_at,
    )


@router.get("", response_model=list[APIKeyResponse])
async def list_api_keys(
    current_user: User = Depends(require_permission(Permission.API_KEYS_READ)),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(APIKey)
        .where(APIKey.user_id == current_user.id)
        .order_by(APIKey.created_at.desc())
    )
    return [APIKeyResponse.from_model(value) for value in result.scalars().all()]


@router.post("/{key_id}/revoke", response_model=APIKeyResponse)
async def revoke_api_key(
    key_id: int,
    current_user: User = Depends(require_permission(Permission.API_KEYS_REVOKE)),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(APIKey).where(
            APIKey.id == key_id,
            APIKey.user_id == current_user.id,
        )
    )
    record = result.scalar_one_or_none()

    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API key not found.")

    if record.revoked_at is None:
        record.revoked_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(record)

    return APIKeyResponse.from_model(record)
