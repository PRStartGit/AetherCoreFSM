from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Site(Base):
    """Site model - represents a physical location within an organization."""
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    site_code = Column(String, nullable=True)  # e.g., "VIG-001"
    is_active = Column(Boolean, default=True)

    # Address
    address = Column(Text, nullable=True)
    city = Column(String, nullable=True)
    postcode = Column(String, nullable=True)
    country = Column(String, default="UK")

    # Foreign Keys
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)

    # Email Reporting Configuration
    daily_report_enabled = Column(Boolean, default=False)
    daily_report_time = Column(String, default="09:00")  # Time in HH:MM format
    weekly_report_enabled = Column(Boolean, default=False)
    weekly_report_day = Column(Integer, default=1)  # 1=Monday, 7=Sunday
    weekly_report_time = Column(String, default="09:00")
    report_recipients = Column(Text, nullable=True)  # Comma-separated emails

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    organization = relationship("Organization", back_populates="sites")
    user_sites = relationship("UserSite", back_populates="site", cascade="all, delete-orphan")
    site_tasks = relationship("SiteTask", back_populates="site", cascade="all, delete-orphan")
    checklists = relationship("Checklist", back_populates="site", cascade="all, delete-orphan")
    defects = relationship("Defect", back_populates="site", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Site {self.name} ({self.organization.name})>"
