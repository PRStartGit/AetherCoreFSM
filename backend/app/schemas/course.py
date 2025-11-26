from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.schemas.course_category import CourseCategoryResponse
from app.schemas.course_module import CourseModuleResponse


class CourseBase(BaseModel):
    """Base course schema."""
    title: str
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    category_id: Optional[int] = None


class CourseCreate(CourseBase):
    """Course creation schema."""
    is_published: bool = False


class CourseUpdate(BaseModel):
    """Course update schema."""
    title: Optional[str] = None
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    category_id: Optional[int] = None
    is_published: Optional[bool] = None


class CourseResponse(CourseBase):
    """Course response schema."""
    id: int
    is_published: bool
    created_by_user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    category: Optional[CourseCategoryResponse] = None

    class Config:
        from_attributes = True


class CourseWithModulesResponse(CourseResponse):
    """Course response with modules."""
    modules: List[CourseModuleResponse] = []

    class Config:
        from_attributes = True
