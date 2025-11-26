from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ModuleProgressBase(BaseModel):
    """Base module progress schema."""
    enrollment_id: int
    module_id: int


class ModuleProgressCreate(ModuleProgressBase):
    """Module progress creation schema."""
    pass


class ModuleProgressUpdate(BaseModel):
    """Module progress update schema."""
    is_completed: Optional[bool] = None
    time_spent_seconds: Optional[int] = None
    last_position_seconds: Optional[int] = None


class ModuleProgressResponse(ModuleProgressBase):
    """Module progress response schema."""
    id: int
    is_completed: bool
    completed_at: Optional[datetime] = None
    time_spent_seconds: int
    last_position_seconds: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CompleteModuleRequest(BaseModel):
    """Request to mark a module as complete."""
    time_spent_seconds: int = 0
