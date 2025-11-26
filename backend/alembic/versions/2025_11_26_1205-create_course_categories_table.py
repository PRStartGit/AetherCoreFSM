"""create course categories table

Revision ID: 2025_11_26_1205
Revises: 2025_11_26_1204
Create Date: 2025-11-26 12:05:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2025_11_26_1205'
down_revision = '2025_11_26_1204'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'course_categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True, onupdate=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index('ix_course_categories_id', 'course_categories', ['id'])
    op.create_index('ix_course_categories_name', 'course_categories', ['name'])


def downgrade():
    op.drop_index('ix_course_categories_name', table_name='course_categories')
    op.drop_index('ix_course_categories_id', table_name='course_categories')
    op.drop_table('course_categories')
