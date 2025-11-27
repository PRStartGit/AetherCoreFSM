from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class SubscriptionPackage(Base):
    """Subscription package - defines pricing tiers based on site count."""
    __tablename__ = "subscription_packages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Display name e.g., "Professional"
    code = Column(String, unique=True, nullable=False, index=True)  # e.g., "professional"
    description = Column(Text, nullable=True)

    # Site limits for this tier
    min_sites = Column(Integer, nullable=False, default=1)
    max_sites = Column(Integer, nullable=True)  # NULL = unlimited

    # Pricing (in GBP)
    monthly_price = Column(Float, nullable=False, default=0.0)
    annual_price = Column(Float, nullable=True)  # If set, offers annual discount

    # Stripe price IDs
    stripe_monthly_price_id = Column(String, nullable=True)
    stripe_annual_price_id = Column(String, nullable=True)

    # Features for landing page display
    features_json = Column(Text, nullable=True)  # JSON array of feature strings

    # Status
    is_active = Column(Boolean, default=True)
    is_popular = Column(Boolean, default=False)  # Highlight on pricing page
    display_order = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    package_modules = relationship("PackageModule", back_populates="package", cascade="all, delete-orphan")
    organizations = relationship("Organization", back_populates="subscription_package")

    def __repr__(self):
        return f"<SubscriptionPackage {self.name} ({self.code})>"
