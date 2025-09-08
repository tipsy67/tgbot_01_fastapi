"""add optional column

Revision ID: 7be94518ded1
Revises: 1ce598c2c45e
Create Date: 2025-09-08 22:16:15.661607

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7be94518ded1'
down_revision: Union[str, Sequence[str], None] = '1ce598c2c45e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('tickets', 'action',
               existing_type=sa.CHAR(length=4),
               nullable=True)
    op.alter_column('tickets', 'initiator_id',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('users', 'last_activity',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('users', 'last_activity',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('tickets', 'initiator_id',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('tickets', 'action',
               existing_type=sa.CHAR(length=4),
               nullable=False)
