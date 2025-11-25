"""
Ticket model for support ticket system
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base


class TicketStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TicketType(str, enum.Enum):
    TECHNICAL = "technical"
    BILLING = "billing"
    GENERAL = "general"
    FEATURE_REQUEST = "feature_request"


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(String(20), unique=True, index=True, nullable=False)
    subject = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)

    status = Column(SQLEnum(TicketStatus, values_callable=lambda x: [e.value for e in x]), default=TicketStatus.OPEN, nullable=False)
    priority = Column(SQLEnum(TicketPriority, values_callable=lambda x: [e.value for e in x]), default=TicketPriority.MEDIUM, nullable=False)
    ticket_type = Column(SQLEnum(TicketType, values_callable=lambda x: [e.value for e in x]), default=TicketType.GENERAL, nullable=False)

    # User who created the ticket
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_by_user = relationship("User", foreign_keys=[created_by_user_id], backref="tickets_created")

    # Organization of the user (for filtering)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    organization = relationship("Organization", backref="tickets")

    # Support agent assigned to the ticket
    assigned_to_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    assigned_to_user = relationship("User", foreign_keys=[assigned_to_user_id], backref="tickets_assigned")

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    closed_at = Column(DateTime, nullable=True)

    # Relationships
    messages = relationship("TicketMessage", back_populates="ticket", cascade="all, delete-orphan", order_by="TicketMessage.created_at")


class TicketMessage(Base):
    __tablename__ = "ticket_messages"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False)
    ticket = relationship("Ticket", back_populates="messages")

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", backref="ticket_messages")

    message = Column(Text, nullable=False)
    is_internal_note = Column(Integer, default=0)  # 1 = internal note (only visible to support)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
