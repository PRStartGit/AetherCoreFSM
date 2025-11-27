from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class OrganizationModuleAddon(Base):
    """Organization Module Addon - tracks purchased module add-ons for organizations."""
    __tablename__ = "organization_module_addons"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign Keys
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)

    # Stripe subscription item ID (for managing the add-on subscription)
    stripe_subscription_item_id = Column(String, nullable=True)

    # Status
    is_active = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    organization = relationship("Organization", back_populates="module_addons")
    module = relationship("Module", back_populates="organization_addons")

    def __repr__(self):
        return f"<OrganizationModuleAddon org={self.organization_id} module={self.module_id}>"
