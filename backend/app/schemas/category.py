from pydantic import BaseModel
from typing import Optional
from datetime import datetime, time
from app.models.category import ChecklistFrequency


class CategoryBase(BaseModel):
    """Base category schema."""
    name: str
    description: Optional[str] = None
    frequency: ChecklistFrequency
    closes_at: Optional[time] = None
    is_global: bool = False


class CategoryCreate(CategoryBase):
    """Category creation schema."""
    organization_id: Optional[int] = None


class CategoryUpdate(BaseModel):
    """Category update schema."""
    name: Optional[str] = None
    description: Optional[str] = None
    frequency: Optional[ChecklistFrequency] = None
    closes_at: Optional[time] = None
    is_active: Optional[bool] = None


class CategoryResponse(CategoryBase):
    """Category response schema."""
    id: int
    organization_id: Optional[int] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CategoryWithTasks(CategoryResponse):
    """Category with task count."""
    task_count: int = 0

    class Config:
        from_attributes = True
