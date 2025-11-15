from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Task(Base):
    """Task model - specific task within a category (e.g., 'Fridge Checks AM')."""
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    order_index = Column(Integer, default=0)  # For ordering tasks within a category

    # Dynamic Form Configuration
    # Example: {"type": "dynamic_quantity", "question": "How many fridges?", "item_type": "fridge"}
    form_config = Column(JSON, nullable=True)

    # Dynamic Task Fields (new system)
    has_dynamic_form = Column(Boolean, default=False)

    # Foreign Keys
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    category = relationship("Category", back_populates="tasks")
    site_tasks = relationship("SiteTask", back_populates="task", cascade="all, delete-orphan")
    checklist_items = relationship("ChecklistItem", back_populates="task", cascade="all, delete-orphan")
    task_fields = relationship("TaskField", back_populates="task", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Task {self.name} (Category: {self.category.name})>"
