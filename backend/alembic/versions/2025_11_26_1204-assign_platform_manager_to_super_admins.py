"""assign Platform Manager role to existing super admins

Revision ID: 2025_11_26_1204
Revises: 2025_11_26_1203
Create Date: 2025-11-26 12:04:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2025_11_26_1204'
down_revision = '2025_11_26_1203'
branch_labels = None
depends_on = None


def upgrade():
    # Get the Platform Manager role ID
    connection = op.get_bind()

    # Find Platform Manager role ID
    platform_manager_result = connection.execute(
        sa.text("SELECT id FROM job_roles WHERE name = 'Platform Manager' AND is_system_role = TRUE")
    )
    platform_manager_row = platform_manager_result.fetchone()

    if platform_manager_row:
        platform_manager_id = platform_manager_row[0]

        # Update all super_admin users to have Platform Manager job role
        connection.execute(
            sa.text(
                "UPDATE users SET job_role_id = :role_id WHERE role = 'super_admin' AND job_role_id IS NULL"
            ),
            {'role_id': platform_manager_id}
        )


def downgrade():
    # Get the Platform Manager role ID
    connection = op.get_bind()

    platform_manager_result = connection.execute(
        sa.text("SELECT id FROM job_roles WHERE name = 'Platform Manager' AND is_system_role = TRUE")
    )
    platform_manager_row = platform_manager_result.fetchone()

    if platform_manager_row:
        platform_manager_id = platform_manager_row[0]

        # Remove Platform Manager job role from super admins
        connection.execute(
            sa.text(
                "UPDATE users SET job_role_id = NULL WHERE role = 'super_admin' AND job_role_id = :role_id"
            ),
            {'role_id': platform_manager_id}
        )
