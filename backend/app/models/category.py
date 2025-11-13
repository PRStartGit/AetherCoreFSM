from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum as SQLEnum, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class ChecklistFrequency(str, enum.Enum):
    """Checklist frequency enumeration."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    SIX_MONTHLY = "six_monthly"
    YEARLY = "yearly"


class Category(Base):
    """Category model - groups related tasks (e.g., 'Restaurant Opening')."""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    # Scheduling
    frequency = Column(SQLEnum(ChecklistFrequency), nullable=False, default=ChecklistFrequency.DAILY)
    closes_at = Column(Time, nullable=True)  # e.g., 13:00 for "Morning Checks"

    # Scope: Global (super admin) or Organization-specific
    is_global = Column(Boolean, default=False)  # True if created by super admin
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    organization = relationship("Organization", back_populates="categories")
    tasks = relationship("Task", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Category {self.name} ({self.frequency})>"
