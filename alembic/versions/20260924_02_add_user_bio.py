"""Добавление поля bio в таблицу users.

Revision ID: 20260924_02
Revises: 20260924_01
Create Date: 2026-09-24 12:15:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260924_02"
down_revision: Union[str, Sequence[str], None] = "20260924_01"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Временный server_default позволяет заполнить уже существующие строки.
    op.add_column(
        "users",
        sa.Column("bio", sa.String(length=500), server_default="", nullable=False),
    )
    op.alter_column("users", "bio", server_default=None)


def downgrade() -> None:
    op.drop_column("users", "bio")
