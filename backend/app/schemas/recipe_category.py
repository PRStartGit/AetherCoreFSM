from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class RecipeCategoryBase(BaseModel):
    """Base schema for RecipeCategory"""
    name: str = Field(..., min_length=1, max_length=100)
    sort_order: int = 0


class RecipeCategoryCreate(RecipeCategoryBase):
    """Schema for creating a new recipe category"""
    sort_order: Optional[int] = None


class RecipeCategoryUpdate(BaseModel):
    """Schema for updating a recipe category"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    sort_order: Optional[int] = None


class RecipeCategoryResponse(RecipeCategoryBase):
    """Response schema for RecipeCategory"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
