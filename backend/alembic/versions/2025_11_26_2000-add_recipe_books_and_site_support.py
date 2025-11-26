"""add recipe books and site support

Revision ID: 2025_11_26_2000
Revises: 2025_11_26_1301
Create Date: 2025-11-26 20:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2025_11_26_2000'
down_revision = '2025_11_26_1301'
branch_labels = None
depends_on = None


def upgrade():
    # Add site_id to recipes table (NULL = global to organization)
    op.add_column('recipes', sa.Column('site_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_recipes_site_id', 'recipes', 'sites', ['site_id'], ['id'], ondelete='CASCADE')
    op.create_index('ix_recipes_site_id', 'recipes', ['site_id'])

    # Create recipe_books table
    op.create_table(
        'recipe_books',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('organization_id', sa.Integer(), nullable=False),
        sa.Column('site_id', sa.Integer(), nullable=True),  # NULL = global to organization
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_by_user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), onupdate=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['site_id'], ['sites.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['created_by_user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_recipe_books_id', 'recipe_books', ['id'])
    op.create_index('ix_recipe_books_organization_id', 'recipe_books', ['organization_id'])
    op.create_index('ix_recipe_books_site_id', 'recipe_books', ['site_id'])

    # Create recipe_book_recipes junction table (many-to-many)
    op.create_table(
        'recipe_book_recipes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('recipe_book_id', sa.Integer(), nullable=False),
        sa.Column('recipe_id', sa.Integer(), nullable=False),
        sa.Column('order_index', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('added_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['recipe_book_id'], ['recipe_books.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['recipe_id'], ['recipes.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('recipe_book_id', 'recipe_id', name='uq_book_recipe')
    )
    op.create_index('ix_recipe_book_recipes_id', 'recipe_book_recipes', ['id'])
    op.create_index('ix_recipe_book_recipes_book_id', 'recipe_book_recipes', ['recipe_book_id'])
    op.create_index('ix_recipe_book_recipes_recipe_id', 'recipe_book_recipes', ['recipe_id'])


def downgrade():
    op.drop_table('recipe_book_recipes')
    op.drop_table('recipe_books')
    op.drop_constraint('fk_recipes_site_id', 'recipes', type_='foreignkey')
    op.drop_index('ix_recipes_site_id', 'recipes')
    op.drop_column('recipes', 'site_id')
