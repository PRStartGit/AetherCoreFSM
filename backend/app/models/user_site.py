from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class UserSite(Base):
    """Association table for User-Site many-to-many relationship."""
    __tablename__ = "user_sites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="user_sites")
    site = relationship("Site", back_populates="user_sites")

    def __repr__(self):
        return f"<UserSite user_id={self.user_id} site_id={self.site_id}>"
