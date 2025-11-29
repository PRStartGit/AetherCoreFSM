"""Add reporting module to modules table

Revision ID: 2025_11_29_1400
Revises: 2025_11_27_1700
Create Date: 2025-11-29 14:00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column

revision = '2025_11_29_1400'
down_revision = '2025_11_27_1700'
branch_labels = None
depends_on = None


def upgrade():
    # Define modules table for insert
    modules_table = table(
        'modules',
        column('name', sa.String),
        column('code', sa.String),
        column('description', sa.Text),
        column('icon', sa.String),
        column('is_core', sa.Boolean),
        column('addon_price_per_site', sa.Float),
        column('addon_price_per_org', sa.Float),
        column('is_active', sa.Boolean),
        column('display_order', sa.Integer)
    )

    # Insert reporting module
    op.bulk_insert(
        modules_table,
        [
            {
                'name': 'Reporting',
                'code': 'reporting',
                'description': 'Generate PDF reports from checklists. Export daily compliance reports with all answers, evidence photos, and status indicators.',
                'icon': 'fa-file-pdf',
                'is_core': False,
                'addon_price_per_site': 1.50,
                'addon_price_per_org': None,
                'is_active': True,
                'display_order': 50
            }
        ]
    )


def downgrade():
    # Remove the reporting module
    op.execute("DELETE FROM modules WHERE code = 'reporting'")
