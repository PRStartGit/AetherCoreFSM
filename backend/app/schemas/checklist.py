from pydantic import BaseModel, field_serializer
from typing import Optional, List
from datetime import datetime, date, time
from app.models.checklist import ChecklistStatus


class ChecklistItemData(BaseModel):
    """Checklist item data."""
    item_name: str
    is_completed: bool = False
    notes: Optional[str] = None
    item_data: Optional[dict] = None
    photo_url: Optional[str] = None
    task_id: int


class ChecklistBase(BaseModel):
    """Base checklist schema."""
    checklist_date: date
    category_id: int
    site_id: int


class ChecklistCreate(ChecklistBase):
    """Checklist creation schema."""
    pass


class ChecklistUpdate(BaseModel):
    """Checklist update schema."""
    status: Optional[ChecklistStatus] = None
    completed_by_id: Optional[int] = None


class ChecklistItemUpdate(BaseModel):
    """Update checklist item."""
    is_completed: bool
    notes: Optional[str] = None
    item_data: Optional[dict] = None
    photo_url: Optional[str] = None


class CategoryInfo(BaseModel):
    """Category information for checklist response."""
    id: int
    name: str
    closes_at: Optional[str] = None

    model_config = {"from_attributes": True}

    @field_serializer('closes_at', when_used='always')
    def serialize_closes_at(self, closes_at):
        """Convert time object to string."""
        if closes_at is None:
            return None
        if isinstance(closes_at, time):
            return closes_at.strftime('%H:%M:%S')
        return str(closes_at)


class ChecklistResponse(ChecklistBase):
    """Checklist response schema."""
    id: int
    status: ChecklistStatus
    total_items: int
    completed_items: int
    completion_percentage: int
    completed_by_id: Optional[int] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    category: Optional[CategoryInfo] = None

    class Config:
        from_attributes = True


class ChecklistWithItems(ChecklistResponse):
    """Checklist with all items."""
    items: List[dict] = []

    class Config:
        from_attributes = True
