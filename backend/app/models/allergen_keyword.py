from sqlalchemy import Column, Integer, String, UniqueConstraint
from app.core.database import Base


class AllergenKeyword(Base):
    """AllergenKeyword model - maps ingredient keywords to allergens for auto-detection."""
    __tablename__ = "allergen_keywords"
    __table_args__ = (
        UniqueConstraint('keyword', 'allergen', name='uq_allergen_keyword'),
    )

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String(100), nullable=False, index=True)
    allergen = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<AllergenKeyword {self.keyword} -> {self.allergen}>"
