"""add nullable instead of optional. 

Revision ID: 1ce598c2c45e
Revises: 0937f18002cd
Create Date: 2025-09-08 22:02:09.926219

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1ce598c2c45e'
down_revision: Union[str, Sequence[str], None] = '0937f18002cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
