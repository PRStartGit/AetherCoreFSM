from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_super_admin
from app.models.user import User
from app.models.recipe_category import RecipeCategory
from app.schemas.recipe_category import RecipeCategoryResponse, RecipeCategoryCreate, RecipeCategoryUpdate

router = APIRouter()


@router.get("", response_model=List[RecipeCategoryResponse])
def get_recipe_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all recipe categories"""
    categories = db.query(RecipeCategory).order_by(
        RecipeCategory.sort_order
    ).all()
    return categories


@router.get("/{category_id}", response_model=RecipeCategoryResponse)
def get_recipe_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific recipe category by ID"""
    category = db.query(RecipeCategory).filter(RecipeCategory.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe category not found"
        )
    return category


@router.post("", response_model=RecipeCategoryResponse, status_code=status.HTTP_201_CREATED)
def create_recipe_category(
    category_data: RecipeCategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Create a new recipe category (Super Admin only)"""
    # Check if name already exists
    existing = db.query(RecipeCategory).filter(
        RecipeCategory.name == category_data.name
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Recipe category '{category_data.name}' already exists"
        )

    # Get the next sort order
    max_sort_order = db.query(RecipeCategory).count()

    new_category = RecipeCategory(
        name=category_data.name,
        sort_order=category_data.sort_order if category_data.sort_order is not None else max_sort_order
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@router.put("/{category_id}", response_model=RecipeCategoryResponse)
def update_recipe_category(
    category_id: int,
    category_data: RecipeCategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Update a recipe category (Super Admin only)"""
    category = db.query(RecipeCategory).filter(RecipeCategory.id == category_id).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe category not found"
        )

    # Check if new name conflicts with another category
    if category_data.name and category_data.name != category.name:
        existing = db.query(RecipeCategory).filter(
            RecipeCategory.name == category_data.name,
            RecipeCategory.id != category_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Recipe category '{category_data.name}' already exists"
            )

    # Update fields
    update_data = category_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(category, field, value)

    db.commit()
    db.refresh(category)

    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Delete a recipe category (Super Admin only)"""
    category = db.query(RecipeCategory).filter(RecipeCategory.id == category_id).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe category not found"
        )

    # Check if category is being used by any recipes
    if category.recipes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete category '{category.name}' as it is being used by {len(category.recipes)} recipe(s)"
        )

    db.delete(category)
    db.commit()

    return None
