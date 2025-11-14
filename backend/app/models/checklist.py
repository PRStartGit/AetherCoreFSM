from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Date, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class ChecklistStatus(str, enum.Enum):
    """Checklist status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    OVERDUE = "overdue"


class Checklist(Base):
    """Checklist model - represents a specific instance of a category for a date."""
    __tablename__ = "checklists"

    id = Column(Integer, primary_key=True, index=True)
    checklist_date = Column(Date, nullable=False)  # The date this checklist is for
    status = Column(SQLEnum(ChecklistStatus), default=ChecklistStatus.PENDING)

    # Foreign Keys
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False)
    completed_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Completion tracking
    total_items = Column(Integer, default=0)
    completed_items = Column(Integer, default=0)
    completion_percentage = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    category = relationship("Category")
    site = relationship("Site", back_populates="checklists")
    completed_by = relationship("User", back_populates="created_checklists", foreign_keys=[completed_by_id])
    items = relationship("ChecklistItem", back_populates="checklist", cascade="all, delete-orphan")

    def calculate_completion(self):
        """Calculate completion percentage."""
        if self.total_items > 0:
            self.completion_percentage = int((self.completed_items / self.total_items) * 100)
        else:
            self.completion_percentage = 0

    def __repr__(self):
        return f"<Checklist {self.checklist_date} - Site: {self.site.name} ({self.status})>"
