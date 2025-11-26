"""create recipe book tables

Revision ID: 2025_11_26_1300
Revises: 2025_11_26_1230
Create Date: 2025-11-26 13:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2025_11_26_1300'
down_revision = '2025_11_26_1230'
branch_labels = None
depends_on = None


def upgrade():
    # Recipe Categories
    op.create_table(
        'recipe_categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('sort_order', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index('ix_recipe_categories_id', 'recipe_categories', ['id'])

    # Ingredient Units
    op.create_table(
        'ingredient_units',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('display_name', sa.String(length=50), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=True),
        sa.Column('sort_order', sa.Integer(), nullable=True, server_default='0'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index('ix_ingredient_units_id', 'ingredient_units', ['id'])

    # Allergen Keywords
    op.create_table(
        'allergen_keywords',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('keyword', sa.String(length=100), nullable=False),
        sa.Column('allergen', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('keyword', 'allergen', name='uq_allergen_keyword')
    )
    op.create_index('ix_allergen_keywords_id', 'allergen_keywords', ['id'])
    op.create_index('ix_allergen_keywords_keyword', 'allergen_keywords', ['keyword'])

    # Recipes
    op.create_table(
        'recipes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('organization_id', sa.Integer(), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('method', sa.Text(), nullable=True),
        sa.Column('prep_time_minutes', sa.Integer(), nullable=True),
        sa.Column('cook_time_minutes', sa.Integer(), nullable=True),
        sa.Column('yield_quantity', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('yield_unit', sa.String(length=50), nullable=True),
        sa.Column('photo_url', sa.String(length=500), nullable=True),
        sa.Column('is_archived', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_by_user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), onupdate=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['category_id'], ['recipe_categories.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['created_by_user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_recipes_id', 'recipes', ['id'])
    op.create_index('ix_recipes_organization_id', 'recipes', ['organization_id'])
    op.create_index('ix_recipes_category_id', 'recipes', ['category_id'])

    # Recipe Ingredients
    op.create_table(
        'recipe_ingredients',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('recipe_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('quantity', sa.Numeric(precision=10, scale=3), nullable=True),
        sa.Column('unit', sa.String(length=50), nullable=True),
        sa.Column('order_index', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['recipe_id'], ['recipes.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_recipe_ingredients_id', 'recipe_ingredients', ['id'])
    op.create_index('ix_recipe_ingredients_recipe_id', 'recipe_ingredients', ['recipe_id'])

    # Recipe Allergens
    op.create_table(
        'recipe_allergens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('recipe_id', sa.Integer(), nullable=False),
        sa.Column('allergen', sa.String(length=100), nullable=False),
        sa.ForeignKeyConstraint(['recipe_id'], ['recipes.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('recipe_id', 'allergen', name='uq_recipe_allergen')
    )
    op.create_index('ix_recipe_allergens_id', 'recipe_allergens', ['id'])
    op.create_index('ix_recipe_allergens_recipe_id', 'recipe_allergens', ['recipe_id'])


def downgrade():
    op.drop_table('recipe_allergens')
    op.drop_table('recipe_ingredients')
    op.drop_table('recipes')
    op.drop_table('allergen_keywords')
    op.drop_table('ingredient_units')
    op.drop_table('recipe_categories')
