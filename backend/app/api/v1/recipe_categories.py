from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.recipe_category import RecipeCategory
from app.schemas.recipe_category import RecipeCategoryResponse

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
