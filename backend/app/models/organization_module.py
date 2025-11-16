from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class OrganizationModule(Base):
    """OrganizationModule model - tracks which modules are enabled for each organization."""
    __tablename__ = "organization_modules"

    id = Column(Integer, primary_key=True, index=True)
    module_name = Column(String, nullable=False)  # e.g., "monitoring", "audit", "training"
    is_enabled = Column(Boolean, default=False)

    # Foreign Keys
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    organization = relationship("Organization", back_populates="org_modules")

    def __repr__(self):
        return f"<OrganizationModule {self.module_name} (Enabled: {self.is_enabled})>"
