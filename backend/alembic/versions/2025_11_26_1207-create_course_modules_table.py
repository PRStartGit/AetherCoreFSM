"""create course modules table

Revision ID: 2025_11_26_1207
Revises: 2025_11_26_1206
Create Date: 2025-11-26 12:07:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2025_11_26_1207'
down_revision = '2025_11_26_1206'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'course_modules',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('video_url', sa.String(length=500), nullable=True),
        sa.Column('pdf_url', sa.String(length=500), nullable=True),
        sa.Column('order_index', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('duration_minutes', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True, onupdate=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ondelete='CASCADE')
    )
    op.create_index('ix_course_modules_id', 'course_modules', ['id'])
    op.create_index('ix_course_modules_course_id', 'course_modules', ['course_id'])
    op.create_index('ix_course_modules_order_index', 'course_modules', ['course_id', 'order_index'])


def downgrade():
    op.drop_index('ix_course_modules_order_index', table_name='course_modules')
    op.drop_index('ix_course_modules_course_id', table_name='course_modules')
    op.drop_index('ix_course_modules_id', table_name='course_modules')
    op.drop_table('course_modules')
