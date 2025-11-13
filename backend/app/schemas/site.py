from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SiteBase(BaseModel):
    """Base site schema."""
    name: str
    site_code: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    postcode: Optional[str] = None
    country: str = "UK"


class SiteCreate(SiteBase):
    """Site creation schema."""
    organization_id: int


class SiteUpdate(BaseModel):
    """Site update schema."""
    name: Optional[str] = None
    site_code: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    postcode: Optional[str] = None
    country: Optional[str] = None
    is_active: Optional[bool] = None
    daily_report_enabled: Optional[bool] = None
    daily_report_time: Optional[str] = None
    weekly_report_enabled: Optional[bool] = None
    weekly_report_day: Optional[int] = None
    weekly_report_time: Optional[str] = None
    report_recipients: Optional[str] = None


class SiteResponse(SiteBase):
    """Site response schema."""
    id: int
    organization_id: int
    is_active: bool
    daily_report_enabled: bool
    daily_report_time: str
    weekly_report_enabled: bool
    weekly_report_day: int
    weekly_report_time: str
    report_recipients: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SiteWithRAG(SiteResponse):
    """Site response with RAG status."""
    rag_status: str = "green"  # red, amber, green
    completion_rate: float = 0.0
    open_defects: int = 0

    class Config:
        from_attributes = True
