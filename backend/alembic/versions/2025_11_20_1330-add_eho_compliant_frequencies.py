"""add_eho_compliant_frequencies

Revision ID: b2c3d4e5f6g7
Revises: a1b2c3d4e5f6
Create Date: 2025-11-20 13:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2c3d4e5f6g7'
down_revision = 'a1b2c3d4e5f6'
branch_labels = None
depends_on = None


def upgrade():
    """Add new frequency types for EHO compliance."""
    # Add new enum values to checklistfrequency enum
    # Note: ALTER TYPE ADD VALUE cannot be rolled back, so we use IF NOT EXISTS
    op.execute("ALTER TYPE checklistfrequency ADD VALUE IF NOT EXISTS 'quarterly'")
    op.execute("ALTER TYPE checklistfrequency ADD VALUE IF NOT EXISTS 'every_2_hours'")
    op.execute("ALTER TYPE checklistfrequency ADD VALUE IF NOT EXISTS 'per_batch'")
    op.execute("ALTER TYPE checklistfrequency ADD VALUE IF NOT EXISTS 'per_delivery'")
    op.execute("ALTER TYPE checklistfrequency ADD VALUE IF NOT EXISTS 'continuous'")
    op.execute("ALTER TYPE checklistfrequency ADD VALUE IF NOT EXISTS 'as_needed'")


def downgrade():
    """
    Note: PostgreSQL does not support removing enum values directly.
    You would need to:
    1. Create a new enum type without the unwanted values
    2. Alter the column to use the new type
    3. Drop the old type
    
    For simplicity, we'll leave this as a no-op since removing enum values
    is destructive and complex. The old values won't cause issues if unused.
    """
    pass
