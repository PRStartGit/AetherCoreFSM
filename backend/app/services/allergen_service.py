"""
Allergen Detection Service
Detects allergens based on ingredient names using keyword matching
"""
from typing import List, Set
from sqlalchemy.orm import Session
from app.models.allergen_keyword import AllergenKeyword
from app.models.recipe_allergen import RecipeAllergen


class AllergenService:
    """Service for detecting allergens in recipes"""

    @staticmethod
    def detect_allergens(ingredient_names: List[str], db: Session) -> Set[str]:
        """
        Detect allergens from a list of ingredient names

        Args:
            ingredient_names: List of ingredient names
            db: Database session

        Returns:
            Set of detected allergen names
        """
        if not ingredient_names:
            return set()

        detected_allergens = set()

        # Get all allergen keywords
        keywords = db.query(AllergenKeyword).all()

        # Check each ingredient against each keyword
        for ingredient in ingredient_names:
            ingredient_lower = ingredient.lower().strip()

            for keyword_entry in keywords:
                # Check if keyword appears in ingredient name
                if keyword_entry.keyword in ingredient_lower:
                    detected_allergens.add(keyword_entry.allergen)

        return detected_allergens

    @staticmethod
    def update_recipe_allergens(recipe_id: int, allergens: Set[str], db: Session) -> None:
        """
        Update the allergens for a recipe

        Args:
            recipe_id: Recipe ID
            allergens: Set of allergen names
            db: Database session
        """
        # Delete existing allergens
        db.query(RecipeAllergen).filter(
            RecipeAllergen.recipe_id == recipe_id
        ).delete()

        # Insert new allergens
        for allergen in allergens:
            db_allergen = RecipeAllergen(
                recipe_id=recipe_id,
                allergen=allergen
            )
            db.add(db_allergen)

        db.commit()

    @staticmethod
    def get_recipe_allergens(recipe_id: int, db: Session) -> List[str]:
        """
        Get list of allergens for a recipe

        Args:
            recipe_id: Recipe ID
            db: Database session

        Returns:
            List of allergen names
        """
        allergens = db.query(RecipeAllergen).filter(
            RecipeAllergen.recipe_id == recipe_id
        ).all()

        return [a.allergen for a in allergens]
