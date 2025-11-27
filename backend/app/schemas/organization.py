from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class OrganizationBase(BaseModel):
    """Base organization schema."""
    name: str
    org_id: str  # Unique identifier like "vig"
    contact_person: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    # Billing information
    billing_email: Optional[EmailStr] = None
    billing_address: Optional[str] = None
    company_name: Optional[str] = None
    vat_number: Optional[str] = None


class OrganizationCreate(OrganizationBase):
    """Organization creation schema."""
    subscription_tier: str = "basic"
    custom_price_per_site: Optional[float] = None


class OrganizationUpdate(BaseModel):
    """Organization update schema."""
    name: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    is_active: Optional[bool] = None
    subscription_tier: Optional[str] = None
    custom_price_per_site: Optional[float] = None
    # Billing information
    billing_email: Optional[EmailStr] = None
    billing_address: Optional[str] = None
    company_name: Optional[str] = None
    vat_number: Optional[str] = None
    # Organization-wide email reporting
    org_report_enabled: Optional[bool] = None
    org_report_day: Optional[int] = None
    org_report_time: Optional[str] = None
    org_report_recipients: Optional[str] = None


class OrganizationResponse(OrganizationBase):
    """Organization response schema."""
    id: int
    is_active: bool
    subscription_tier: str
    custom_price_per_site: Optional[float] = None
    subscription_start_date: Optional[datetime] = None
    subscription_end_date: Optional[datetime] = None
    is_trial: bool
    # Organization-wide email reporting
    org_report_enabled: bool = False
    org_report_day: int = 1
    org_report_time: str = "09:00"
    org_report_recipients: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class OrganizationWithStats(OrganizationResponse):
    """Organization with statistics."""
    total_sites: int = 0
    total_users: int = 0
    active_modules: list[str] = []

    class Config:
        from_attributes = True
