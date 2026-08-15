import structlog
from fastapi import FastAPI

from app.ai.router import router as ai_router
from app.core.config import settings
from app.core.lifespan import lifespan
from app.core.logging import configure_logging
from app.identity.router import router as identity_router


configure_logging()
logger = structlog.get_logger()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.include_router(identity_router, prefix=settings.api_prefix)
app.include_router(ai_router, prefix=settings.api_prefix)


@app.get("/health", tags=["System"])
async def health() -> dict[str, str]:
    return {
        "status": "ok",
        "application": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }


logger.info(
    "application_initialized",
    application=settings.app_name,
    environment=settings.environment,
)
