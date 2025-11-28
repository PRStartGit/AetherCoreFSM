"""
Recipe Service
Handles recipe CRUD operations, scaling, and related logic
"""
from typing import List, Optional
from decimal import Decimal
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from app.models.recipe import Recipe
from app.models.recipe_ingredient import RecipeIngredient
from app.models.recipe_category import RecipeCategory
from app.schemas.recipe import RecipeCreate, RecipeUpdate, RecipeScaledIngredient
from app.services.allergen_service import AllergenService


class RecipeService:
    """Service for recipe operations"""

    @staticmethod
    def create_recipe(
        recipe_data: RecipeCreate,
        organization_id: int,
        user_id: int,
        db: Session
    ) -> Recipe:
        """
        Create a new recipe with ingredients

        Args:
            recipe_data: Recipe creation data
            organization_id: Organization ID
            user_id: User ID creating the recipe
            db: Database session

        Returns:
            Created Recipe
        """
        # Create recipe
        recipe_dict = recipe_data.model_dump(exclude={'ingredients', 'allergens'})
        db_recipe = Recipe(
            **recipe_dict,
            organization_id=organization_id,
            created_by_user_id=user_id
        )
        db.add(db_recipe)
        db.flush()

        # Add ingredients
        for idx, ingredient in enumerate(recipe_data.ingredients):
            db_ingredient = RecipeIngredient(
                recipe_id=db_recipe.id,
                **ingredient.model_dump(),
                order_index=idx
            )
            db.add(db_ingredient)

        db.commit()
        db.refresh(db_recipe)

        # Handle allergens: use manual selection if provided, otherwise auto-detect
        if recipe_data.allergens:
            # Use manually selected allergens
            AllergenService.update_recipe_allergens(db_recipe.id, set(recipe_data.allergens), db)
        else:
            # Auto-detect allergens from ingredients
            ingredient_names = [ing.name for ing in recipe_data.ingredients]
            allergens = AllergenService.detect_allergens(ingredient_names, db)
            AllergenService.update_recipe_allergens(db_recipe.id, allergens, db)

        return db_recipe

    @staticmethod
    def get_recipe_by_id(recipe_id: int, db: Session) -> Optional[Recipe]:
        """Get recipe by ID with related data"""
        return db.query(Recipe).options(
            joinedload(Recipe.ingredients),
            joinedload(Recipe.allergens),
            joinedload(Recipe.category)
        ).filter(Recipe.id == recipe_id).first()

    @staticmethod
    def get_recipes(
        organization_id: Optional[int],
        db: Session,
        search: Optional[str] = None,
        category_id: Optional[int] = None,
        recipe_book_id: Optional[int] = None,
        allergen: Optional[str] = None,
        include_archived: bool = False,
        skip: int = 0,
        limit: int = 100
    ) -> List[Recipe]:
        """
        Get recipes for an organization with filters

        Args:
            organization_id: Organization ID (None = all organizations for super admin)
            db: Database session
            search: Search term for recipe title
            category_id: Filter by category
            recipe_book_id: Filter by recipe book
            allergen: Filter by allergen (exclude recipes with this allergen)
            include_archived: Include archived recipes
            skip: Pagination offset
            limit: Pagination limit

        Returns:
            List of recipes
        """
        query = db.query(Recipe)

        # Filter by organization if specified
        if organization_id is not None:
            query = query.filter(Recipe.organization_id == organization_id)

        if not include_archived:
            query = query.filter(Recipe.is_archived == False)

        if search:
            query = query.filter(Recipe.title.ilike(f"%{search}%"))

        if category_id:
            query = query.filter(Recipe.category_id == category_id)

        if recipe_book_id:
            # Filter to recipes in this recipe book
            from app.models.recipe_book import RecipeBookRecipe
            recipes_in_book = db.query(RecipeBookRecipe.recipe_id).filter(
                RecipeBookRecipe.recipe_book_id == recipe_book_id
            ).subquery()
            query = query.filter(Recipe.id.in_(recipes_in_book))

        if allergen:
            # Exclude recipes containing this allergen
            from app.models.recipe_allergen import RecipeAllergen
            recipes_with_allergen = db.query(RecipeAllergen.recipe_id).filter(
                RecipeAllergen.allergen == allergen
            ).subquery()
            query = query.filter(~Recipe.id.in_(recipes_with_allergen))

        query = query.options(
            joinedload(Recipe.category),
            joinedload(Recipe.allergens)
        )

        return query.order_by(Recipe.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def update_recipe(
        recipe_id: int,
        recipe_data: RecipeUpdate,
        db: Session
    ) -> Optional[Recipe]:
        """
        Update a recipe

        Args:
            recipe_id: Recipe ID
            recipe_data: Update data
            db: Database session

        Returns:
            Updated recipe
        """
        db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
        if not db_recipe:
            return None

        update_dict = recipe_data.model_dump(exclude_unset=True, exclude={'ingredients', 'allergens'})

        for key, value in update_dict.items():
            setattr(db_recipe, key, value)

        # Update ingredients if provided
        if recipe_data.ingredients is not None:
            # Delete existing ingredients
            db.query(RecipeIngredient).filter(
                RecipeIngredient.recipe_id == recipe_id
            ).delete()

            # Add new ingredients
            for idx, ingredient in enumerate(recipe_data.ingredients):
                db_ingredient = RecipeIngredient(
                    recipe_id=recipe_id,
                    **ingredient.model_dump(),
                    order_index=idx
                )
                db.add(db_ingredient)

        # Handle allergens: use manual selection if provided, otherwise auto-detect
        if recipe_data.allergens is not None:
            # Use manually selected allergens
            AllergenService.update_recipe_allergens(recipe_id, set(recipe_data.allergens), db)
        elif recipe_data.ingredients is not None:
            # Auto-detect allergens from new ingredients
            ingredient_names = [ing.name for ing in recipe_data.ingredients]
            allergens = AllergenService.detect_allergens(ingredient_names, db)
            AllergenService.update_recipe_allergens(recipe_id, allergens, db)

        db.commit()
        db.refresh(db_recipe)
        return db_recipe

    @staticmethod
    def delete_recipe(recipe_id: int, db: Session) -> bool:
        """
        Archive a recipe (soft delete)

        Args:
            recipe_id: Recipe ID
            db: Database session

        Returns:
            True if deleted, False if not found
        """
        db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
        if not db_recipe:
            return False

        db_recipe.is_archived = True
        db.commit()
        return True

    @staticmethod
    def scale_recipe(
        recipe: Recipe,
        new_yield: Decimal
    ) -> List[RecipeScaledIngredient]:
        """
        Scale recipe ingredients to a new yield

        Args:
            recipe: Recipe to scale
            new_yield: New yield quantity

        Returns:
            List of scaled ingredients
        """
        if not recipe.yield_quantity or recipe.yield_quantity == 0:
            # Can't scale without original yield
            return [
                RecipeScaledIngredient(
                    name=ing.name,
                    original_quantity=ing.quantity,
                    scaled_quantity=ing.quantity,
                    unit=ing.unit
                )
                for ing in recipe.ingredients
            ]

        scale_factor = new_yield / recipe.yield_quantity
        scaled_ingredients = []

        for ingredient in recipe.ingredients:
            scaled_qty = None
            if ingredient.quantity:
                scaled_qty = ingredient.quantity * scale_factor
                # Round to 2 decimal places
                scaled_qty = round(scaled_qty, 2)

            scaled_ingredients.append(RecipeScaledIngredient(
                name=ingredient.name,
                original_quantity=ingredient.quantity,
                scaled_quantity=scaled_qty,
                unit=ingredient.unit
            ))

        return scaled_ingredients
