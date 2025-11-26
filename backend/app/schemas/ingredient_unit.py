from pydantic import BaseModel, Field
from typing import Optional


class IngredientUnitBase(BaseModel):
    """Base schema for IngredientUnit"""
    name: str = Field(..., min_length=1, max_length=50)
    display_name: str = Field(..., min_length=1, max_length=50)
    category: Optional[str] = Field(None, max_length=50)
    sort_order: int = 0


class IngredientUnitCreate(IngredientUnitBase):
    """Schema for creating a new ingredient unit"""
    sort_order: Optional[int] = None


class IngredientUnitUpdate(BaseModel):
    """Schema for updating an ingredient unit"""
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    display_name: Optional[str] = Field(None, min_length=1, max_length=50)
    category: Optional[str] = Field(None, max_length=50)
    sort_order: Optional[int] = None


class IngredientUnitResponse(IngredientUnitBase):
    """Response schema for IngredientUnit"""
    id: int

    class Config:
        from_attributes = True
