from datetime import datetime, timedelta, timezone

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.identity.repository import (
    RoleRepository,
    SessionRepository,
    UserRepository,
)
from app.identity.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    hash_token,
    verify_password,
)
from app.identity.models import User


class AuthenticationError(Exception):
    """Raised when authentication fails."""


class RegistrationError(Exception):
    """Raised when user registration fails."""


class AuthenticationService:
    def __init__(self, db: AsyncSession):
        self.db = db

        self.users = UserRepository(db)
        self.roles = RoleRepository(db)
        self.sessions = SessionRepository(db)

    async def register(
        self,
        *,
        email: str,
        username: str | None,
        password: str,
    ) -> User:
        email = email.strip().lower()

        if username:
            username = username.strip()

        existing_email = await self.users.get_by_email(email)

        if existing_email is not None:
            raise RegistrationError(
                "An account with this email already exists."
            )

        if username:
            existing_username = await self.users.get_by_username(
                username
            )

            if existing_username is not None:
                raise RegistrationError(
                    "This username is already in use."
                )

        password_hash = hash_password(password)

        try:
            user = await self.users.create(
                email=email,
                username=username,
                password_hash=password_hash,
            )

            # Default role assignment.
            role = await self.roles.get_by_name("user")

            if role is not None:
                user.roles.append(role)

            await self.db.commit()

            await self.db.refresh(user)

            return user

        except IntegrityError:
            await self.db.rollback()

            raise RegistrationError(
                "Unable to create account."
            )

    async def authenticate(
        self,
        *,
        email: str,
        password: str,
        user_agent: str | None = None,
        ip_address: str | None = None,
    ) -> tuple[str, str, int]:

        email = email.strip().lower()

        user = await self.users.get_by_email(email)

        if user is None:
            raise AuthenticationError(
                "Invalid email or password."
            )

        if not user.is_active:
            raise AuthenticationError(
                "This account is inactive."
            )

        if user.password_hash is None:
            raise AuthenticationError(
                "This account does not use password authentication."
            )

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise AuthenticationError(
                "Invalid email or password."
            )

        access_token = create_access_token(user.id)

        refresh_token = create_refresh_token()

        refresh_token_hash = hash_token(refresh_token)

        now = datetime.now(timezone.utc)

        expires_at = now + timedelta(
            days=settings.refresh_token_expire_days
        )

        await self.sessions.create(
            user_id=user.id,
            refresh_token_hash=refresh_token_hash,
            expires_at=expires_at,
            user_agent=user_agent,
            ip_address=ip_address,
        )

        await self.db.commit()

        return (
            access_token,
            refresh_token,
            settings.access_token_expire_minutes * 60,
        )

    async def refresh(
        self,
        *,
        refresh_token: str,
        user_agent: str | None = None,
        ip_address: str | None = None,
    ) -> tuple[str, str, int]:

        token_hash = hash_token(refresh_token)

        session = await self.sessions.get_by_refresh_token_hash(
            token_hash
        )

        if session is None:
            raise AuthenticationError(
                "Invalid refresh token."
            )

        now = datetime.now(timezone.utc)

        if session.revoked_at is not None:
            raise AuthenticationError(
                "Refresh token has been revoked."
            )

        if session.expires_at <= now:
            raise AuthenticationError(
                "Refresh token has expired."
            )

        user = await self.users.get_by_id(session.user_id)

        if user is None or not user.is_active:
            raise AuthenticationError(
                "User account is unavailable."
            )

        # Rotate the refresh token.
        await self.sessions.revoke(
            session,
            revoked_at=now,
        )

        new_refresh_token = create_refresh_token()

        new_refresh_token_hash = hash_token(
            new_refresh_token
        )

        new_expires_at = now + timedelta(
            days=settings.refresh_token_expire_days
        )

        await self.sessions.create(
            user_id=user.id,
            refresh_token_hash=new_refresh_token_hash,
            expires_at=new_expires_at,
            user_agent=user_agent,
            ip_address=ip_address,
        )

        new_access_token = create_access_token(user.id)

        await self.db.commit()

        return (
            new_access_token,
            new_refresh_token,
            settings.access_token_expire_minutes * 60,
        )

    async def logout(
        self,
        *,
        refresh_token: str,
    ) -> None:

        token_hash = hash_token(refresh_token)

        session = await self.sessions.get_by_refresh_token_hash(
            token_hash
        )

        if session is None:
            # Logout should be idempotent.
            return

        if session.revoked_at is None:
            await self.sessions.revoke(
                session,
                revoked_at=datetime.now(timezone.utc),
            )

        await self.db.commit()