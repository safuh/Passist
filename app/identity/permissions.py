"""Permission names and authorization primitives."""

from enum import StrEnum


class Permission(StrEnum):
    """Stable application permission identifiers."""

    AUTH_ME = "auth:me"
    API_KEYS_READ = "api_keys:read"
    API_KEYS_CREATE = "api_keys:create"
    API_KEYS_REVOKE = "api_keys:revoke"
    AI_PROVIDERS_READ = "ai:providers:read"
    AI_PROVIDERS_MANAGE = "ai:providers:manage"
    CONVERSATIONS_READ = "conversations:read"
    CONVERSATIONS_WRITE = "conversations:write"
    TOOLS_EXECUTE = "tools:execute"
    DOCUMENTS_READ = "documents:read"
    DOCUMENTS_WRITE = "documents:write"


DEFAULT_ROLE_PERMISSIONS: dict[str, tuple[Permission, ...]] = {
    "user": (
        Permission.AUTH_ME,
        Permission.API_KEYS_READ,
        Permission.API_KEYS_CREATE,
        Permission.API_KEYS_REVOKE,
        Permission.AI_PROVIDERS_READ,
        Permission.AI_PROVIDERS_MANAGE,
        Permission.CONVERSATIONS_READ,
        Permission.CONVERSATIONS_WRITE,
        Permission.TOOLS_EXECUTE,
        Permission.DOCUMENTS_READ,
        Permission.DOCUMENTS_WRITE,
    ),
    "admin": tuple(Permission),
}
