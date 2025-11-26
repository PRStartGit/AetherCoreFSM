from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class RecipeBookBase(BaseModel):
    """Base schema for RecipeBook"""
    title: str
    description: Optional[str] = None
    site_id: Optional[int] = None  # NULL = global to organization
    is_active: bool = True


class RecipeBookCreate(RecipeBookBase):
    """Create schema for RecipeBook"""
    pass


class RecipeBookUpdate(BaseModel):
    """Update schema for RecipeBook"""
    title: Optional[str] = None
    description: Optional[str] = None
    site_id: Optional[int] = None
    is_active: Optional[bool] = None


class RecipeBookResponse(RecipeBookBase):
    """Response schema for RecipeBook"""
    id: int
    organization_id: int
    created_by_user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class RecipeInBook(BaseModel):
    """Minimal recipe info for listing recipes in a book"""
    id: int
    title: str
    description: Optional[str] = None
    photo_url: Optional[str] = None
    category_id: Optional[int] = None
    order_index: int = 0
    added_at: datetime

    class Config:
        from_attributes = True


class RecipeBookWithRecipes(RecipeBookResponse):
    """RecipeBook with its assigned recipes"""
    recipes: List[RecipeInBook] = []
    recipe_count: int = 0

    class Config:
        from_attributes = True


class AddRecipeToBook(BaseModel):
    """Schema for adding a recipe to a book"""
    recipe_id: int
    order_index: Optional[int] = 0


class RemoveRecipeFromBook(BaseModel):
    """Schema for removing a recipe from a book"""
    recipe_id: int
