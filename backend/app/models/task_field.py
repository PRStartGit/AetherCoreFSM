from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class TaskField(Base):
    """TaskField model - configurable fields for dynamic task forms."""
    __tablename__ = "task_fields"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, index=True)

    # Field configuration
    field_type = Column(String(50), nullable=False)  # number, text, temperature, yes_no, dropdown, photo, repeating_group
    field_label = Column(String(255), nullable=False)
    field_order = Column(Integer, nullable=False)  # For ordering fields in the form
    is_required = Column(Boolean, default=True)

    # JSON configuration
    validation_rules = Column(JSON, nullable=True)  # e.g., {"min": 0, "max": 10, "create_defect_if": "out_of_range"}
    options = Column(JSON, nullable=True)  # e.g., for dropdown: ["Option 1", "Option 2"]
    show_if = Column(JSON, nullable=True)  # Conditional logic: {"field_id": 123, "value": "yes"}

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    task = relationship("Task", back_populates="task_fields")
    responses = relationship("TaskFieldResponse", back_populates="task_field", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<TaskField {self.field_label} ({self.field_type})>"
