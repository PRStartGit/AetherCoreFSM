"""create course enrollments table

Revision ID: 2025_11_26_1209
Revises: 2025_11_26_1208
Create Date: 2025-11-26 12:09:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2025_11_26_1209'
down_revision = '2025_11_26_1208'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'course_enrollments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('assigned_by_user_id', sa.Integer(), nullable=True),
        sa.Column('enrolled_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='not_started'),
        sa.Column('progress_percentage', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_accessed_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['assigned_by_user_id'], ['users.id'], ondelete='SET NULL'),
        sa.UniqueConstraint('user_id', 'course_id', name='uq_user_course')
    )
    op.create_index('ix_course_enrollments_id', 'course_enrollments', ['id'])
    op.create_index('ix_course_enrollments_user_id', 'course_enrollments', ['user_id'])
    op.create_index('ix_course_enrollments_course_id', 'course_enrollments', ['course_id'])
    op.create_index('ix_course_enrollments_status', 'course_enrollments', ['status'])


def downgrade():
    op.drop_index('ix_course_enrollments_status', table_name='course_enrollments')
    op.drop_index('ix_course_enrollments_course_id', table_name='course_enrollments')
    op.drop_index('ix_course_enrollments_user_id', table_name='course_enrollments')
    op.drop_index('ix_course_enrollments_id', table_name='course_enrollments')
    op.drop_table('course_enrollments')
