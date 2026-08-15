from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.models import Provider


class ProviderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_for_owner(self, owner_id: int) -> list[Provider]:
        result = await self.db.execute(
            select(Provider)
            .where(Provider.owner_id == owner_id)
            .order_by(Provider.name)
        )
        return list(result.scalars().all())

    async def get_for_owner(self, provider_id: int, owner_id: int) -> Provider | None:
        result = await self.db.execute(
            select(Provider).where(
                Provider.id == provider_id,
                Provider.owner_id == owner_id,
            )
        )
        return result.scalar_one_or_none()

    async def create(
        self,
        *,
        owner_id: int,
        name: str,
        provider_type: str,
        base_url: str | None,
        api_key_encrypted: str | None,
        default_model: str | None,
        enabled: bool,
    ) -> Provider:
        provider = Provider(
            owner_id=owner_id,
            name=name,
            provider_type=provider_type,
            base_url=base_url,
            api_key_encrypted=api_key_encrypted,
            default_model=default_model,
            enabled=enabled,
        )
        self.db.add(provider)
        await self.db.flush()
        await self.db.refresh(provider)
        return provider
