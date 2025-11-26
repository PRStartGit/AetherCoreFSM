from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class RecipeIngredientBase(BaseModel):
    """Base schema for RecipeIngredient"""
    name: str
    quantity: Optional[Decimal] = None
    unit: Optional[str] = None
    order_index: int = 0


class RecipeIngredientCreate(RecipeIngredientBase):
    """Create schema for RecipeIngredient"""
    pass


class RecipeIngredientUpdate(BaseModel):
    """Update schema for RecipeIngredient"""
    name: Optional[str] = None
    quantity: Optional[Decimal] = None
    unit: Optional[str] = None
    order_index: Optional[int] = None


class RecipeIngredientResponse(RecipeIngredientBase):
    """Response schema for RecipeIngredient"""
    id: int
    recipe_id: int

    class Config:
        from_attributes = True
