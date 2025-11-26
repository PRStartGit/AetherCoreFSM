from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from app.schemas.recipe_ingredient import RecipeIngredientCreate, RecipeIngredientResponse


class RecipeBase(BaseModel):
    """Base schema for Recipe"""
    title: str
    description: Optional[str] = None
    category_id: Optional[int] = None
    method: Optional[str] = None
    prep_time_minutes: Optional[int] = None
    cook_time_minutes: Optional[int] = None
    yield_quantity: Optional[Decimal] = None
    yield_unit: Optional[str] = None
    photo_url: Optional[str] = None


class RecipeCreate(RecipeBase):
    """Create schema for Recipe"""
    ingredients: List[RecipeIngredientCreate] = []


class RecipeUpdate(BaseModel):
    """Update schema for Recipe"""
    title: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    method: Optional[str] = None
    prep_time_minutes: Optional[int] = None
    cook_time_minutes: Optional[int] = None
    yield_quantity: Optional[Decimal] = None
    yield_unit: Optional[str] = None
    photo_url: Optional[str] = None
    is_archived: Optional[bool] = None
    ingredients: Optional[List[RecipeIngredientCreate]] = None


class RecipeResponse(RecipeBase):
    """Response schema for Recipe"""
    id: int
    organization_id: int
    is_archived: bool
    created_by_user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class RecipeWithDetails(RecipeResponse):
    """Recipe with ingredients and allergens"""
    ingredients: List[RecipeIngredientResponse] = []
    allergens: List[str] = []
    total_time_minutes: Optional[int] = None
    category_name: Optional[str] = None

    class Config:
        from_attributes = True


class RecipeScaledIngredient(BaseModel):
    """Scaled ingredient for recipe scaling"""
    name: str
    original_quantity: Optional[Decimal] = None
    scaled_quantity: Optional[Decimal] = None
    unit: Optional[str] = None


class RecipeScaled(RecipeResponse):
    """Recipe with scaled ingredients"""
    original_yield: Optional[Decimal] = None
    scaled_yield: Decimal
    scale_factor: Decimal
    ingredients: List[RecipeScaledIngredient] = []
    allergens: List[str] = []

    class Config:
        from_attributes = True
