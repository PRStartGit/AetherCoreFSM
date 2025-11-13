from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User, UserRole
from app.models.checklist import Checklist, ChecklistStatus
from app.models.checklist_item import ChecklistItem
from app.schemas.checklist import (
    ChecklistCreate, ChecklistUpdate, ChecklistResponse,
    ChecklistWithItems, ChecklistItemUpdate
)

router = APIRouter()


@router.post("/checklists", response_model=ChecklistResponse, status_code=status.HTTP_201_CREATED)
def create_checklist(
    checklist_data: ChecklistCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new checklist instance."""
    # Check if checklist already exists for this date/category/site
    existing = db.query(Checklist).filter(
        Checklist.checklist_date == checklist_data.checklist_date,
        Checklist.category_id == checklist_data.category_id,
        Checklist.site_id == checklist_data.site_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Checklist already exists for this date, category, and site"
        )

    new_checklist = Checklist(
        checklist_date=checklist_data.checklist_date,
        category_id=checklist_data.category_id,
        site_id=checklist_data.site_id,
        status=ChecklistStatus.PENDING
    )

    db.add(new_checklist)
    db.commit()
    db.refresh(new_checklist)

    return new_checklist


@router.get("/checklists", response_model=List[ChecklistResponse])
def list_checklists(
    site_id: int = None,
    status_filter: ChecklistStatus = None,
    start_date: date = None,
    end_date: date = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List checklists with filters."""
    query = db.query(Checklist)

    # Filter by site
    if site_id:
        query = query.filter(Checklist.site_id == site_id)

    # Filter by status
    if status_filter:
        query = query.filter(Checklist.status == status_filter)

    # Filter by date range
    if start_date:
        query = query.filter(Checklist.checklist_date >= start_date)
    if end_date:
        query = query.filter(Checklist.checklist_date <= end_date)

    # Filter by organization (non-super-admins)
    if current_user.role != UserRole.SUPER_ADMIN:
        from app.models.site import Site
        query = query.join(Site).filter(Site.organization_id == current_user.organization_id)

    checklists = query.order_by(Checklist.checklist_date.desc()).offset(skip).limit(limit).all()
    return checklists


@router.get("/checklists/{checklist_id}", response_model=ChecklistWithItems)
def get_checklist(
    checklist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get checklist by ID with all items."""
    checklist = db.query(Checklist).filter(Checklist.id == checklist_id).first()

    if not checklist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Checklist not found"
        )

    # Check permissions
    if current_user.role != UserRole.SUPER_ADMIN:
        if current_user.organization_id != checklist.site.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

    # Get all items
    items = []
    for item in checklist.items:
        items.append({
            "id": item.id,
            "item_name": item.item_name,
            "is_completed": item.is_completed,
            "notes": item.notes,
            "item_data": item.item_data,
            "photo_url": item.photo_url,
            "task_id": item.task_id,
            "completed_at": item.completed_at
        })

    checklist_dict = {
        **checklist.__dict__,
        "items": items
    }

    return checklist_dict


@router.put("/checklists/{checklist_id}", response_model=ChecklistResponse)
def update_checklist(
    checklist_id: int,
    checklist_data: ChecklistUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update checklist status."""
    checklist = db.query(Checklist).filter(Checklist.id == checklist_id).first()

    if not checklist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Checklist not found"
        )

    # Update fields
    update_data = checklist_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(checklist, field, value)

    # Recalculate completion
    checklist.calculate_completion()

    db.commit()
    db.refresh(checklist)

    return checklist


@router.put("/checklists/{checklist_id}/items/{item_id}", response_model=dict)
def update_checklist_item(
    checklist_id: int,
    item_id: int,
    item_data: ChecklistItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a checklist item."""
    checklist_item = db.query(ChecklistItem).filter(
        ChecklistItem.id == item_id,
        ChecklistItem.checklist_id == checklist_id
    ).first()

    if not checklist_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Checklist item not found"
        )

    # Update item
    checklist_item.is_completed = item_data.is_completed
    checklist_item.notes = item_data.notes
    checklist_item.item_data = item_data.item_data
    checklist_item.photo_url = item_data.photo_url

    if item_data.is_completed:
        from datetime import datetime
        checklist_item.completed_at = datetime.utcnow()

    # Update checklist completion stats
    checklist = checklist_item.checklist
    checklist.completed_items = sum(1 for item in checklist.items if item.is_completed)
    checklist.calculate_completion()

    # Update checklist status
    if checklist.completion_percentage == 100:
        checklist.status = ChecklistStatus.COMPLETED
        checklist.completed_at = datetime.utcnow()
        checklist.completed_by_id = current_user.id
    elif checklist.completion_percentage > 0:
        checklist.status = ChecklistStatus.IN_PROGRESS

    db.commit()

    return {"message": "Checklist item updated successfully"}


@router.delete("/checklists/{checklist_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_checklist(
    checklist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete checklist."""
    checklist = db.query(Checklist).filter(Checklist.id == checklist_id).first()

    if not checklist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Checklist not found"
        )

    db.delete(checklist)
    db.commit()

    return None
