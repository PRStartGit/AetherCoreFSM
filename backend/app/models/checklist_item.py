from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class ChecklistItem(Base):
    """ChecklistItem model - individual item within a checklist."""
    __tablename__ = "checklist_items"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, nullable=False)  # e.g., "Fridge 1 Temperature"
    is_completed = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)

    # Dynamic data - stores user input (e.g., temperature values)
    # Example: {"temperature": "4.5", "unit": "celsius"}
    item_data = Column(JSON, nullable=True)

    # Photo evidence
    photo_url = Column(String, nullable=True)

    # Foreign Keys
    checklist_id = Column(Integer, ForeignKey("checklists.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    checklist = relationship("Checklist", back_populates="items")
    task = relationship("Task", back_populates="checklist_items")
    defects = relationship("Defect", back_populates="checklist_item", cascade="all, delete-orphan")
    field_responses = relationship("TaskFieldResponse", back_populates="checklist_item", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ChecklistItem {self.item_name} (Completed: {self.is_completed})>"
