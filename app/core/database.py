from collections.abc import AsyncGenerator
from datetime import datetime, timezone

from sqlalchemy import DateTime, TypeDecorator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.
    """

    pass

class UTCDateTime(TypeDecorator[datetime]):
    """
    Stores UTC datetimes.

    PostgreSQL:
        Uses TIMESTAMP WITH TIME ZONE.

    SQLite:
        Stores the datetime representation but may return
        it without timezone information, so we normalize
        it back to UTC when reading.
    """

    impl = DateTime(timezone=True)
    cache_ok = True

    def process_bind_param(
        self,
        value: datetime | None,
        dialect,
    ) -> datetime | None:

        if value is None:
            return None

        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)

        return value.astimezone(timezone.utc)

    def process_result_value(
        self,
        value: datetime | None,
        dialect,
    ) -> datetime | None:

        if value is None:
            return None

        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)

        return value.astimezone(timezone.utc)

engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
)


AsyncSessionFactory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that provides a database session.
    """

    async with AsyncSessionFactory() as session:
        yield session