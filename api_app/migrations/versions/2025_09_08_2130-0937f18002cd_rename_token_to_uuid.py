"""rename token to uuid

Revision ID: 0937f18002cd
Revises: b5dfee5f9b8e
Create Date: 2025-09-08 21:30:24.981758

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0937f18002cd'
down_revision: Union[str, Sequence[str], None] = 'b5dfee5f9b8e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('user_uuid', sa.Uuid(), nullable=False))
    op.drop_column('users', 'token')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('users', sa.Column('token', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.drop_column('users', 'user_uuid')
