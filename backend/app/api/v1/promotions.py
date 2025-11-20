from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_super_admin
from app.models.promotion import Promotion
from app.models.user import User
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


# Pydantic schemas
class PromotionCreate(BaseModel):
    name: str
    description: str | None = None
    trial_days: int
    is_active: bool = False
    start_date: datetime | None = None
    end_date: datetime | None = None


class PromotionUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    trial_days: int | None = None
    is_active: bool | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None


class PromotionResponse(BaseModel):
    id: int
    name: str
    description: str | None
    trial_days: int
    is_active: bool
    created_at: datetime
    updated_at: datetime | None
    start_date: datetime | None
    end_date: datetime | None

    class Config:
        from_attributes = True


@router.get("/promotions", response_model=List[PromotionResponse])
def list_promotions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """List all promotions (Super Admin only)"""
    promotions = db.query(Promotion).order_by(Promotion.created_at.desc()).all()
    return promotions


@router.get("/promotions/active", response_model=PromotionResponse | None)
def get_active_promotion(
    db: Session = Depends(get_db)
):
    """Get the currently active promotion (Public endpoint)"""
    promotion = db.query(Promotion).filter(Promotion.is_active == True).first()
    return promotion


@router.get("/promotions/{promotion_id}", response_model=PromotionResponse)
def get_promotion(
    promotion_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Get a specific promotion (Super Admin only)"""
    promotion = db.query(Promotion).filter(Promotion.id == promotion_id).first()
    if not promotion:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return promotion


@router.post("/promotions", response_model=PromotionResponse, status_code=status.HTTP_201_CREATED)
def create_promotion(
    promotion_data: PromotionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Create a new promotion (Super Admin only)"""
    
    # If setting this promotion as active, deactivate all others
    if promotion_data.is_active:
        db.query(Promotion).update({"is_active": False})
    
    new_promotion = Promotion(
        name=promotion_data.name,
        description=promotion_data.description,
        trial_days=promotion_data.trial_days,
        is_active=promotion_data.is_active,
        start_date=promotion_data.start_date,
        end_date=promotion_data.end_date
    )
    
    db.add(new_promotion)
    db.commit()
    db.refresh(new_promotion)
    
    return new_promotion


@router.put("/promotions/{promotion_id}", response_model=PromotionResponse)
def update_promotion(
    promotion_id: int,
    promotion_data: PromotionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Update a promotion (Super Admin only)"""
    promotion = db.query(Promotion).filter(Promotion.id == promotion_id).first()
    
    if not promotion:
        raise HTTPException(status_code=404, detail="Promotion not found")
    
    # If setting this promotion as active, deactivate all others
    if promotion_data.is_active:
        db.query(Promotion).filter(Promotion.id != promotion_id).update({"is_active": False})
    
    # Update fields
    update_data = promotion_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(promotion, field, value)
    
    promotion.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(promotion)
    
    return promotion


@router.delete("/promotions/{promotion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_promotion(
    promotion_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Delete a promotion (Super Admin only)"""
    promotion = db.query(Promotion).filter(Promotion.id == promotion_id).first()
    
    if not promotion:
        raise HTTPException(status_code=404, detail="Promotion not found")
    
    # Don't allow deleting the active promotion if it's the only one
    if promotion.is_active:
        other_promotions = db.query(Promotion).filter(Promotion.id != promotion_id).count()
        if other_promotions == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete the only active promotion. Create another promotion first."
            )
    
    db.delete(promotion)
    db.commit()
    
    return None


@router.post("/promotions/{promotion_id}/activate", response_model=PromotionResponse)
def activate_promotion(
    promotion_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Activate a specific promotion (deactivates all others)"""
    promotion = db.query(Promotion).filter(Promotion.id == promotion_id).first()
    
    if not promotion:
        raise HTTPException(status_code=404, detail="Promotion not found")
    
    # Deactivate all promotions
    db.query(Promotion).update({"is_active": False})
    
    # Activate the selected one
    promotion.is_active = True
    promotion.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(promotion)
    
    return promotion
