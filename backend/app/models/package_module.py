from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class PackageModule(Base):
    """Package-Module relationship - defines which modules are included in each package."""
    __tablename__ = "package_modules"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign Keys
    package_id = Column(Integer, ForeignKey("subscription_packages.id"), nullable=False)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)

    # Is this module included by default in this package?
    is_included = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    package = relationship("SubscriptionPackage", back_populates="package_modules")
    module = relationship("Module", back_populates="package_modules")

    def __repr__(self):
        return f"<PackageModule package={self.package_id} module={self.module_id}>"
