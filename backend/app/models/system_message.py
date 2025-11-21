from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class VisibilityScope(str, enum.Enum):
    ORG_ADMINS_ONLY = "org_admins_only"
    SITE_USERS_ONLY = "site_users_only"
    BOTH = "both"
    ORGANIZATION = "organization"  # Org admin message to their org


class SystemMessage(Base):
    """System message model for broadcast messages."""
    __tablename__ = "system_messages"

    id = Column(Integer, primary_key=True, index=True)
    message_content = Column(Text, nullable=False)
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)  # Null = global/super admin
    visibility_scope = Column(String, nullable=False, default=VisibilityScope.BOTH.value)
    expiry_date = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    created_by = relationship("User", foreign_keys=[created_by_user_id])
    organization = relationship("Organization", foreign_keys=[organization_id])
    dismissals = relationship("MessageDismissal", back_populates="message", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<SystemMessage {self.id} by user {self.created_by_user_id}>"


class MessageDismissal(Base):
    """Tracks which users have dismissed which messages."""
    __tablename__ = "message_dismissals"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("system_messages.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    dismissed_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    message = relationship("SystemMessage", back_populates="dismissals")
    user = relationship("User")

    def __repr__(self):
        return f"<MessageDismissal message={self.message_id} user={self.user_id}>"
