"""
Job Role schemas for API responses
"""
from pydantic import BaseModel
from datetime import datetime


class JobRoleResponse(BaseModel):
    id: int
    name: str
    is_system_role: bool
    created_at: datetime

    class Config:
        from_attributes = True
