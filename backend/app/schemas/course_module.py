from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CourseModuleBase(BaseModel):
    """Base course module schema."""
    title: str
    description: Optional[str] = None
    video_url: Optional[str] = None
    pdf_url: Optional[str] = None
    text_content: Optional[str] = None
    duration_minutes: Optional[int] = None


class CourseModuleCreate(CourseModuleBase):
    """Course module creation schema."""
    course_id: int
    order_index: int = 0


class CourseModuleUpdate(BaseModel):
    """Course module update schema."""
    title: Optional[str] = None
    description: Optional[str] = None
    video_url: Optional[str] = None
    pdf_url: Optional[str] = None
    text_content: Optional[str] = None
    order_index: Optional[int] = None
    duration_minutes: Optional[int] = None


class CourseModuleResponse(CourseModuleBase):
    """Course module response schema."""
    id: int
    course_id: int
    order_index: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ReorderModulesRequest(BaseModel):
    """Request schema for reordering modules."""
    module_orders: dict[int, int]  # {module_id: new_order_index}
