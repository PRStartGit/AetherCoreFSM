"""seed recipe book data

Revision ID: 2025_11_26_1301
Revises: 2025_11_26_1300
Create Date: 2025-11-26 13:01:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = '2025_11_26_1301'
down_revision = '2025_11_26_1300'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    # 1. Seed Recipe Categories
    categories = [
        ('Starters', 1),
        ('Mains', 2),
        ('Desserts', 3),
        ('Sauces', 4),
        ('Prep Items', 5),
        ('Sides', 6),
        ('Soups', 7),
        ('Salads', 8),
        ('Beverages', 9),
        ('Other', 10)
    ]

    for name, sort_order in categories:
        conn.execute(text(
            "INSERT INTO recipe_categories (name, sort_order) VALUES (:name, :sort_order)"
        ), {"name": name, "sort_order": sort_order})

    # 2. Seed Ingredient Units
    units = [
        # Weight
        ('g', 'grams', 'weight', 1),
        ('kg', 'kilograms', 'weight', 2),
        ('oz', 'ounces', 'weight', 3),
        ('lb', 'pounds', 'weight', 4),

        # Volume
        ('ml', 'millilitres', 'volume', 10),
        ('L', 'litres', 'volume', 11),
        ('tsp', 'teaspoon', 'volume', 12),
        ('tbsp', 'tablespoon', 'volume', 13),
        ('fl oz', 'fluid ounces', 'volume', 14),
        ('cup', 'cups', 'volume', 15),
        ('pint', 'pints', 'volume', 16),

        # Count
        ('pc', 'piece', 'count', 20),
        ('pcs', 'pieces', 'count', 21),
        ('whole', 'whole', 'count', 22),
        ('bunch', 'bunch', 'count', 23),
        ('clove', 'clove', 'count', 24),
        ('cloves', 'cloves', 'count', 25),
        ('slice', 'slice', 'count', 26),
        ('slices', 'slices', 'count', 27),
        ('leaf', 'leaf', 'count', 28),
        ('leaves', 'leaves', 'count', 29),
        ('sprig', 'sprig', 'count', 30),
        ('sprigs', 'sprigs', 'count', 31),

        # Other
        ('pinch', 'pinch', 'other', 40),
        ('to taste', 'to taste', 'other', 41),
        ('handful', 'handful', 'other', 42),
        ('dash', 'dash', 'other', 43)
    ]

    for name, display_name, category, sort_order in units:
        conn.execute(text(
            "INSERT INTO ingredient_units (name, display_name, category, sort_order) VALUES (:name, :display, :cat, :sort)"
        ), {"name": name, "display": display_name, "cat": category, "sort": sort_order})

    # 3. Seed Allergen Keywords
    allergen_mappings = [
        # Celery
        ('celery', 'Celery'),
        ('celeriac', 'Celery'),

        # Gluten
        ('wheat', 'Gluten'),
        ('flour', 'Gluten'),
        ('bread', 'Gluten'),
        ('pasta', 'Gluten'),
        ('noodles', 'Gluten'),
        ('couscous', 'Gluten'),
        ('semolina', 'Gluten'),
        ('rye', 'Gluten'),
        ('barley', 'Gluten'),
        ('oats', 'Gluten'),
        ('bran', 'Gluten'),
        ('bulgur', 'Gluten'),
        ('spelt', 'Gluten'),
        ('farro', 'Gluten'),
        ('seitan', 'Gluten'),
        ('breadcrumbs', 'Gluten'),
        ('batter', 'Gluten'),

        # Crustaceans
        ('prawn', 'Crustaceans'),
        ('prawns', 'Crustaceans'),
        ('shrimp', 'Crustaceans'),
        ('crab', 'Crustaceans'),
        ('lobster', 'Crustaceans'),
        ('crayfish', 'Crustaceans'),
        ('langoustine', 'Crustaceans'),

        # Eggs
        ('egg', 'Eggs'),
        ('eggs', 'Eggs'),
        ('mayonnaise', 'Eggs'),
        ('mayo', 'Eggs'),
        ('meringue', 'Eggs'),
        ('aioli', 'Eggs'),

        # Fish
        ('fish', 'Fish'),
        ('salmon', 'Fish'),
        ('tuna', 'Fish'),
        ('cod', 'Fish'),
        ('haddock', 'Fish'),
        ('anchovy', 'Fish'),
        ('anchovies', 'Fish'),
        ('sardine', 'Fish'),
        ('sardines', 'Fish'),
        ('mackerel', 'Fish'),
        ('trout', 'Fish'),
        ('halibut', 'Fish'),
        ('sea bass', 'Fish'),
        ('hake', 'Fish'),
        ('worcestershire', 'Fish'),

        # Lupin
        ('lupin', 'Lupin'),

        # Milk/Dairy
        ('milk', 'Dairy'),
        ('cream', 'Dairy'),
        ('butter', 'Dairy'),
        ('cheese', 'Dairy'),
        ('cheddar', 'Dairy'),
        ('parmesan', 'Dairy'),
        ('mozzarella', 'Dairy'),
        ('feta', 'Dairy'),
        ('brie', 'Dairy'),
        ('gouda', 'Dairy'),
        ('yogurt', 'Dairy'),
        ('yoghurt', 'Dairy'),
        ('crème', 'Dairy'),
        ('creme', 'Dairy'),
        ('bechamel', 'Dairy'),
        ('custard', 'Dairy'),
        ('whey', 'Dairy'),
        ('casein', 'Dairy'),
        ('lactose', 'Dairy'),
        ('ghee', 'Dairy'),

        # Molluscs
        ('mussel', 'Molluscs'),
        ('mussels', 'Molluscs'),
        ('oyster', 'Molluscs'),
        ('oysters', 'Molluscs'),
        ('clam', 'Molluscs'),
        ('clams', 'Molluscs'),
        ('squid', 'Molluscs'),
        ('octopus', 'Molluscs'),
        ('scallop', 'Molluscs'),
        ('scallops', 'Molluscs'),
        ('whelk', 'Molluscs'),
        ('snail', 'Molluscs'),
        ('snails', 'Molluscs'),

        # Mustard
        ('mustard', 'Mustard'),
        ('dijon', 'Mustard'),

        # Nuts (Tree Nuts)
        ('almond', 'Nuts'),
        ('almonds', 'Nuts'),
        ('hazelnut', 'Nuts'),
        ('hazelnuts', 'Nuts'),
        ('walnut', 'Nuts'),
        ('walnuts', 'Nuts'),
        ('cashew', 'Nuts'),
        ('cashews', 'Nuts'),
        ('pecan', 'Nuts'),
        ('pecans', 'Nuts'),
        ('brazil', 'Nuts'),
        ('brazils', 'Nuts'),
        ('pistachio', 'Nuts'),
        ('pistachios', 'Nuts'),
        ('macadamia', 'Nuts'),
        ('macadamias', 'Nuts'),
        ('chestnut', 'Nuts'),
        ('chestnuts', 'Nuts'),
        ('pine nut', 'Nuts'),
        ('pine nuts', 'Nuts'),

        # Peanuts
        ('peanut', 'Peanuts'),
        ('peanuts', 'Peanuts'),
        ('groundnut', 'Peanuts'),
        ('groundnuts', 'Peanuts'),

        # Sesame
        ('sesame', 'Sesame'),
        ('tahini', 'Sesame'),
        ('hummus', 'Sesame'),

        # Soybeans/Soya
        ('soy', 'Soya'),
        ('soya', 'Soya'),
        ('soybean', 'Soya'),
        ('soybeans', 'Soya'),
        ('tofu', 'Soya'),
        ('edamame', 'Soya'),
        ('miso', 'Soya'),
        ('tempeh', 'Soya'),
        ('soy sauce', 'Soya'),

        # Sulphites
        ('sulphite', 'Sulphites'),
        ('sulphites', 'Sulphites'),
        ('sulfite', 'Sulphites'),
        ('sulfites', 'Sulphites'),
        ('wine', 'Sulphites'),
        ('dried fruit', 'Sulphites'),
        ('vinegar', 'Sulphites')
    ]

    for keyword, allergen in allergen_mappings:
        conn.execute(text(
            "INSERT INTO allergen_keywords (keyword, allergen) VALUES (:keyword, :allergen)"
        ), {"keyword": keyword.lower(), "allergen": allergen})

    # 4. Seed Job Roles (if they don't exist)
    job_roles = [
        ('Head Chef', True),
        ('Sous Chef', True),
        ('Chef', True),
        ('General Manager', True),
        ('Assistant Manager', True)
    ]

    for role_name, is_system in job_roles:
        # Check if role exists
        result = conn.execute(text(
            "SELECT id FROM job_roles WHERE name = :name"
        ), {"name": role_name})

        if not result.fetchone():
            conn.execute(text(
                "INSERT INTO job_roles (name, is_system_role) VALUES (:name, :is_system)"
            ), {"name": role_name, "is_system": is_system})


def downgrade():
    conn = op.get_bind()

    # Remove seed data in reverse order
    conn.execute(text("DELETE FROM allergen_keywords"))
    conn.execute(text("DELETE FROM ingredient_units"))
    conn.execute(text("DELETE FROM recipe_categories"))

    # Only remove job roles that we added (system roles for recipes)
    conn.execute(text(
        "DELETE FROM job_roles WHERE name IN ('Head Chef', 'Sous Chef', 'Chef', 'General Manager', 'Assistant Manager') AND is_system_role = true"
    ))
