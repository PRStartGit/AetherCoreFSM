from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


# Junction table for recipe book to site (many-to-many)
recipe_book_sites = Table(
    'recipe_book_sites',
    Base.metadata,
    Column('recipe_book_id', Integer, ForeignKey('recipe_books.id', ondelete='CASCADE'), primary_key=True),
    Column('site_id', Integer, ForeignKey('sites.id', ondelete='CASCADE'), primary_key=True)
)


class RecipeBook(Base):
    """Recipe Book model - collections of recipes for organizations or sites."""
    __tablename__ = "recipe_books"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    site_id = Column(Integer, ForeignKey("sites.id", ondelete="CASCADE"), nullable=True, index=True)  # Deprecated - use sites relationship
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    organization = relationship("Organization")
    site = relationship("Site", foreign_keys=[site_id])  # Legacy single site
    sites = relationship("Site", secondary=recipe_book_sites, backref="recipe_books")  # Multiple sites
    created_by = relationship("User")
    recipe_assignments = relationship("RecipeBookRecipe", back_populates="recipe_book", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<RecipeBook {self.title}>"


class RecipeBookRecipe(Base):
    """Junction table for recipe books and recipes (many-to-many)."""
    __tablename__ = "recipe_book_recipes"

    id = Column(Integer, primary_key=True, index=True)
    recipe_book_id = Column(Integer, ForeignKey("recipe_books.id", ondelete="CASCADE"), nullable=False, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False, index=True)
    order_index = Column(Integer, default=0, nullable=True)
    added_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    recipe_book = relationship("RecipeBook", back_populates="recipe_assignments")
    recipe = relationship("Recipe", back_populates="book_assignments")

    def __repr__(self):
        return f"<RecipeBookRecipe book_id={self.recipe_book_id} recipe_id={self.recipe_id}>"
