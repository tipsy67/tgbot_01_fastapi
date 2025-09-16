"""add fields to prize

Revision ID: a324f76e31f7
Revises: 9434707cc79c
Create Date: 2025-09-16 21:22:17.952694

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a324f76e31f7'
down_revision: Union[str, Sequence[str], None] = '9434707cc79c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('prizes', sa.Column('name', sa.String(length=50), nullable=False))
    op.add_column('prizes', sa.Column('weight', sa.Integer(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('prizes', 'weight')
    op.drop_column('prizes', 'name')
