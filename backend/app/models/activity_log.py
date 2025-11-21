from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class LogType(str, enum.Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    REGISTRATION = "registration"
    ORG_REGISTRATION = "org_registration"
    TASK_COMPLETED = "task_completed"
    CHECKLIST_COMPLETED = "checklist_completed"
    ERROR = "error"
    DEFECT_CREATED = "defect_created"
    DEFECT_RESOLVED = "defect_resolved"


class ActivityLog(Base):
    """Activity log for tracking user actions and system events."""
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    log_type = Column(String, nullable=False, index=True)
    message = Column(Text, nullable=False)
    details = Column(Text, nullable=True)  # JSON string for extra data

    # User who performed the action (nullable for system events)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    user_email = Column(String, nullable=True)  # Store email in case user is deleted

    # Organization context (nullable for super admin actions)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="SET NULL"), nullable=True)
    organization_name = Column(String, nullable=True)

    # IP and user agent for security tracking
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)

    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationships
    user = relationship("User", backref="activity_logs")
    organization = relationship("Organization", backref="activity_logs")

    def __repr__(self):
        return f"<ActivityLog {self.log_type}: {self.message[:50]}>"
