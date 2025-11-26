from pydantic import BaseModel


class AllergenKeywordResponse(BaseModel):
    """Response schema for AllergenKeyword"""
    id: int
    keyword: str
    allergen: str

    class Config:
        from_attributes = True


class RecipeAllergenResponse(BaseModel):
    """Response schema for RecipeAllergen"""
    id: int
    recipe_id: int
    allergen: str

    class Config:
        from_attributes = True
