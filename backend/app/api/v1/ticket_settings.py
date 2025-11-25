"""
Ticket Settings API endpoints
Manage ticket categories and system settings
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from app.db.session import get_db
from app.db.base import Base
from app.core.auth import get_current_user
from app.models.user import User, UserRole

router = APIRouter()


# Model for ticket categories (stored in DB)
class TicketCategory(Base):
    __tablename__ = "ticket_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


# Model for ticket settings (stored in DB)
class TicketSettings(Base):
    __tablename__ = "ticket_settings"

    id = Column(Integer, primary_key=True, index=True)
    setting_key = Column(String(100), unique=True, nullable=False)
    setting_value = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Pydantic schemas
class TicketCategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True
    sort_order: int = 0


class TicketCategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None


class TicketCategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    is_active: bool
    sort_order: int
    created_at: datetime

    class Config:
        from_attributes = True


class TicketSettingsResponse(BaseModel):
    ticketing_enabled: bool
    auto_assign_enabled: bool
    email_notifications_enabled: bool
    default_priority: str
    sla_response_hours: int


class TicketSettingsUpdate(BaseModel):
    ticketing_enabled: Optional[bool] = None
    auto_assign_enabled: Optional[bool] = None
    email_notifications_enabled: Optional[bool] = None
    default_priority: Optional[str] = None
    sla_response_hours: Optional[int] = None


def require_super_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(status_code=403, detail="Super admin access required")
    return current_user


# Default settings
DEFAULT_SETTINGS = {
    "ticketing_enabled": "true",
    "auto_assign_enabled": "false",
    "email_notifications_enabled": "true",
    "default_priority": "medium",
    "sla_response_hours": "24"
}


def get_setting(db: Session, key: str) -> str:
    setting = db.query(TicketSettings).filter(TicketSettings.setting_key == key).first()
    if setting:
        return setting.setting_value
    return DEFAULT_SETTINGS.get(key, "")


def set_setting(db: Session, key: str, value: str):
    setting = db.query(TicketSettings).filter(TicketSettings.setting_key == key).first()
    if setting:
        setting.setting_value = value
        setting.updated_at = datetime.utcnow()
    else:
        setting = TicketSettings(setting_key=key, setting_value=value)
        db.add(setting)
    db.commit()


# Category endpoints
@router.get("/categories", response_model=List[TicketCategoryResponse])
def list_categories(
    include_inactive: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all ticket categories"""
    query = db.query(TicketCategory)
    if not include_inactive:
        query = query.filter(TicketCategory.is_active == True)
    return query.order_by(TicketCategory.sort_order).all()


@router.post("/categories", response_model=TicketCategoryResponse)
def create_category(
    category_data: TicketCategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_admin)
):
    """Create a new ticket category"""
    category = TicketCategory(
        name=category_data.name,
        description=category_data.description,
        is_active=category_data.is_active,
        sort_order=category_data.sort_order
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.patch("/categories/{category_id}", response_model=TicketCategoryResponse)
def update_category(
    category_id: int,
    category_data: TicketCategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_admin)
):
    """Update a ticket category"""
    category = db.query(TicketCategory).filter(TicketCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    if category_data.name is not None:
        category.name = category_data.name
    if category_data.description is not None:
        category.description = category_data.description
    if category_data.is_active is not None:
        category.is_active = category_data.is_active
    if category_data.sort_order is not None:
        category.sort_order = category_data.sort_order

    db.commit()
    db.refresh(category)
    return category


@router.delete("/categories/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_admin)
):
    """Delete a ticket category (soft delete by setting inactive)"""
    category = db.query(TicketCategory).filter(TicketCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    category.is_active = False
    db.commit()
    return {"message": "Category deactivated"}


# Settings endpoints
@router.get("/settings", response_model=TicketSettingsResponse)
def get_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_admin)
):
    """Get ticket system settings"""
    return TicketSettingsResponse(
        ticketing_enabled=get_setting(db, "ticketing_enabled") == "true",
        auto_assign_enabled=get_setting(db, "auto_assign_enabled") == "true",
        email_notifications_enabled=get_setting(db, "email_notifications_enabled") == "true",
        default_priority=get_setting(db, "default_priority"),
        sla_response_hours=int(get_setting(db, "sla_response_hours") or "24")
    )


@router.patch("/settings", response_model=TicketSettingsResponse)
def update_settings(
    settings_data: TicketSettingsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_admin)
):
    """Update ticket system settings"""
    if settings_data.ticketing_enabled is not None:
        set_setting(db, "ticketing_enabled", str(settings_data.ticketing_enabled).lower())
    if settings_data.auto_assign_enabled is not None:
        set_setting(db, "auto_assign_enabled", str(settings_data.auto_assign_enabled).lower())
    if settings_data.email_notifications_enabled is not None:
        set_setting(db, "email_notifications_enabled", str(settings_data.email_notifications_enabled).lower())
    if settings_data.default_priority is not None:
        set_setting(db, "default_priority", settings_data.default_priority)
    if settings_data.sla_response_hours is not None:
        set_setting(db, "sla_response_hours", str(settings_data.sla_response_hours))

    return TicketSettingsResponse(
        ticketing_enabled=get_setting(db, "ticketing_enabled") == "true",
        auto_assign_enabled=get_setting(db, "auto_assign_enabled") == "true",
        email_notifications_enabled=get_setting(db, "email_notifications_enabled") == "true",
        default_priority=get_setting(db, "default_priority"),
        sla_response_hours=int(get_setting(db, "sla_response_hours") or "24")
    )
