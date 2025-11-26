from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.course_enrollment import EnrollmentStatus


class EnrollmentBase(BaseModel):
    """Base enrollment schema."""
    user_id: int
    course_id: int


class EnrollmentCreate(EnrollmentBase):
    """Enrollment creation schema."""
    pass


class EnrollmentUpdate(BaseModel):
    """Enrollment update schema."""
    status: Optional[EnrollmentStatus] = None
    progress_percentage: Optional[int] = None


class EnrollmentResponse(EnrollmentBase):
    """Enrollment response schema."""
    id: int
    assigned_by_user_id: Optional[int] = None
    enrolled_at: datetime
    status: EnrollmentStatus
    progress_percentage: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    last_accessed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class EnrollmentWithCourseResponse(EnrollmentResponse):
    """Enrollment response with course details."""
    course_title: str
    course_description: Optional[str] = None
    course_thumbnail_url: Optional[str] = None
    course_category_name: Optional[str] = None


class AssignCoursesRequest(BaseModel):
    """Request to assign multiple courses to multiple users."""
    user_ids: List[int]
    course_ids: List[int]
