from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base


class Promotion(Base):
    """Promotion model - represents special offers and trial periods."""
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # e.g., "Black Friday 2025"
    description = Column(Text, nullable=True)
    
    # Trial period settings
    trial_days = Column(Integer, nullable=False, default=30)  # Duration in days
    
    # Active status
    is_active = Column(Boolean, default=False)  # Only one promotion can be active at a time
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Optional: Start and end dates for the promotion
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<Promotion {self.name} - {self.trial_days} days>"
