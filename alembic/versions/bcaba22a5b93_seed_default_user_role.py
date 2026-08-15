"""seed default user role

Revision ID: bcaba22a5b93
Revises: 4c50ff22b13c
Create Date: 2026-08-12 09:44:47.103338

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bcaba22a5b93'
down_revision: Union[str, Sequence[str], None] = '4c50ff22b13c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        sa.text(
            """
            INSERT INTO roles (name, description)
            VALUES ('user', 'Default application user role')
            """
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        sa.text(
            """
            DELETE FROM roles
            WHERE name = 'user'
            """
        )
    )
