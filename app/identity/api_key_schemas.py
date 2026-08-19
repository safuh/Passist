from datetime import datetime

from pydantic import BaseModel, Field


class APIKeyCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    expires_at: datetime | None = None


class APIKeyCreateResponse(BaseModel):
    id: int
    name: str
    key_prefix: str
    api_key: str
    expires_at: datetime | None


class APIKeyResponse(BaseModel):
    id: int
    name: str
    key_prefix: str
    created_at: datetime
    last_used_at: datetime | None
    expires_at: datetime | None
    revoked_at: datetime | None

    @classmethod
    def from_model(cls, value):
        return cls(
            id=value.id,
            name=value.name,
            key_prefix=value.key_prefix,
            created_at=value.created_at,
            last_used_at=value.last_used_at,
            expires_at=value.expires_at,
            revoked_at=value.revoked_at,
        )
