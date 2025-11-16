"""add_dynamic_task_fields_and_responses

Revision ID: ebe66fde3a15
Revises: 9b8ebaebc5a0
Create Date: 2025-11-15 11:46:16.034364

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ebe66fde3a15'
down_revision = '9b8ebaebc5a0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add has_dynamic_form column to tasks table
    op.add_column('tasks', sa.Column('has_dynamic_form', sa.Boolean(), server_default='0', nullable=True))

    # Create task_fields table
    op.create_table(
        'task_fields',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('field_type', sa.String(length=50), nullable=False),
        sa.Column('field_label', sa.String(length=255), nullable=False),
        sa.Column('field_order', sa.Integer(), nullable=False),
        sa.Column('is_required', sa.Boolean(), server_default='1', nullable=True),

        # Configuration (JSON for SQLite instead of JSONB)
        sa.Column('validation_rules', sa.JSON(), nullable=True),
        sa.Column('options', sa.JSON(), nullable=True),

        # Conditional logic
        sa.Column('show_if', sa.JSON(), nullable=True),

        # Timestamps
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),

        sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_fields_id'), 'task_fields', ['id'], unique=False)
    op.create_index(op.f('ix_task_fields_task_id'), 'task_fields', ['task_id'], unique=False)

    # Create task_field_responses table
    op.create_table(
        'task_field_responses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('checklist_item_id', sa.Integer(), nullable=False),  # Changed from task_completion_id to match our schema
        sa.Column('task_field_id', sa.Integer(), nullable=False),

        # Response values (polymorphic - one will be populated)
        sa.Column('text_value', sa.Text(), nullable=True),
        sa.Column('number_value', sa.Float(), nullable=True),  # Using Float instead of DECIMAL for SQLite
        sa.Column('boolean_value', sa.Boolean(), nullable=True),
        sa.Column('json_value', sa.JSON(), nullable=True),
        sa.Column('file_url', sa.Text(), nullable=True),

        # Auto-generated defect (if validation triggers)
        sa.Column('auto_defect_id', sa.Integer(), nullable=True),

        # Timestamps
        sa.Column('completed_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('completed_by', sa.Integer(), nullable=True),

        sa.ForeignKeyConstraint(['checklist_item_id'], ['checklist_items.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['task_field_id'], ['task_fields.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['auto_defect_id'], ['defects.id'], ),
        sa.ForeignKeyConstraint(['completed_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_field_responses_id'), 'task_field_responses', ['id'], unique=False)
    op.create_index(op.f('ix_task_field_responses_checklist_item_id'), 'task_field_responses', ['checklist_item_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_task_field_responses_checklist_item_id'), table_name='task_field_responses')
    op.drop_index(op.f('ix_task_field_responses_id'), table_name='task_field_responses')
    op.drop_table('task_field_responses')

    op.drop_index(op.f('ix_task_fields_task_id'), table_name='task_fields')
    op.drop_index(op.f('ix_task_fields_id'), table_name='task_fields')
    op.drop_table('task_fields')

    op.drop_column('tasks', 'has_dynamic_form')
