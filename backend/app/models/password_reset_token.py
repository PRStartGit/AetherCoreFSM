from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from datetime import datetime, timedelta


class PasswordResetToken(Base):
    """Password reset token model for handling password resets."""
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    used = Column(Integer, default=0)  # SQLite uses 0/1 for boolean

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User")

    def is_valid(self):
        """Check if token is still valid (not expired and not used)."""
        return not self.used and datetime.utcnow() < self.expires_at

    def __repr__(self):
        return f"<PasswordResetToken {self.token[:8]}... for user_id={self.user_id}>"
