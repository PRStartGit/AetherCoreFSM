"""add_promotions_table

Revision ID: a1b2c3d4e5f6
Revises: 
Create Date: 2025-11-19 18:45:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = '2025_11_19_1845'
down_revision = 'a1b2c3d4e5f6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'promotions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('trial_days', sa.Integer(), nullable=False, server_default='30'),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('start_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('end_date', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_promotions_id'), 'promotions', ['id'], unique=False)
    
    # Create default promotion (30-day trial)
    op.execute(text("""
        INSERT INTO promotions (name, description, trial_days, is_active, created_at)
        VALUES ('Standard Trial', 'Default 30-day trial period', 30, true, CURRENT_TIMESTAMP)
    """))


def downgrade() -> None:
    op.drop_index(op.f('ix_promotions_id'), table_name='promotions')
    op.drop_table('promotions')
