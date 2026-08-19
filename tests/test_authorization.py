from types import SimpleNamespace

from app.identity.authorization import has_permission
from app.identity.permissions import Permission


def test_user_permission_is_resolved_through_roles():
    user = SimpleNamespace(
        roles=[
            SimpleNamespace(
                permissions=[
                    SimpleNamespace(name=Permission.API_KEYS_CREATE.value),
                ]
            )
        ]
    )

    assert has_permission(user, Permission.API_KEYS_CREATE)


def test_missing_permission_is_denied():
    user = SimpleNamespace(roles=[])

    assert not has_permission(user, Permission.API_KEYS_CREATE)
