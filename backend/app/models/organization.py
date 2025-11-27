from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Organization(Base):
    """Organization model - represents a client company."""
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    org_id = Column(String, unique=True, index=True, nullable=False)  # e.g., "vig" for Viva Italia Group
    is_active = Column(Boolean, default=True)

    # Contact Information
    contact_person = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)
    contact_phone = Column(String, nullable=True)
    address = Column(Text, nullable=True)

    # Subscription
    subscription_tier = Column(String, default="basic")  # platform_admin, free, basic, professional, enterprise
    custom_price_per_site = Column(Float, nullable=True)  # Custom pricing if set by super admin
    subscription_start_date = Column(DateTime(timezone=True), nullable=True)
    subscription_end_date = Column(DateTime(timezone=True), nullable=True)
    is_trial = Column(Boolean, default=True)

    # Stripe Integration
    stripe_customer_id = Column(String, nullable=True, index=True)
    stripe_subscription_id = Column(String, nullable=True)

    # Link to subscription package (new tier system)
    package_id = Column(Integer, ForeignKey("subscription_packages.id"), nullable=True)

    # Organization-wide Email Reporting
    org_report_enabled = Column(Boolean, default=False)
    org_report_day = Column(Integer, default=1)  # 1=Monday, 7=Sunday
    org_report_time = Column(String, default="09:00")
    org_report_recipients = Column(Text, nullable=True)  # Comma-separated emails

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    users = relationship("User", back_populates="organization", cascade="all, delete-orphan")
    sites = relationship("Site", back_populates="organization", cascade="all, delete-orphan")
    categories = relationship("Category", back_populates="organization", cascade="all, delete-orphan")
    org_modules = relationship("OrganizationModule", back_populates="organization", cascade="all, delete-orphan")
    subscription_package = relationship("SubscriptionPackage", back_populates="organizations")
    module_addons = relationship("OrganizationModuleAddon", back_populates="organization", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Organization {self.name} ({self.org_id})>"
