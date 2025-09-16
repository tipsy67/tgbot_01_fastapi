"""add fields to prize .

Revision ID: 9837ccf19f8c
Revises: a324f76e31f7
Create Date: 2025-09-16 21:38:14.750397

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9837ccf19f8c'
down_revision: Union[str, Sequence[str], None] = 'a324f76e31f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('prizes', sa.Column('quantity', sa.Integer(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('prizes', 'quantity')
