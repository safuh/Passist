"""seed application permissions and default role mappings

Revision ID: 20260819_permissions
Revises: 20260815_ai_providers

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260819_permissions"
down_revision: Union[str, Sequence[str], None] = "20260815_ai_providers"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

PERMISSIONS = [
    ("auth:me", "Read the current authenticated user"),
    ("api_keys:read", "List API keys owned by the user"),
    ("api_keys:create", "Create API keys"),
    ("api_keys:revoke", "Revoke API keys"),
    ("ai:providers:read", "Read AI provider configuration"),
    ("ai:providers:manage", "Manage AI provider configuration"),
    ("conversations:read", "Read conversations"),
    ("conversations:write", "Create and modify conversations"),
    ("tools:execute", "Execute enabled tools"),
    ("documents:read", "Read knowledge documents"),
    ("documents:write", "Create and modify knowledge documents"),
]


def upgrade() -> None:
    connection = op.get_bind()

    for name, description in PERMISSIONS:
        connection.execute(
            sa.text(
                "INSERT INTO permissions (name, description) "
                "SELECT :name, :description "
                "WHERE NOT EXISTS (SELECT 1 FROM permissions WHERE name = :name)"
            ),
            {"name": name, "description": description},
        )

    connection.execute(
        sa.text(
            "INSERT INTO roles (name, description) "
            "SELECT 'admin', 'Platform administrator role' "
            "WHERE NOT EXISTS (SELECT 1 FROM roles WHERE name = 'admin')"
        )
    )

    user_permissions = [name for name, _ in PERMISSIONS]
    for name in user_permissions:
        connection.execute(
            sa.text(
                "INSERT INTO role_permissions (role_id, permission_id) "
                "SELECT r.id, p.id FROM roles r CROSS JOIN permissions p "
                "WHERE r.name = 'user' AND p.name = :permission "
                "AND NOT EXISTS (SELECT 1 FROM role_permissions rp "
                "WHERE rp.role_id = r.id AND rp.permission_id = p.id)"
            ),
            {"permission": name},
        )
        connection.execute(
            sa.text(
                "INSERT INTO role_permissions (role_id, permission_id) "
                "SELECT r.id, p.id FROM roles r CROSS JOIN permissions p "
                "WHERE r.name = 'admin' AND p.name = :permission "
                "AND NOT EXISTS (SELECT 1 FROM role_permissions rp "
                "WHERE rp.role_id = r.id AND rp.permission_id = p.id)"
            ),
            {"permission": name},
        )


def downgrade() -> None:
    connection = op.get_bind()
    connection.execute(
        sa.text(
            "DELETE FROM role_permissions WHERE permission_id IN "
            "(SELECT id FROM permissions WHERE name LIKE '%:%')"
        )
    )
    connection.execute(sa.text("DELETE FROM roles WHERE name = 'admin'"))
    connection.execute(
        sa.text(
            "DELETE FROM permissions WHERE name IN (" +
            ",".join(f"'{name}'" for name, _ in PERMISSIONS) + ")"
        )
    )
