"""
Update recipe allergens based on ingredient analysis.
This script analyzes ingredients in existing recipes and infers allergens.
"""
import sys
import os
import re

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal, engine, Base
from app.models.recipe import Recipe
from app.models.recipe_ingredient import RecipeIngredient
from app.models.recipe_allergen import RecipeAllergen
from app.models.organization import Organization
from sqlalchemy.orm import joinedload


# UK 14 Allergens with ingredient patterns that indicate their presence
ALLERGEN_INGREDIENTS = {
    "Cereals containing gluten": [
        # Pasta types
        r'\bpasta\b', r'\bspaghetti\b', r'\bpenne\b', r'\brigatoni\b', r'\bfusilli\b',
        r'\blinguine\b', r'\btagliatelle\b', r'\bfettuccine\b', r'\blasagne\b', r'\blasagna\b',
        r'\bmacaroni\b', r'\borzo\b', r'\bgnocchi\b', r'\bravioli\b', r'\btortellini\b',
        r'\bcannelloni\b', r'\bfarfalle\b', r'\bpaccheri\b', r'\bpappardelle\b',
        # Bread and baked goods
        r'\bbread\b', r'\bflour\b', r'\bbatter\b', r'\bbreadcrumb', r'\bcrumb\b',
        r'\bpanko\b', r'\bbruschetta\b', r'\bfocaccia\b', r'\bciabatta\b', r'\bcrostini\b',
        r'\bpizza\b', r'\bdough\b', r'\bpastry\b', r'\bcroissant\b', r'\bcrouton',
        # Cereals and grains
        r'\bwheat\b', r'\bbarley\b', r'\brye\b', r'\boat', r'\bcouscous\b',
        r'\bbulgar\b', r'\bbulgur\b', r'\bsemolina\b',
        # Sauces that typically contain flour
        r'\bbechamel\b', r'\broux\b',
        # Breaded items
        r'\bbreaded\b', r'\bpanfried\b', r'\bcoated\b',
    ],
    "Milk": [
        # Cheese varieties
        r'\bcheese\b', r'\bparmesan\b', r'\bparmigiano\b', r'\bmozzarella\b', r'\bbrie\b',
        r'\bgorgonzola\b', r'\bmascarpone\b', r'\bricotta\b', r'\bpecorino\b', r'\bcheddar\b',
        r'\bgoat.?s?\s*cheese\b', r'\bfeta\b', r'\bhalloumi\b', r'\bburrata\b', r'\bstracchino\b',
        r'\btaleggio\b', r'\bscamorza\b', r'\bprovolone\b', r'\bfontina\b',
        # Cream and dairy
        r'\bcream\b', r'\bdouble\s*cream\b', r'\bsingle\s*cream\b', r'\bwhipping\s*cream\b',
        r'\bsour\s*cream\b', r'\bcreme\s*fraiche\b', r'\bfraiche\b',
        # Butter and milk
        r'\bbutter\b', r'\bmilk\b', r'\byogh?urt\b',
        # Dairy products
        r'\bice\s*cream\b', r'\bgelato\b', r'\bpanna\s*cotta\b',
        # Carbonara (traditionally has cheese)
        r'\bcarbonara\b',
    ],
    "Eggs": [
        r'\begg\b', r'\beggs\b',
        # Mayonnaise and sauces
        r'\bmayo\b', r'\bmayonnaise\b', r'\baioli\b', r'\bhollandaise\b',
        # Pasta that typically contains eggs
        r'\bcarbonara\b', r'\bmeringue\b', r'\bcustard\b',
        # Batter and breaded items often contain egg
        r'\bbatter\b', r'\bbreaded\b',
    ],
    "Fish": [
        r'\bfish\b', r'\bsalmon\b', r'\btuna\b', r'\bcod\b', r'\banchov', r'\bsea\s*bass\b',
        r'\btrout\b', r'\bmackerel\b', r'\bswordfish\b', r'\bsardine', r'\bhalibut\b',
        r'\bhaddock\b', r'\bplaice\b', r'\bsole\b', r'\bseabass\b', r'\bbranzino\b',
        r'\bpesce\b',  # Italian for fish
        # Fish-based sauces
        r'\bworcestershire\b', r'\bfish\s*sauce\b',
    ],
    "Crustaceans": [
        r'\bprawn', r'\bshrimp', r'\blobster\b', r'\bcrab\b', r'\blangoustine',
        r'\bcrayfish\b', r'\bcrawfish\b', r'\bscampi\b',
    ],
    "Molluscs": [
        r'\bcalamari\b', r'\bsquid\b', r'\bmussel', r'\bclam\b', r'\boyster',
        r'\bscallop', r'\boctopus\b', r'\bsnail', r'\bescargot',
    ],
    "Nuts": [
        r'\balmond', r'\bwalnut', r'\bhazelnut', r'\bcashew', r'\bpistachio',
        r'\bpecan', r'\bmacadamia\b', r'\bbrazil\s*nut', r'\bchestnut',
        r'\bpine\s*nut', r'\bpinoli\b', r'\bnuts?\b',  # Generic "nut" or "nuts"
        # Nut products
        r'\bpraline\b', r'\bfrancipane\b', r'\bfrangipane\b', r'\bnut\s*brittle\b',
        r'\bamaretto\b', r'\bpesto\b',  # Traditional pesto contains pine nuts
    ],
    "Peanuts": [
        r'\bpeanut', r'\bgroundnut\b', r'\bsatay\b',
    ],
    "Sesame seeds": [
        r'\bsesame\b', r'\btahini\b', r'\bhalva\b', r'\bhummus\b', r'\bhumus\b',
    ],
    "Soybeans": [
        r'\bsoy\b', r'\bsoya\b', r'\btofu\b', r'\bedamame\b', r'\bmiso\b',
        r'\bteriyaki\b', r'\btamari\b',
        # Soy sauce variations
        r'\bsoy\s*sauce\b', r'\bsoya\s*sauce\b',
    ],
    "Celery": [
        r'\bcelery\b', r'\bceleriac\b',
    ],
    "Mustard": [
        r'\bmustard\b', r'\bdijon\b',
    ],
    "Sulphur dioxide and sulphites": [
        # Wine and vinegar
        r'\bwine\b', r'\bvinegar\b', r'\bprosecco\b', r'\bchampagne\b',
        # Dried fruits
        r'\bdried\s*fruit', r'\bdried\s*apricot', r'\braisin', r'\bsultana',
        r'\bdried\s*fig', r'\bprune\b',
        # Preserved items
        r'\bpickle', r'\bpreserved\b',
    ],
    "Lupin": [
        r'\blupin\b',
    ],
}


