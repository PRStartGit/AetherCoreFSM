from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_super_admin
from app.models.user import User
from app.models.ingredient_unit import IngredientUnit
from app.schemas.ingredient_unit import IngredientUnitResponse, IngredientUnitCreate, IngredientUnitUpdate

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


@router.get("/{unit_id}", response_model=IngredientUnitResponse)
def get_ingredient_unit(
    unit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific ingredient unit by ID"""
    unit = db.query(IngredientUnit).filter(IngredientUnit.id == unit_id).first()
    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingredient unit not found"
        )
    return unit


@router.post("", response_model=IngredientUnitResponse, status_code=status.HTTP_201_CREATED)
def create_ingredient_unit(
    unit_data: IngredientUnitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Create a new ingredient unit (Super Admin only)"""
    # Check if name already exists
    existing = db.query(IngredientUnit).filter(
        IngredientUnit.name == unit_data.name
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ingredient unit '{unit_data.name}' already exists"
        )

    # Get the next sort order
    max_sort_order = db.query(IngredientUnit).count()

    new_unit = IngredientUnit(
        name=unit_data.name,
        display_name=unit_data.display_name,
        category=unit_data.category,
        sort_order=unit_data.sort_order if unit_data.sort_order is not None else max_sort_order
    )

    db.add(new_unit)
    db.commit()
    db.refresh(new_unit)

    return new_unit


@router.put("/{unit_id}", response_model=IngredientUnitResponse)
def update_ingredient_unit(
    unit_id: int,
    unit_data: IngredientUnitUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Update an ingredient unit (Super Admin only)"""
    unit = db.query(IngredientUnit).filter(IngredientUnit.id == unit_id).first()

    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingredient unit not found"
        )

    # Check if new name conflicts with another unit
    if unit_data.name and unit_data.name != unit.name:
        existing = db.query(IngredientUnit).filter(
            IngredientUnit.name == unit_data.name,
            IngredientUnit.id != unit_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ingredient unit '{unit_data.name}' already exists"
            )

    # Update fields
    update_data = unit_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(unit, field, value)

    db.commit()
    db.refresh(unit)

    return unit


@router.delete("/{unit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ingredient_unit(
    unit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Delete an ingredient unit (Super Admin only)"""
    unit = db.query(IngredientUnit).filter(IngredientUnit.id == unit_id).first()

    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingredient unit not found"
        )

    db.delete(unit)
    db.commit()

    return None
