"""Reusable role and permission authorization dependencies."""

from collections.abc import Callable

from fastapi import Depends, HTTPException, status

from app.core.security import get_current_user
from app.identity.models import User
from app.identity.permissions import Permission


def has_permission(user: User, permission: Permission | str) -> bool:
    """Return whether a user has the requested permission through any role."""
    required = str(permission)
    return any(
        permission_obj.name == required
        for role in user.roles
        for permission_obj in role.permissions
    )


def require_permission(permission: Permission | str) -> Callable:
    """Create a FastAPI dependency enforcing one application permission."""

    async def dependency(
        current_user: User = Depends(get_current_user),
    ) -> User:
        if not has_permission(current_user, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions.",
            )
        return current_user

    return dependency
