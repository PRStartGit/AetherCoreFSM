"""create user_module_access table

Revision ID: 2025_11_26_1202
Revises: 2025_11_26_1201
Create Date: 2025-11-26 12:02:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2025_11_26_1202'
down_revision = '2025_11_26_1201'
branch_labels = None
depends_on = None


def upgrade():
    # Create user_module_access table
    op.create_table(
        'user_module_access',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('module_name', sa.String(length=50), nullable=False),
        sa.Column('granted_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('granted_by_user_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['granted_by_user_id'], ['users.id'], ondelete='SET NULL'),
        sa.UniqueConstraint('user_id', 'module_name', name='uq_user_module')
    )

    # Create indexes for better query performance
    op.create_index('ix_user_module_access_user_id', 'user_module_access', ['user_id'])
    op.create_index('ix_user_module_access_module_name', 'user_module_access', ['module_name'])
    op.create_index('ix_user_module_access_id', 'user_module_access', ['id'])


def downgrade():
    op.drop_index('ix_user_module_access_id', table_name='user_module_access')
    op.drop_index('ix_user_module_access_module_name', table_name='user_module_access')
    op.drop_index('ix_user_module_access_user_id', table_name='user_module_access')
    op.drop_table('user_module_access')
