"""
Notification schemas for API responses
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    notification_type: str
    related_id: Optional[int]
    related_url: Optional[str]
    is_read: bool
    read_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationMarkRead(BaseModel):
    notification_ids: list[int]
