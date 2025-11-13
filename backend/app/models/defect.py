from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class DefectSeverity(str, enum.Enum):
    """Defect severity enumeration."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class DefectStatus(str, enum.Enum):
    """Defect status enumeration."""
    OPEN = "open"
    CLOSED = "closed"


class Defect(Base):
    """Defect model - represents an issue or non-compliance."""
    __tablename__ = "defects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(SQLEnum(DefectSeverity), nullable=False, default=DefectSeverity.MEDIUM)
    status = Column(SQLEnum(DefectStatus), default=DefectStatus.OPEN)

    # Photo evidence
    photo_url = Column(String, nullable=True)

    # Foreign Keys
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False)
    checklist_item_id = Column(Integer, ForeignKey("checklist_items.id"), nullable=True)
    reported_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    closed_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    closed_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    site = relationship("Site", back_populates="defects")
    checklist_item = relationship("ChecklistItem", back_populates="defects")
    reported_by = relationship("User", foreign_keys=[reported_by_id])
    closed_by = relationship("User", foreign_keys=[closed_by_id])

    def __repr__(self):
        return f"<Defect {self.title} ({self.severity} - {self.status})>"
