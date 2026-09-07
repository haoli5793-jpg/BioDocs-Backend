"""add database defaults

Revision ID: 3ab3c05276e5
Revises: ef67aed8480b
Create Date: 2026-09-07 21:41:56.747185

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '3ab3c05276e5'
down_revision: str | Sequence[str] | None = 'ef67aed8480b'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """执行本次迁移。"""
    op.alter_column(
        "documents",
        "status",
        existing_type=sa.String(length=50),
        server_default=sa.text("'pending'"),
        existing_nullable=False,
    )
    op.alter_column(
        "users",
        "is_admin",
        existing_type=sa.Boolean(),
        server_default=sa.text("0"),
        existing_nullable=False,
    )


def downgrade() -> None:
    """撤销本次迁移。"""
    op.alter_column(
        "users",
        "is_admin",
        existing_type=sa.Boolean(),
        server_default=None,
        existing_nullable=False,
    )
    op.alter_column(
        "documents",
        "status",
        existing_type=sa.String(length=50),
        server_default=None,
        existing_nullable=False,
    )
