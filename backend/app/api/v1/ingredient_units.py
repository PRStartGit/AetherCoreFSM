from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.ingredient_unit import IngredientUnit
from app.schemas.ingredient_unit import IngredientUnitResponse

router = APIRouter()


@router.get("", response_model=List[IngredientUnitResponse])
def get_ingredient_units(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all ingredient units for dropdown"""
    units = db.query(IngredientUnit).order_by(
        IngredientUnit.sort_order
    ).all()
    return units
