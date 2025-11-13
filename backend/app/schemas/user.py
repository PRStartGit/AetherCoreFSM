from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.user import UserRole


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    first_name: str
    last_name: str
    role: UserRole
    phone: Optional[str] = None
    is_active: bool = True


class UserCreate(UserBase):
    """User creation schema."""
    password: str
    organization_id: Optional[int] = None


class UserUpdate(BaseModel):
    """User update schema."""
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[UserRole] = None


class UserResponse(UserBase):
    """User response schema."""
    id: int
    organization_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserWithSites(UserResponse):
    """User response with associated sites."""
    site_ids: list[int] = []

    class Config:
        from_attributes = True
