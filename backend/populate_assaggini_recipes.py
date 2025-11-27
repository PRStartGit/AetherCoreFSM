"""
Populate Assaggini Pasta Recipes
Creates 13 pasta recipes from the Assaggini training manual
"""
import sys
from decimal import Decimal

from app.core.database import SessionLocal, engine, Base
from app.models.organization import Organization
from app.models.site import Site
from app.models.user import User
from app.models.recipe_category import RecipeCategory
from app.models.recipe import Recipe
from app.models.recipe_ingredient import RecipeIngredient
from app.models.ingredient_unit import IngredientUnit
from app.models.recipe_book import RecipeBook, RecipeBookRecipe


def populate_assaggini_recipes():
    """Populate Assaggini pasta recipes."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        print("\n[*] Populating Assaggini Pasta Recipes...")

        # Get Viva Italia Group organization
        org = db.query(Organization).filter(Organization.name.ilike("%viva%italia%")).first()
        if not org:
            print("\n[!] Viva Italia Group organization not found. Please create it first.")
            return

        print(f"\n[OK] Using Organization: {org.name} (ID: {org.id})")

        # Get Assaggini Edinburgh site
        site = db.query(Site).filter(
            Site.organization_id == org.id,
            Site.name.ilike("%assaggini%")
        ).first()
        if site:
            print(f"[OK] Using Site: {site.name} (ID: {site.id})")
        else:
            print("[!] No Assaggini site found, creating organization-global recipes")

        # Get a user to be the creator (use first admin or super admin)
        creator = db.query(User).filter(
            User.organization_id == org.id
        ).first()

        if not creator:
            # Try super admin
            creator = db.query(User).filter(User.role == "super_admin").first()

        if not creator:
            print("\n[!] No user found to be the recipe creator")
            return

        print(f"[OK] Using Creator: {creator.email} (ID: {creator.id})")

        # Get or create "Pasta" category (categories are global, not per-organization)
        category = db.query(RecipeCategory).filter(
            RecipeCategory.name == "Pasta"
        ).first()

        if not category:
            category = RecipeCategory(
                name="Pasta",
                sort_order=0
            )
            db.add(category)
            db.commit()
            db.refresh(category)
            print(f"[OK] Created category: Pasta (ID: {category.id})")
        else:
            print(f"[OK] Using existing category: Pasta (ID: {category.id})")

        # Get common units
        units = {}
        for unit_name in ["g", "ml", "each", "tsp", "tbsp"]:
            unit = db.query(IngredientUnit).filter(IngredientUnit.unit == unit_name).first()
            if unit:
                units[unit_name] = unit.id

        # Define all 13 recipes
        recipes_data = [
            {
                "title": "Rigatoni Carbonara",
                "description": "Classic Roman pasta with guanciale, egg, and pecorino",
                "prep_time": 10,
                "cook_time": 15,
                "yield_qty": 1,
                "yield_unit": "portion",
                "method": """1. In a large pan fry the guanciale until crisp and all fat has rendered
2. Add the white wine to deglaze the pan
3. Boil the pasta for 8-10 minutes
4. Once cooked add the pasta to the pan with the guanciale
5. Turn off the heat and add the egg mix
6. Stir continuously until the sauce is smooth and creamy
7. Season with black pepper
8. Plate and finish with pecorino cheese""",
                "ingredients": [
                    ("Rigatoni pasta", 100, "g"),
                    ("Guanciale", 40, "g"),
                    ("Egg yolk", 2, "each"),
                    ("Pecorino cheese", 30, "g"),
                    ("White wine", 30, "ml"),
                    ("Black pepper", 1, "tsp"),
                ]
            },
            {
                "title": "Penne Arrabbiata",
                "description": "Spicy tomato pasta with chili and garlic",
                "prep_time": 5,
                "cook_time": 15,
                "yield_qty": 1,
                "yield_unit": "portion",
                "method": """1. In a large pan heat olive oil