def analyze_ingredients_for_allergens(ingredients: list) -> set:
    """
    Analyze a list of ingredients and return a set of allergens.

    Args:
        ingredients: List of ingredient dictionaries with 'name' key

    Returns:
        Set of allergen names
    """
    detected_allergens = set()

    # Combine all ingredient names into one text for analysis
    all_text = " ".join([ing.get("name", "") if isinstance(ing, dict) else str(ing) for ing in ingredients])
    all_text_lower = all_text.lower()

    # Check each allergen category
    for allergen, patterns in ALLERGEN_INGREDIENTS.items():
        for pattern in patterns:
            if re.search(pattern, all_text_lower, re.IGNORECASE):
                detected_allergens.add(allergen)
                break  # Found this allergen, move to next

    return detected_allergens


def update_recipe_allergens_in_database():
    """Update allergens for all Tony Macaroni recipes based on ingredient analysis."""
    print("=" * 60)
    print("UPDATING RECIPE ALLERGENS")
    print("=" * 60)

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Get Viva Italia Group organization
        org = db.query(Organization).filter(Organization.name.ilike("%viva%italia%")).first()
        if not org:
            print("[ERROR] Viva Italia Group organization not found!")
            return
        print(f"[OK] Organization: {org.name} (ID: {org.id})")

        # Get all recipes with ingredients
        recipes = db.query(Recipe).options(
            joinedload(Recipe.ingredients)
        ).filter(
            Recipe.organization_id == org.id
        ).all()

        print(f"[OK] Found {len(recipes)} recipes to analyze")

        updated_count = 0
        allergen_summary = {}

        for recipe in recipes:
            # Get ingredient names
            ingredient_data = [{"name": ing.name} for ing in recipe.ingredients]

            # Analyze ingredients for allergens
            detected_allergens = analyze_ingredients_for_allergens(ingredient_data)

            # Get current allergens from database
            current_allergens = db.query(RecipeAllergen).filter(
                RecipeAllergen.recipe_id == recipe.id
            ).all()
            current_allergen_set = {a.allergen for a in current_allergens}

            # Merge detected with current (don't remove manually added ones)
            new_allergens = detected_allergens - current_allergen_set

            if new_allergens:
                # Add new allergens
                for allergen in new_allergens:
                    allergen_record = RecipeAllergen(
                        recipe_id=recipe.id,
                        allergen=allergen
                    )
                    db.add(allergen_record)
                    allergen_summary[allergen] = allergen_summary.get(allergen, 0) + 1

                updated_count += 1
                print(f"  [{recipe.id}] {recipe.title}: +{len(new_allergens)} allergens ({', '.join(sorted(new_allergens))})")

        db.commit()

        print(f"\n[SUMMARY]")
        print(f"  Recipes updated: {updated_count}")
        print(f"\n  Allergens added:")
        for allergen, count in sorted(allergen_summary.items(), key=lambda x: -x[1]):
            print(f"    {allergen}: {count}")

        # Final allergen count per recipe
        print(f"\n  Verifying final allergen distribution...")
        all_allergen_counts = db.query(
            RecipeAllergen.allergen,
            db.func.count(RecipeAllergen.id)
        ).join(Recipe).filter(
            Recipe.organization_id == org.id
        ).group_by(RecipeAllergen.allergen).all()

        print(f"\n  Final allergen counts:")
        for allergen, count in sorted(all_allergen_counts, key=lambda x: -x[1]):
            print(f"    {allergen}: {count} recipes")

    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    update_recipe_allergens_in_database()
