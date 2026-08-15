from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProviderCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    provider_type: str = Field(min_length=1, max_length=50)
    base_url: str | None = Field(default=None, max_length=500)
    api_key: str | None = Field(default=None, min_length=1)
    default_model: str | None = Field(default=None, max_length=200)
    enabled: bool = True


class ProviderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    provider_type: str
    base_url: str | None
    default_model: str | None
    enabled: bool
    created_at: datetime
    updated_at: datetime


class ProviderTypeResponse(BaseModel):
    provider_types: list[str]
