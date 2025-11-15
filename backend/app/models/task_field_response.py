from sqlalchemy import Column, Integer, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class TaskFieldResponse(Base):
    """TaskFieldResponse model - stores responses to dynamic task fields."""
    __tablename__ = "task_field_responses"

    id = Column(Integer, primary_key=True, index=True)
    checklist_item_id = Column(Integer, ForeignKey("checklist_items.id", ondelete="CASCADE"), nullable=False, index=True)
    task_field_id = Column(Integer, ForeignKey("task_fields.id", ondelete="CASCADE"), nullable=False)

    # Polymorphic response values (only one should be populated based on field_type)
    text_value = Column(Text, nullable=True)
    number_value = Column(Float, nullable=True)
    boolean_value = Column(Boolean, nullable=True)
    json_value = Column(JSON, nullable=True)  # For complex types like repeating groups
    file_url = Column(Text, nullable=True)  # For photo uploads

    # Auto-generated defect (if validation triggers)
    auto_defect_id = Column(Integer, ForeignKey("defects.id"), nullable=True)

    # Timestamps and metadata
    completed_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
    checklist_item = relationship("ChecklistItem", back_populates="field_responses")
    task_field = relationship("TaskField", back_populates="responses")
    auto_defect = relationship("Defect", foreign_keys=[auto_defect_id])
    completed_by_user = relationship("User", foreign_keys=[completed_by])

    def __repr__(self):
        return f"<TaskFieldResponse for field {self.task_field_id}>"

    def get_value(self):
        """Helper method to get the actual value regardless of type."""
        if self.text_value is not None:
            return self.text_value
        elif self.number_value is not None:
            return self.number_value
        elif self.boolean_value is not None:
            return self.boolean_value
        elif self.json_value is not None:
            return self.json_value
        elif self.file_url is not None:
            return self.file_url
        return None
