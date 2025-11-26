from pydantic import BaseModel
from datetime import datetime


class RecipeCategoryBase(BaseModel):
    """Base schema for RecipeCategory"""
    name: str
    sort_order: int = 0


class RecipeCategoryResponse(RecipeCategoryBase):
    """Response schema for RecipeCategory"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
