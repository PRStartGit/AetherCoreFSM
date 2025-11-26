"""seed course categories

Revision ID: 2025_11_26_1208
Revises: 2025_11_26_1207
Create Date: 2025-11-26 12:08:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision = '2025_11_26_1208'
down_revision = '2025_11_26_1207'
branch_labels = None
depends_on = None


def upgrade():
    # Create a table representation for bulk insert
    course_categories_table = table(
        'course_categories',
        column('name', sa.String),
        column('description', sa.String)
    )

    # Seed initial course categories
    categories = [
        {
            'name': 'Food Safety',
            'description': 'Courses related to food safety regulations, best practices, and compliance'
        },
        {
            'name': 'Health & Hygiene',
            'description': 'Personal hygiene, workplace cleanliness, and health standards'
        },
        {
            'name': 'Kitchen Operations',
            'description': 'Kitchen management, equipment handling, and operational procedures'
        },
        {
            'name': 'Customer Service',
            'description': 'Front-of-house operations and customer interaction best practices'
        },
        {
            'name': 'Allergen Awareness',
            'description': 'Understanding and managing food allergens in hospitality'
        },
        {
            'name': 'Fire Safety',
            'description': 'Fire prevention, safety protocols, and emergency procedures'
        },
        {
            'name': 'First Aid',
            'description': 'Basic first aid and emergency response training'
        },
        {
            'name': 'Compliance',
            'description': 'Regulatory compliance and legal requirements for hospitality'
        }
    ]

    op.bulk_insert(course_categories_table, categories)


def downgrade():
    connection = op.get_bind()
    # Delete only the categories we created
    category_names = [
        'Food Safety', 'Health & Hygiene', 'Kitchen Operations',
        'Customer Service', 'Allergen Awareness', 'Fire Safety',
        'First Aid', 'Compliance'
    ]
    for name in category_names:
        connection.execute(
            sa.text("DELETE FROM course_categories WHERE name = :name"),
            {'name': name}
        )
