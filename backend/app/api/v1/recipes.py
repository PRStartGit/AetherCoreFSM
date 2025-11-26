from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from decimal import Decimal
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.recipe_permissions import has_recipe_access, has_recipe_crud
from app.models.user import User
from app.schemas.recipe import (
    RecipeCreate,
    RecipeUpdate,
    RecipeResponse,
    RecipeWithDetails,
    RecipeScaled
)
from app.services.recipe_service import RecipeService
from app.services.allergen_service import AllergenService

router = APIRouter()


@router.post("", response_model=RecipeResponse, status_code=status.HTTP_201_CREATED)
def create_recipe(
    recipe: RecipeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new recipe (CRUD roles only)"""
    # Check CRUD permission
    if not has_recipe_crud(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to create recipes"
        )

    # Check access permission
    if not has_recipe_access(current_user, db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to the Recipe Book module"
        )

    # Use user's organization
    if not current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must belong to an organization"
        )

    return RecipeService.create_recipe(
        recipe,
        current_user.organization_id,
        current_user.id,
        db
    )


@router.get("", response_model=List[RecipeResponse])
def get_recipes(
    search: Optional[str] = Query(None, description="Search recipe titles"),
    category_id: Optional[int] = Query(None, description="Filter by category"),
    allergen: Optional[str] = Query(None, description="Exclude recipes with this allergen"),
    include_archived: bool = Query(False, description="Include archived recipes"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get recipes for user's organization"""
    # Check access permission
    if not has_recipe_access(current_user, db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to the Recipe Book module"
        )

    if not current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must belong to an organization"
        )

    return RecipeService.get_recipes(
        current_user.organization_id,
        db,
        search=search,
        category_id=category_id,
        allergen=allergen,
        include_archived=include_archived,
        skip=skip,
        limit=limit
    )


@router.get("/{recipe_id}", response_model=RecipeWithDetails)
def get_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get recipe by ID with ingredients and allergens"""
    # Check access permission
    if not has_recipe_access(current_user, db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to the Recipe Book module"
        )

    recipe = RecipeService.get_recipe_by_id(recipe_id, db)
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )

    # Check organization match
    if recipe.organization_id != current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Recipe belongs to a different organization"
        )

    # Build response with details
    allergens = AllergenService.get_recipe_allergens(recipe.id, db)
    category_name = recipe.category.name if recipe.category else None

    response_dict = {
        **RecipeResponse.model_validate(recipe).model_dump(),
        "ingredients": recipe.ingredients,
        "allergens": allergens,
        "total_time_minutes": recipe.total_time_minutes,
        "category_name": category_name
    }

    return RecipeWithDetails(**response_dict)


@router.put("/{recipe_id}", response_model=RecipeResponse)
def update_recipe(
    recipe_id: int,
    recipe: RecipeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a recipe (CRUD roles only)"""
    # Check CRUD permission
    if not has_recipe_crud(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to edit recipes"
        )

    # Check access permission
    if not has_recipe_access(current_user, db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to the Recipe Book module"
        )

    # Check recipe exists
    db_recipe = RecipeService.get_recipe_by_id(recipe_id, db)
    if not db_recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )

    # Check organization match
    if db_recipe.organization_id != current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Recipe belongs to a different organization"
        )

    updated = RecipeService.update_recipe(recipe_id, recipe, db)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )

    return updated


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Archive a recipe (CRUD roles only)"""
    # Check CRUD permission
    if not has_recipe_crud(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete recipes"
        )

    # Check access permission
    if not has_recipe_access(current_user, db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to the Recipe Book module"
        )

    # Check recipe exists
    db_recipe = RecipeService.get_recipe_by_id(recipe_id, db)
    if not db_recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )

    # Check organization match
    if db_recipe.organization_id != current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Recipe belongs to a different organization"
        )

    if not RecipeService.delete_recipe(recipe_id, db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )


@router.get("/{recipe_id}/scaled", response_model=RecipeScaled)
def get_scaled_recipe(
    recipe_id: int,
    yield_quantity: Decimal = Query(..., description="New yield quantity"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get recipe with scaled ingredients"""
    # Check access permission
    if not has_recipe_access(current_user, db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to the Recipe Book module"
        )

    recipe = RecipeService.get_recipe_by_id(recipe_id, db)
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )

    # Check organization match
    if recipe.organization_id != current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Recipe belongs to a different organization"
        )

    # Scale ingredients
    scaled_ingredients = RecipeService.scale_recipe(recipe, yield_quantity)

    # Get allergens
    allergens = AllergenService.get_recipe_allergens(recipe.id, db)

    # Calculate scale factor
    scale_factor = yield_quantity / recipe.yield_quantity if recipe.yield_quantity else Decimal(1)

    response_dict = {
        **RecipeResponse.model_validate(recipe).model_dump(),
        "original_yield": recipe.yield_quantity,
        "scaled_yield": yield_quantity,
        "scale_factor": scale_factor,
        "ingredients": scaled_ingredients,
        "allergens": allergens
    }

    return RecipeScaled(**response_dict)
