"""create module progress table

Revision ID: 2025_11_26_1210
Revises: 2025_11_26_1209
Create Date: 2025-11-26 12:10:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2025_11_26_1210'
down_revision = '2025_11_26_1209'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'module_progress',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('enrollment_id', sa.Integer(), nullable=False),
        sa.Column('module_id', sa.Integer(), nullable=False),
        sa.Column('is_completed', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('time_spent_seconds', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('last_position_seconds', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True, onupdate=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['enrollment_id'], ['course_enrollments.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['module_id'], ['course_modules.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('enrollment_id', 'module_id', name='uq_enrollment_module')
    )
    op.create_index('ix_module_progress_id', 'module_progress', ['id'])
    op.create_index('ix_module_progress_enrollment_id', 'module_progress', ['enrollment_id'])
    op.create_index('ix_module_progress_module_id', 'module_progress', ['module_id'])


def downgrade():
    op.drop_index('ix_module_progress_module_id', table_name='module_progress')
    op.drop_index('ix_module_progress_enrollment_id', table_name='module_progress')
    op.drop_index('ix_module_progress_id', table_name='module_progress')
    op.drop_table('module_progress')
