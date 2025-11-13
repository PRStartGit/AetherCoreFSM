from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.defect import DefectSeverity, DefectStatus


class DefectBase(BaseModel):
    """Base defect schema."""
    title: str
    description: Optional[str] = None
    severity: DefectSeverity
    photo_url: Optional[str] = None


class DefectCreate(DefectBase):
    """Defect creation schema."""
    site_id: int
    checklist_item_id: Optional[int] = None


class DefectUpdate(BaseModel):
    """Defect update schema."""
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[DefectSeverity] = None
    status: Optional[DefectStatus] = None
    photo_url: Optional[str] = None


class DefectClose(BaseModel):
    """Close defect schema."""
    notes: Optional[str] = None


class DefectResponse(DefectBase):
    """Defect response schema."""
    id: int
    site_id: int
    checklist_item_id: Optional[int] = None
    reported_by_id: int
    closed_by_id: Optional[int] = None
    status: DefectStatus
    created_at: datetime
    closed_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DefectWithDetails(DefectResponse):
    """Defect with reporter and site details."""
    reporter_name: Optional[str] = None
    site_name: Optional[str] = None

    class Config:
        from_attributes = True
