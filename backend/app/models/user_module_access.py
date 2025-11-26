from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class UserModuleAccess(Base):
    """UserModuleAccess model - tracks which modules each user has access to."""
    __tablename__ = "user_module_access"
    __table_args__ = (
        UniqueConstraint('user_id', 'module_name', name='uq_user_module'),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    module_name = Column(String(50), nullable=False, index=True)
    granted_at = Column(DateTime(timezone=True), server_default=func.now())
    granted_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="module_access")
    granted_by = relationship("User", foreign_keys=[granted_by_user_id])

    def __repr__(self):
        return f"<UserModuleAccess user_id={self.user_id} module={self.module_name}>"
