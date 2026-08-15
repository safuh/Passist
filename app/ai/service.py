from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.models import Provider
from app.ai.registry import provider_registry
from app.ai.repository import ProviderRepository
from app.ai.schemas import ProviderCreate
from app.core.secrets import decrypt_secret, encrypt_secret


class AIConfigurationError(Exception):
    """Raised when an AI provider configuration is invalid."""


class AIService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.providers = ProviderRepository(db)

    async def list_providers(self, owner_id: int) -> list[Provider]:
        return await self.providers.list_for_owner(owner_id)

    async def create_provider(self, owner_id: int, data: ProviderCreate) -> Provider:
        if data.provider_type not in provider_registry.supported_types():
            raise AIConfigurationError(
                f"Unsupported provider type: {data.provider_type}"
            )

        encrypted_key = encrypt_secret(data.api_key) if data.api_key else None

        provider = await self.providers.create(
            owner_id=owner_id,
            name=data.name.strip(),
            provider_type=data.provider_type,
            base_url=data.base_url,
            api_key_encrypted=encrypted_key,
            default_model=data.default_model,
            enabled=data.enabled,
        )

        await self.db.commit()
        return provider

    async def get_runtime_provider(self, provider: Provider):
        if not provider.enabled:
            raise AIConfigurationError("AI provider is disabled.")

        api_key = (
            decrypt_secret(provider.api_key_encrypted)
            if provider.api_key_encrypted
            else None
        )

        return provider_registry.create(
            provider.provider_type,
            base_url=provider.base_url,
            api_key=api_key,
        )
