"""add job_role_id and hire_date to users

Revision ID: 2025_11_26_1203
Revises: 2025_11_26_1202
Create Date: 2025-11-26 12:03:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = '2025_11_26_1203'
down_revision = '2025_11_26_1202'
branch_labels = None
depends_on = None


def upgrade():
    # Add columns to users table
    op.add_column('users', sa.Column('job_role_id', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('hire_date', sa.Date(), nullable=True))
    
    # Foreign key only supported in batch mode for SQLite
    bind = op.get_bind()
    if bind.dialect.name != 'sqlite':
        op.create_foreign_key('fk_users_job_role_id', 'users', 'job_roles', ['job_role_id'], ['id'])


def downgrade():
    bind = op.get_bind()
    if bind.dialect.name != 'sqlite':
        op.drop_constraint('fk_users_job_role_id', 'users', type_='foreignkey')
    op.drop_column('users', 'hire_date')
    op.drop_column('users', 'job_role_id')
