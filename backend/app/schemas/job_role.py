"""
Job Role schemas for API responses
"""
from pydantic import BaseModel, Field
from datetime import datetime


class JobRoleCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    is_system_role: bool = False


class JobRoleUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    is_system_role: bool


class JobRoleResponse(BaseModel):
    id: int
    name: str
    is_system_role: bool
    created_at: datetime

    class Config:
        from_attributes = True