2. Add garlic and chili flakes
3. Add tomato sauce and cook for 5 minutes
4. Boil pasta for 8-10 minutes
5. Add cooked pasta to the sauce
6. Toss well and season
7. Finish with fresh basil and parmesan""",
                "ingredients": [
                    ("Penne pasta", 100, "g"),
                    ("Tomato sauce", 150, "ml"),
                    ("Garlic cloves", 2, "each"),
                    ("Chili flakes", 1, "tsp"),
                    ("Olive oil", 20, "ml"),
                    ("Basil", 5, "g"),
                    ("Parmesan", 20, "g"),
                ]
            },
            {
                "title": "Bucatini Amatriciana",
                "description": "Traditional sauce with guanciale, tomato, and pecorino",
                "prep_time": 10,
                "cook_time": 20,
                "yield_qty": 1,
                "yield_unit": "portion",
                "method": """1. Fry guanciale until crispy
2. Add white wine to deglaze
3. Add tomato sauce and cook for 10 minutes
4. Boil bucatini for 10-12 minutes
5. Add pasta to sauce
6. Toss and season
7. Finish with pecorino and black pepper""",
                "ingredients": [
                    ("Bucatini pasta", 100, "g"),
                    ("Guanciale", 40, "g"),
                    ("Tomato sauce", 150, "ml"),
                    ("White wine", 30, "ml"),
                    ("Pecorino cheese", 30, "g"),
                    ("Black pepper", 1, "tsp"),
                ]
            },
            {
                "title": "Spaghetti Pomodoro",
                "description": "Simple and fresh tomato sauce with basil",
                "prep_time": 5,
                "cook_time": 15,
                "yield_qty": 1,
                "yield_unit": "portion",
                "method": """1. Heat olive oil in a pan
2. Add garlic and cook until fragrant
3. Add tomato sauce and cook for 10 minutes
4. Boil spaghetti for 8-10 minutes
5. Add pasta to sauce
6. Toss with fresh basil
7. Finish with parmesan""",
                "ingredients": [
                    ("Spaghetti pasta", 100, "g"),
                    ("Tomato sauce", 150, "ml"),
                    ("Garlic cloves", 2, "each"),
                    ("Olive oil", 20, "ml"),
                    ("Basil", 5, "g"),
                    ("Parmesan", 20, "g"),
                ]
            },
            {
                "title": "Radiatori Norma",
                "description": "Sicilian pasta with eggplant, tomato, and ricotta salata",
                "prep_time": 15,
                "cook_time": 20,
                "yield_qty": 1,
                "yield_unit": "portion",
                "method": """1. Dice and fry eggplant until golden
2. In separate pan, cook tomato sauce
3. Boil radiatori for 8-10 minutes
4. Combine pasta, eggplant, and sauce
5. Add fresh basil
6. Top with ricotta salata""",
                "ingredients": [
                    ("Radiatori pasta", 100, "g"),
                    ("Eggplant", 80, "g"),
                    ("Tomato sauce", 150, "ml"),
                    ("Ricotta salata", 30, "g"),
                    ("Basil", 5, "g"),
                    ("Olive oil", 30, "ml"),
                ]
            },
            {
                "title": "Pici Cacio e Pepe",
                "description": "Roman pasta with pecorino and black pepper",
                "prep_time": 5,
                "cook_time": 10,
                "yield_qty": 1,
                "yield_unit": "portion",
                "method": """1. Boil pici pasta for 6-8 minutes
2. Reserve pasta water
3. In a pan, toast black pepper
4. Add pasta water to create emulsion
5. Add cooked pasta
6. Remove from heat and add pecorino
7. Toss vigorously until creamy""",
                "ingredients": [
                    ("Pici pasta", 100, "g"),
                    ("Pecorino cheese", 40, "g"),
                    ("Black pepper", 2, "tsp"),
                ]
            },
            {
                "title": "Paccheri Gamberi e Limone",
                "description": "Prawns with lemon, garlic, and white wine",
                "prep_time": 10,
                "cook_time": 15,
                "yield_qty": 1,
                "yield_unit": "portion",
                "method": """1. Sauté garlic in olive oil
