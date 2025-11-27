"""add_eho_compliant_frequencies

Revision ID: 2025_11_20_1330
Revises: 2025_11_19_1845
Create Date: 2025-11-20 13:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2025_11_20_1330'
down_revision = '2025_11_19_1845'
branch_labels = None
depends_on = None


def upgrade():
    """Add new frequency types for EHO compliance."""
    # Only execute on PostgreSQL - SQLite uses strings for enums
    bind = op.get_bind()
    if bind.dialect.name == 'postgresql':
        # Add new enum values to checklistfrequency enum
        op.execute("ALTER TYPE checklistfrequency ADD VALUE IF NOT EXISTS 'quarterly'")
        op.execute("ALTER TYPE checklistfrequency ADD VALUE IF NOT EXISTS 'every_2_hours'")
        op.execute("ALTER TYPE checklistfrequency ADD VALUE IF NOT EXISTS 'per_batch'")
        op.execute("ALTER TYPE checklistfrequency ADD VALUE IF NOT EXISTS 'per_delivery'")
        op.execute("ALTER TYPE checklistfrequency ADD VALUE IF NOT EXISTS 'continuous'")
        op.execute("ALTER TYPE checklistfrequency ADD VALUE IF NOT EXISTS 'as_needed'")


def downgrade():
    """
    Note: PostgreSQL does not support removing enum values directly.
    For simplicity, we leave this as a no-op.
    """
    pass
