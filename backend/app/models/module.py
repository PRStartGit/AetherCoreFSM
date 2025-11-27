from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Module(Base):
    """Module definition - defines available modules in the system."""
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Display name e.g., "Recipe Book"
    code = Column(String, unique=True, nullable=False, index=True)  # e.g., "recipes", "training"
    description = Column(Text, nullable=True)
    icon = Column(String, nullable=True)  # Icon class for UI

    # Core modules are always included in all packages
    is_core = Column(Boolean, default=False)

    # Add-on pricing (nullable - if both null, module can't be purchased as add-on)
    addon_price_per_site = Column(Float, nullable=True)  # e.g., 2.00 for recipes
    addon_price_per_org = Column(Float, nullable=True)   # e.g., 5.00 for training (flat rate)

    # Stripe price ID for add-on billing
    stripe_addon_price_id = Column(String, nullable=True)

    # Status
    is_active = Column(Boolean, default=True)
    display_order = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    package_modules = relationship("PackageModule", back_populates="module", cascade="all, delete-orphan")
    organization_addons = relationship("OrganizationModuleAddon", back_populates="module", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Module {self.name} ({self.code})>"
