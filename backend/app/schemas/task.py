from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime


class TaskBase(BaseModel):
    """Base task schema."""
    name: str
    description: Optional[str] = None
    order_index: int = 0
    form_config: Optional[Dict[str, Any]] = None
    has_dynamic_form: Optional[bool] = False
    allocated_departments: Optional[List[str]] = None


class TaskCreate(TaskBase):
    """Task creation schema."""
    category_id: int


class TaskUpdate(BaseModel):
    """Task update schema."""
    name: Optional[str] = None
    description: Optional[str] = None
    order_index: Optional[int] = None
    form_config: Optional[Dict[str, Any]] = None
    has_dynamic_form: Optional[bool] = None
    is_active: Optional[bool] = None
    allocated_departments: Optional[List[str]] = None


class TaskResponse(TaskBase):
    """Task response schema."""
    id: int
    category_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TaskWithSites(TaskResponse):
    """Task with assigned sites."""
    site_ids: List[int] = []

    class Config:
        from_attributes = True


class TaskAssignment(BaseModel):
    """Task assignment to sites."""
    task_id: int
    site_ids: List[int]
