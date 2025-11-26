from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base


class RecipeAllergen(Base):
    """RecipeAllergen model - stores detected allergens for recipes."""
    __tablename__ = "recipe_allergens"
    __table_args__ = (
        UniqueConstraint('recipe_id', 'allergen', name='uq_recipe_allergen'),
    )

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False, index=True)
    allergen = Column(String(100), nullable=False)

    # Relationships
    recipe = relationship("Recipe", back_populates="allergens")

    def __repr__(self):
        return f"<RecipeAllergen recipe_id={self.recipe_id} allergen={self.allergen}>"
