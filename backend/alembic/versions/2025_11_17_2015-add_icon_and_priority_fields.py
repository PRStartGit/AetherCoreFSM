"""add icon and priority fields

Revision ID: a1b2c3d4e5f6
Revises: ebe66fde3a15
Create Date: 2025-11-17 20:15:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = 'ebe66fde3a15'
branch_labels = None
depends_on = None


def upgrade():
    # Add icon column to categories table
    op.add_column('categories', sa.Column('icon', sa.String(), nullable=True))

    # Add priority column to tasks table
    op.add_column('tasks', sa.Column('priority', sa.String(), server_default='medium', nullable=True))


def downgrade():
    # Remove priority column from tasks table
    op.drop_column('tasks', 'priority')

    # Remove icon column from categories table
    op.drop_column('categories', 'icon')
