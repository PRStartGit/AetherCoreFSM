"""create courses table

Revision ID: 2025_11_26_1206
Revises: 2025_11_26_1205
Create Date: 2025-11-26 12:06:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2025_11_26_1206'
down_revision = '2025_11_26_1205'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'courses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('thumbnail_url', sa.String(length=500), nullable=True),
        sa.Column('category_id', sa.Integer(), nullable=True),
        sa.Column('is_published', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('created_by_user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True, onupdate=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['category_id'], ['course_categories.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['created_by_user_id'], ['users.id'], ondelete='CASCADE')
    )
    op.create_index('ix_courses_id', 'courses', ['id'])
    op.create_index('ix_courses_title', 'courses', ['title'])
    op.create_index('ix_courses_category_id', 'courses', ['category_id'])
    op.create_index('ix_courses_is_published', 'courses', ['is_published'])


def downgrade():
    op.drop_index('ix_courses_is_published', table_name='courses')
    op.drop_index('ix_courses_category_id', table_name='courses')
    op.drop_index('ix_courses_title', table_name='courses')
    op.drop_index('ix_courses_id', table_name='courses')
    op.drop_table('courses')