2. Add prawns and cook until pink
3. Add white wine and lemon juice
4. Boil paccheri for 10-12 minutes
5. Add pasta to prawn sauce
6. Toss with parsley and lemon zest
7. Season and serve""",
                "ingredients": [
                    ("Paccheri pasta", 100, "g"),
                    ("Prawns", 80, "g"),
                    ("Garlic cloves", 2, "each"),
                    ("White wine", 50, "ml"),
                    ("Lemon", 1, "each"),
                    ("Parsley", 5, "g"),
                    ("Olive oil", 20, "ml"),
                ]
            },
            {
                "title": "Tagliolini Aglio Olio e Peperoncino",
                "description": "Simple pasta with garlic, oil, and chili",
                "prep_time": 5,
                "cook_time": 10,
                "yield_qty": 1,
                "yield_unit": "portion",
                "method": """1. Boil tagliolini for 6-8 minutes
2. In a pan, heat olive oil
3. Add sliced garlic and chili flakes
4. Add pasta and pasta water
5. Toss until emulsified
6. Finish with parsley""",
                "ingredients": [
                    ("Tagliolini pasta", 100, "g"),
                    ("Garlic cloves", 3, "each"),
                    ("Chili flakes", 1, "tsp"),
                    ("Olive oil", 40, "ml"),
                    ("Parsley", 5, "g"),
                ]
            },
            {
                "title": "Orecchiette Verde",
                "description": "Ear-shaped pasta with broccoli and garlic",
                "prep_time": 10,
                "cook_time": 15,
                "yield_qty": 1,
                "yield_unit": "portion",
                "method": """1. Blanch broccoli florets
2. Boil orecchiette for 10-12 minutes
3. Sauté garlic and chili in olive oil
4. Add broccoli and mash slightly
5. Add pasta and toss
6. Finish with parmesan""",
                "ingredients": [
                    ("Orecchiette pasta", 100, "g"),
                    ("Broccoli", 100, "g"),
                    ("Garlic cloves", 2, "each"),
                    ("Chili flakes", 1, "tsp"),
                    ("Olive oil", 30, "ml"),
                    ("Parmesan", 20, "g"),
                ]
            },
            {
                "title": "Reginette Lamb Ragu",
                "description": "Rich slow-cooked lamb sauce with ribbon pasta",
                "prep_time": 20,
                "cook_time": 120,
                "yield_qty": 1,
                "yield_unit": "portion",
                "method": """1. Brown lamb mince in olive oil
2. Add onions, carrots, and celery
3. Add tomato paste and cook out
4. Add red wine and reduce
5. Add tomatoes and simmer for 2 hours
6. Boil reginette for 8-10 minutes
7. Toss pasta with ragu
8. Finish with pecorino""",
                "ingredients": [
                    ("Reginette pasta", 100, "g"),
                    ("Lamb mince", 100, "g"),
                    ("Tomato sauce", 150, "ml"),
                    ("Red wine", 50, "ml"),
                    ("Onion", 40, "g"),
                    ("Carrot", 30, "g"),
                    ("Celery", 30, "g"),
                    ("Pecorino cheese", 20, "g"),
                ]
            },
            {
                "title": "Gnocchi al Pesto",
                "description": "Potato dumplings with basil pesto",
                "prep_time": 10,
                "cook_time": 5,
                "yield_qty": 1,
                "yield_unit": "portion",
                "method": """1. Boil gnocchi until they float (2-3 minutes)
2. In a bowl, mix pesto with pasta water
3. Drain gnocchi and add to pesto
4. Toss gently
5. Finish with parmesan and pine nuts""",
                "ingredients": [
                    ("Gnocchi", 120, "g"),
                    ("Pesto", 40, "g"),
                    ("Parmesan", 20, "g"),
                    ("Pine nuts", 10, "g"),
                ]
            },
            {
                "title": "Girasoli Pistachio",
                "description": "Sunflower-shaped filled pasta with pistachio cream",
                "prep_time": 5,
                "cook_time": 8,
                "yield_qty": 1,
                "yield_unit": "portion",
                "method": """1. Boil girasoli for 6-8 minutes
2. In a pan, heat pistachio cream
3. Add butter and pasta water
4. Add cooked pasta and toss
5. Finish with crushed pistachios and parmesan""",
                "ingredients": [
                    ("Girasoli pasta", 120, "g"),
                    ("Pistachio cream", 50, "g"),
                    ("Butter", 20, "g"),
                    ("Pistachios", 15, "g"),
                    ("Parmesan", 15, "g"),
                ]
            },
            {
                "title": "Ravioli Burro e Salvia",
                "description": "Filled pasta with butter and sage sauce",
                "prep_time": 5,
                "cook_time": 8,
                "yield_qty": 1,
                "yield_unit": "portion",
                "method": """1. Boil ravioli for 6-8 minutes
