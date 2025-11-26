"""seed job_roles data

Revision ID: 2025_11_26_1201
Revises: 2025_11_26_1200
Create Date: 2025-11-26 12:01:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '2025_11_26_1201'
down_revision = '2025_11_26_1200'
branch_labels = None
depends_on = None


def upgrade():
    # Insert predefined job roles
    job_roles_table = sa.table(
        'job_roles',
        sa.column('name', sa.String),
        sa.column('is_system_role', sa.Boolean),
        sa.column('created_at', sa.DateTime)
    )

    # 9 hospitality roles + 1 system role (Platform Manager)
    roles = [
        {'name': 'General Manager', 'is_system_role': False},
        {'name': 'Assistant Manager', 'is_system_role': False},
        {'name': 'Duty Manager', 'is_system_role': False},
        {'name': 'Supervisor', 'is_system_role': False},
        {'name': 'FoH Staff Member', 'is_system_role': False},
        {'name': 'Head Chef', 'is_system_role': False},
        {'name': 'Sous Chef', 'is_system_role': False},
        {'name': 'Chef', 'is_system_role': False},
        {'name': 'Kitchen Porter', 'is_system_role': False},
        {'name': 'Platform Manager', 'is_system_role': True},  # System role for super admins
    ]

    op.bulk_insert(
        job_roles_table,
        [
            {
                'name': role['name'],
                'is_system_role': role['is_system_role'],
                'created_at': datetime.utcnow()
            }
            for role in roles
        ]
    )


def downgrade():
    # Delete all seeded job roles
    op.execute("DELETE FROM job_roles WHERE name IN ('General Manager', 'Assistant Manager', 'Duty Manager', 'Supervisor', 'FoH Staff Member', 'Head Chef', 'Sous Chef', 'Chef', 'Kitchen Porter', 'Platform Manager')")
