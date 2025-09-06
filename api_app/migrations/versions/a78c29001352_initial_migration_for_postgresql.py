"""Initial migration for PostgreSQL

Revision ID: a78c29001352
Revises: 
Create Date: 2025-09-06 23:45:08.848034

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a78c29001352'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('prizes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('phone_number', sa.String(length=12), nullable=True),
    sa.Column('language_code', sa.String(length=2), nullable=True),
    sa.Column('token', sa.String(length=50), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('last_activity', sa.DateTime(), nullable=False),
    sa.Column('is_staff', sa.Boolean(), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tickets',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('action', sa.CHAR(length=4), nullable=False),
    sa.Column('action_description', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('initiator_id', sa.Integer(), nullable=False),
    sa.Column('is_fired', sa.Boolean(), nullable=False),
    sa.Column('fired_at', sa.DateTime(), nullable=False),
    sa.Column('prize_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['initiator_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['prize_id'], ['prizes.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('tickets')
    op.drop_table('users')
    op.drop_table('prizes')
