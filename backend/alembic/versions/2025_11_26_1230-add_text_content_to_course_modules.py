"""add text_content to course_modules

Revision ID: 2025_11_26_1230
Revises: 2025_11_26_1210
Create Date: 2025-11-26 12:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2025_11_26_1230'
down_revision = '2025_11_26_1210'
branch_labels = None
depends_on = None


def upgrade():
    # Add text_content column to course_modules table
    op.add_column('course_modules', sa.Column('text_content', sa.Text(), nullable=True))


def downgrade():
    # Remove text_content column from course_modules table
    op.drop_column('course_modules', 'text_content')
