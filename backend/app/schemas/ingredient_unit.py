from pydantic import BaseModel
from typing import Optional


class IngredientUnitBase(BaseModel):
    """Base schema for IngredientUnit"""
    name: str
    display_name: str
    category: Optional[str] = None
    sort_order: int = 0


class IngredientUnitResponse(IngredientUnitBase):
    """Response schema for IngredientUnit"""
    id: int

    class Config:
        from_attributes = True
