from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class BlogPost(Base):
    """Blog post model for news articles."""
    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True, index=True)
    excerpt = Column(Text, nullable=True)  # Short summary for cards/listings
    content = Column(Text, nullable=False)  # HTML content
    thumbnail_url = Column(String(500), nullable=True)  # Image URL for thumbnail
    is_published = Column(Boolean, default=False)
    published_at = Column(DateTime(timezone=True), nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    created_by = relationship("User", foreign_keys=[created_by_id])

    def __repr__(self):
        return f"<BlogPost {self.id}: {self.title}>"
