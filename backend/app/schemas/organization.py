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


class OrganizationResponse(OrganizationBase):
    """Organization response schema."""
    id: int
    is_active: bool
    subscription_tier: str
    custom_price_per_site: Optional[float] = None
    subscription_start_date: Optional[datetime] = None
    subscription_end_date: Optional[datetime] = None
    is_trial: bool
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
