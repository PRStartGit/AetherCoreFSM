from sqlalchemy import Column, Integer, String
from app.core.database import Base


class IngredientUnit(Base):
    """IngredientUnit model - predefined units for ingredients."""
    __tablename__ = "ingredient_units"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    display_name = Column(String(50), nullable=False)
    category = Column(String(50), nullable=True)  # weight, volume, count, other
    sort_order = Column(Integer, default=0, nullable=False)

    def __repr__(self):
        return f"<IngredientUnit {self.name} ({self.display_name})>"
