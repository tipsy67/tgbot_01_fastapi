"""add nullable instead of optional

Revision ID: b5dfee5f9b8e
Revises: 5cf7681fffe0
Create Date: 2025-09-08 21:11:57.408122

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b5dfee5f9b8e'
down_revision: Union[str, Sequence[str], None] = '5cf7681fffe0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('tickets', 'fired_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('tickets', 'fired_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
