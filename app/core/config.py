from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration.

    Values are loaded from environment variables and .env.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "PAssist"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = False

    # API
    api_prefix: str = "/api"

    # Database
    database_url: str = Field(
        default="sqlite+aiosqlite:///./passist.db"
    )

    # Security
    secret_key: str
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 30

    # Logging
    log_level: str = "INFO"
    log_json: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings() # type: ignore


settings = get_settings()