2. In a pan, melt butter
3. Add sage leaves and let sizzle
4. Add cooked ravioli gently
5. Toss carefully
6. Finish with parmesan and black pepper""",
                "ingredients": [
                    ("Ravioli", 120, "g"),
                    ("Butter", 40, "g"),
                    ("Sage leaves", 5, "each"),
                    ("Parmesan", 20, "g"),
                    ("Black pepper", 1, "tsp"),
                ]
            },
        ]

        created_recipes = []

        print(f"\n[*] Creating {len(recipes_data)} recipes...")

        for recipe_data in recipes_data:
            # Check if recipe already exists
            existing = db.query(Recipe).filter(
                Recipe.organization_id == org.id,
                Recipe.title == recipe_data["title"]
            ).first()

            if existing:
                print(f"[SKIP] Recipe '{recipe_data['title']}' already exists")
                created_recipes.append(existing)
                continue

            # Create recipe
            recipe = Recipe(
                organization_id=org.id,
                site_id=site.id if site else None,
                category_id=category.id,
                title=recipe_data["title"],
                description=recipe_data["description"],
                method=recipe_data["method"],
                prep_time_minutes=recipe_data["prep_time"],
                cook_time_minutes=recipe_data["cook_time"],
                yield_quantity=Decimal(str(recipe_data["yield_qty"])),
                yield_unit=recipe_data["yield_unit"],
                is_archived=False,
                created_by_user_id=creator.id
            )
            db.add(recipe)
            db.flush()

            # Add ingredients
            for idx, (name, quantity, unit_name) in enumerate(recipe_data["ingredients"]):
                ingredient = RecipeIngredient(
                    recipe_id=recipe.id,
                    name=name,
                    quantity=Decimal(str(quantity)),
                    unit_id=units.get(unit_name),
                    order_index=idx
                )
                db.add(ingredient)

            db.commit()
            db.refresh(recipe)
            created_recipes.append(recipe)
            print(f"[OK] Created recipe: {recipe.title} (ID: {recipe.id})")

        # Create Recipe Book
        print(f"\n[*] Creating Recipe Book...")

        book = db.query(RecipeBook).filter(
            RecipeBook.organization_id == org.id,
            RecipeBook.title == "Assaggini Pasta Collection"
        ).first()

        if book:
            print(f"[SKIP] Recipe book already exists (ID: {book.id})")
        else:
            book = RecipeBook(
                organization_id=org.id,
                site_id=site.id if site else None,
                title="Assaggini Pasta Collection",
                description="Complete collection of pasta recipes from the Assaggini training manual",
                is_active=True,
                created_by_user_id=creator.id
            )
            db.add(book)
            db.commit()
            db.refresh(book)
            print(f"[OK] Created recipe book: {book.title} (ID: {book.id})")

        # Add recipes to book
        print(f"\n[*] Adding recipes to book...")
        for idx, recipe in enumerate(created_recipes):
            # Check if already assigned
            existing_assignment = db.query(RecipeBookRecipe).filter(
                RecipeBookRecipe.recipe_book_id == book.id,
                RecipeBookRecipe.recipe_id == recipe.id
            ).first()

            if existing_assignment:
                print(f"[SKIP] Recipe '{recipe.title}' already in book")
                continue

            assignment = RecipeBookRecipe(
                recipe_book_id=book.id,
                recipe_id=recipe.id,
                order_index=idx
            )
            db.add(assignment)

        db.commit()
        print(f"[OK] Added {len(created_recipes)} recipes to book")

        print(f"\n[SUCCESS] Assaggini pasta recipes populated successfully!")
        print(f"  - Organization: {org.name}")
        print(f"  - Site: {site.name if site else 'Organization-global'}")
        print(f"  - Category: Pasta")
        print(f"  - Recipes created: {len(created_recipes)}")
        print(f"  - Recipe book: Assaggini Pasta Collection")

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    populate_assaggini_recipes()
