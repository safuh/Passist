"""add AI provider configuration

Revision ID: 20260815_ai_providers
Revises: bcaba22a5b93
Create Date: 2026-08-15

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260815_ai_providers"
down_revision: Union[str, Sequence[str], None] = "bcaba22a5b93"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "ai_providers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("provider_type", sa.String(length=50), nullable=False),
        sa.Column("base_url", sa.String(length=500), nullable=True),
        sa.Column("api_key_encrypted", sa.String(length=2048), nullable=True),
        sa.Column("default_model", sa.String(length=200), nullable=True),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ai_providers_owner_id", "ai_providers", ["owner_id"])
    op.create_index("ix_ai_providers_provider_type", "ai_providers", ["provider_type"])
    op.create_index(
        "ix_ai_providers_owner_name",
        "ai_providers",
        ["owner_id", "name"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("ix_ai_providers_owner_name", table_name="ai_providers")
    op.drop_index("ix_ai_providers_provider_type", table_name="ai_providers")
    op.drop_index("ix_ai_providers_owner_id", table_name="ai_providers")
    op.drop_table("ai_providers")
