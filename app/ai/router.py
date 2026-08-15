from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.schemas import ProviderCreate, ProviderResponse, ProviderTypeResponse
from app.ai.registry import provider_registry
from app.ai.service import AIConfigurationError, AIService
from app.core.database import get_db
from app.core.security import get_current_user
from app.identity.models import User


router = APIRouter(prefix="/ai", tags=["AI"])


@router.get("/provider-types", response_model=ProviderTypeResponse)
async def provider_types() -> ProviderTypeResponse:
    return ProviderTypeResponse(provider_types=list(provider_registry.supported_types()))


@router.get("/providers", response_model=list[ProviderResponse])
async def list_providers(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await AIService(db).list_providers(current_user.id)


@router.post(
    "/providers",
    response_model=ProviderResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_provider(
    data: ProviderCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        return await AIService(db).create_provider(current_user.id, data)
    except AIConfigurationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
