from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.core.database import get_db
from app.core.dependencies import get_current_super_admin
from app.models.user import User
from app.models.allergen_keyword import AllergenKeyword

router = APIRouter()


class AllergenKeywordResponse(BaseModel):
    id: int
    keyword: str
    allergen: str

    class Config:
        from_attributes = True


class AllergenKeywordCreate(BaseModel):
    keyword: str
    allergen: str


class AllergenKeywordUpdate(BaseModel):
    keyword: str | None = None
    allergen: str | None = None


# UK 14 Allergens for reference
UK_14_ALLERGENS = [
    'Celery', 'Cereals containing gluten', 'Crustaceans', 'Eggs', 'Fish',
    'Lupin', 'Milk', 'Molluscs', 'Mustard', 'Nuts', 'Peanuts',
    'Sesame seeds', 'Soybeans', 'Sulphur dioxide and sulphites'
]


@router.get("/allergens/list", response_model=List[str])
def get_allergen_list():
    """Get the UK 14 allergens list"""
    return UK_14_ALLERGENS


@router.get("", response_model=List[AllergenKeywordResponse])
def get_allergen_keywords(
    allergen: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Get all allergen keywords (Super Admin only)"""
    query = db.query(AllergenKeyword)

    if allergen:
        query = query.filter(AllergenKeyword.allergen == allergen)

    keywords = query.order_by(AllergenKeyword.allergen, AllergenKeyword.keyword).all()
    return keywords


@router.get("/{keyword_id}", response_model=AllergenKeywordResponse)
def get_allergen_keyword(
    keyword_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Get a specific allergen keyword by ID (Super Admin only)"""
    keyword = db.query(AllergenKeyword).filter(AllergenKeyword.id == keyword_id).first()
    if not keyword:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Allergen keyword not found"
        )
    return keyword


@router.post("", response_model=AllergenKeywordResponse, status_code=status.HTTP_201_CREATED)
def create_allergen_keyword(
    keyword_data: AllergenKeywordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Create a new allergen keyword (Super Admin only)"""
    # Check if keyword already exists for this allergen
    existing = db.query(AllergenKeyword).filter(
        AllergenKeyword.keyword == keyword_data.keyword.lower().strip(),
        AllergenKeyword.allergen == keyword_data.allergen
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Keyword '{keyword_data.keyword}' already exists for allergen '{keyword_data.allergen}'"
        )

    new_keyword = AllergenKeyword(
        keyword=keyword_data.keyword.lower().strip(),
        allergen=keyword_data.allergen
    )

    db.add(new_keyword)
    db.commit()
    db.refresh(new_keyword)

    return new_keyword


@router.put("/{keyword_id}", response_model=AllergenKeywordResponse)
def update_allergen_keyword(
    keyword_id: int,
    keyword_data: AllergenKeywordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Update an allergen keyword (Super Admin only)"""
    keyword = db.query(AllergenKeyword).filter(AllergenKeyword.id == keyword_id).first()

    if not keyword:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Allergen keyword not found"
        )

    # Update fields
    if keyword_data.keyword is not None:
        keyword.keyword = keyword_data.keyword.lower().strip()
    if keyword_data.allergen is not None:
        keyword.allergen = keyword_data.allergen

    db.commit()
    db.refresh(keyword)

    return keyword


@router.delete("/{keyword_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_allergen_keyword(
    keyword_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Delete an allergen keyword (Super Admin only)"""
    keyword = db.query(AllergenKeyword).filter(AllergenKeyword.id == keyword_id).first()

    if not keyword:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Allergen keyword not found"
        )

    db.delete(keyword)
    db.commit()

    return None
