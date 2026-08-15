from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.identity.models import APIKey, Role, Session, User
from sqlalchemy.orm import selectinload

class UserRepository:
    """Persistence operations for users."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(
            select(User)
            .options(
                selectinload(User.roles)
                .selectinload(Role.permissions)
            )
            .where(User.id == user_id)
        )

        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> User | None:
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    async def create(
        self,
        *,
        email: str,
        username: str | None,
        password_hash: str,
    ) -> User:
        user = User(
            email=email,
            username=username,
            password_hash=password_hash,
        )

        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)

        return user

    async def save(self, user: User) -> User:
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)

        return user


class RoleRepository:
    """Persistence operations for roles."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_name(self, name: str) -> Role | None:
        result = await self.db.execute(
            select(Role).where(Role.name == name)
        )
        return result.scalar_one_or_none()


class SessionRepository:
    """Persistence operations for authentication sessions."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        *,
        user_id: int,
        refresh_token_hash: str,
        expires_at: datetime,
        user_agent: str | None = None,
        ip_address: str | None = None,
    ) -> Session:
        session = Session(
            user_id=user_id,
            refresh_token_hash=refresh_token_hash,
            expires_at=expires_at,
            user_agent=user_agent,
            ip_address=ip_address,
        )

        self.db.add(session)
        await self.db.flush()
        await self.db.refresh(session)

        return session

    async def get_by_refresh_token_hash(
        self,
        token_hash: str,
    ) -> Session | None:
        result = await self.db.execute(
            select(Session).where(
                Session.refresh_token_hash == token_hash
            )
        )

        return result.scalar_one_or_none()

    async def revoke(
        self,
        session: Session,
        *,
        revoked_at: datetime,
    ) -> Session:
        session.revoked_at = revoked_at

        self.db.add(session)
        await self.db.flush()
        await self.db.refresh(session)

        return session


class APIKeyRepository:
    """Persistence operations for API keys."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_hash(self, key_hash: str) -> APIKey | None:
        result = await self.db.execute(
            select(APIKey).where(
                APIKey.key_hash == key_hash
            )
        )

        return result.scalar_one_or_none()

    async def create(
        self,
        *,
        user_id: int,
        name: str,
        key_prefix: str,
        key_hash: str,
        expires_at: datetime | None = None,
    ) -> APIKey:
        api_key = APIKey(
            user_id=user_id,
            name=name,
            key_prefix=key_prefix,
            key_hash=key_hash,
            expires_at=expires_at,
        )

        self.db.add(api_key)
        await self.db.flush()
        await self.db.refresh(api_key)

        return api_key