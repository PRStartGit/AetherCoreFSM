from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CourseCategoryBase(BaseModel):
    """Base course category schema."""
    name: str
    description: Optional[str] = None


class CourseCategoryCreate(CourseCategoryBase):
    """Course category creation schema."""
    pass


class CourseCategoryUpdate(BaseModel):
    """Course category update schema."""
    name: Optional[str] = None
    description: Optional[str] = None


class CourseCategoryResponse(CourseCategoryBase):
    """Course category response schema."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
