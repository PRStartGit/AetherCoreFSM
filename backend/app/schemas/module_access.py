"""
Module Access schemas for API requests and responses
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserModuleAccessResponse(BaseModel):
    id: int
    user_id: int
    module_name: str
    granted_at: datetime
    granted_by_user_id: Optional[int]

    class Config:
        from_attributes = True


class GrantModuleAccessRequest(BaseModel):
    module_name: str
