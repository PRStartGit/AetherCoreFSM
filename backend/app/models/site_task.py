from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class SiteTask(Base):
    """Association table for Site-Task relationship - assigns tasks to specific sites."""
    __tablename__ = "site_tasks"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    site = relationship("Site", back_populates="site_tasks")
    task = relationship("Task", back_populates="site_tasks")

    def __repr__(self):
        return f"<SiteTask site_id={self.site_id} task_id={self.task_id}>"
