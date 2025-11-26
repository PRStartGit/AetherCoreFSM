"""create job_roles table

Revision ID: 2025_11_26_1200
Revises: 2025_11_25_2300
Create Date: 2025-11-26 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2025_11_26_1200'
down_revision = '2025_11_25_2300'
branch_labels = None
depends_on = None


def upgrade():
    # Create job_roles table
    op.create_table(
        'job_roles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('is_system_role', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # Create index on name for faster lookups
    op.create_index('ix_job_roles_name', 'job_roles', ['name'])
    op.create_index('ix_job_roles_id', 'job_roles', ['id'])


def downgrade():
    op.drop_index('ix_job_roles_id', table_name='job_roles')
    op.drop_index('ix_job_roles_name', table_name='job_roles')
    op.drop_table('job_roles')
