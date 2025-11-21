from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import date, timedelta
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User, UserRole
from app.api.v1.activity_logs import log_activity
from app.models.activity_log import LogType
from app.models.checklist import Checklist, ChecklistStatus
from app.models.checklist_item import ChecklistItem
from app.schemas.checklist import (
    ChecklistCreate, ChecklistUpdate, ChecklistResponse,
    ChecklistWithItems, ChecklistItemUpdate
)
from pydantic import BaseModel

router = APIRouter()


# Schema for bulk generation
class BulkGenerateRequest(BaseModel):
    start_date: date
    end_date: Optional[date] = None
    site_ids: Optional[List[int]] = None
    category_ids: Optional[List[int]] = None


@router.post("/checklists", response_model=ChecklistResponse, status_code=status.HTTP_201_CREATED)
def create_checklist(
    checklist_data: ChecklistCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new checklist instance with automatically populated items."""
    from app.models.task import Task

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

    # Create the checklist
    new_checklist = Checklist(
        checklist_date=checklist_data.checklist_date,
        category_id=checklist_data.category_id,
        site_id=checklist_data.site_id,
        status=ChecklistStatus.PENDING
    )

    db.add(new_checklist)
    db.flush()  # Get checklist ID without committing

    # Query all active tasks for this category, ordered by order_index
    tasks = db.query(Task).filter(
        Task.category_id == checklist_data.category_id,
        Task.is_active == True
    ).order_by(Task.order_index).all()

    # Create checklist items for each task
    for task in tasks:
        checklist_item = ChecklistItem(
            checklist_id=new_checklist.id,
            task_id=task.id,
            item_name=task.name,
            is_completed=False
        )
        db.add(checklist_item)

    # Set total_items count
    new_checklist.total_items = len(tasks)
    new_checklist.completed_items = 0

    db.commit()
    db.refresh(new_checklist)

    return new_checklist


@router.post("/checklists/generate-bulk", status_code=status.HTTP_201_CREATED)
def generate_checklists_bulk(
    request: BulkGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Generate checklists in bulk for multiple dates, sites, and categories.
    Useful for initial population or testing. Only admins can use this endpoint.
    """
    from app.models.task import Task
    from app.models.category import Category
    from app.models.site import Site

    # Only admins can generate checklists in bulk
    if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.ORG_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can generate checklists in bulk"
        )

    # Set end_date to start_date if not provided (single day)
    end_date = request.end_date or request.start_date

    # Validate date range
    if end_date < request.start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="end_date must be after or equal to start_date"
        )

    # Get sites
    if request.site_ids:
        sites = db.query(Site).filter(Site.id.in_(request.site_ids)).all()
        if current_user.role == UserRole.ORG_ADMIN:
            # Org admins can only generate for their org's sites
            sites = [s for s in sites if s.organization_id == current_user.organization_id]
    else:
        if current_user.role == UserRole.SUPER_ADMIN:
            sites = db.query(Site).all()
        else:
            # Org admins get all sites in their organization
            sites = db.query(Site).filter(Site.organization_id == current_user.organization_id).all()

    # Get categories
    if request.category_ids:
        categories = db.query(Category).filter(
            Category.id.in_(request.category_ids),
            Category.is_active == True
        ).all()
    else:
        # Get all active categories (global + org-specific)
        if current_user.role == UserRole.SUPER_ADMIN:
            categories = db.query(Category).filter(Category.is_active == True).all()
        else:
            categories = db.query(Category).filter(
                (Category.is_global == True) | (Category.organization_id == current_user.organization_id),
                Category.is_active == True
            ).all()

    # Generate checklists
    created_count = 0
    skipped_count = 0
    current_date = request.start_date

    while current_date <= end_date:
        for site in sites:
            for category in categories:
                # Check if checklist already exists
                existing = db.query(Checklist).filter(
                    Checklist.checklist_date == current_date,
                    Checklist.category_id == category.id,
                    Checklist.site_id == site.id
                ).first()

                if existing:
                    skipped_count += 1
                    continue

                # Create checklist
                new_checklist = Checklist(
                    checklist_date=current_date,
                    category_id=category.id,
                    site_id=site.id,
                    status=ChecklistStatus.PENDING
                )
                db.add(new_checklist)
                db.flush()

                # Get tasks for this category
                tasks = db.query(Task).filter(
                    Task.category_id == category.id,
                    Task.is_active == True
                ).order_by(Task.order_index).all()

                # Create checklist items
                for task in tasks:
                    checklist_item = ChecklistItem(
                        checklist_id=new_checklist.id,
                        task_id=task.id,
                        item_name=task.name,
                        is_completed=False
                    )
                    db.add(checklist_item)

                # Set totals
                new_checklist.total_items = len(tasks)
                new_checklist.completed_items = 0

                created_count += 1

        # Move to next day
        current_date += timedelta(days=1)

    db.commit()

    return {
        "message": "Checklists generated successfully",
        "created": created_count,
        "skipped": skipped_count,
        "date_range": f"{request.start_date} to {end_date}",
        "sites_count": len(sites),
        "categories_count": len(categories)
    }


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
    from app.models.category import Category

    query = db.query(Checklist).options(joinedload(Checklist.category))

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

    # Filter by organization and user sites
    if current_user.role == UserRole.SUPER_ADMIN:
        # Super admins see all checklists
        pass
    elif current_user.role == UserRole.ORG_ADMIN:
        # Org admins see all checklists in their organization
        from app.models.site import Site
        query = query.join(Site).filter(Site.organization_id == current_user.organization_id)
    elif current_user.role == UserRole.SITE_USER:
        # Site users only see checklists for their assigned sites
        from app.models.user_site import UserSite
        assigned_site_ids = [us.site_id for us in current_user.user_sites]
        if not assigned_site_ids:
            # Return empty list if user has no assigned sites
            return []
        query = query.filter(Checklist.site_id.in_(assigned_site_ids))

    checklists = query.order_by(Checklist.checklist_date.desc()).offset(skip).limit(limit).all()

    # Manually build response to handle time field serialization
    result = []
    for checklist in checklists:
        checklist_dict = {
            "id": checklist.id,
            "checklist_date": checklist.checklist_date,
            "category_id": checklist.category_id,
            "site_id": checklist.site_id,
            "status": checklist.status,
            "total_items": checklist.total_items,
            "completed_items": checklist.completed_items,
            "completion_percentage": checklist.completion_percentage,
            "completed_by_id": checklist.completed_by_id,
            "created_at": checklist.created_at,
            "completed_at": checklist.completed_at,
            "updated_at": checklist.updated_at,
            "category": {
                "id": checklist.category.id,
                "name": checklist.category.name,
                "closes_at": checklist.category.closes_at.strftime('%H:%M:%S') if checklist.category.closes_at else None
            } if checklist.category else None
        }
        result.append(checklist_dict)

    return result


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
    was_completed = checklist.status == ChecklistStatus.COMPLETED
    if checklist.completion_percentage == 100:
        checklist.status = ChecklistStatus.COMPLETED
        checklist.completed_at = datetime.utcnow()
        checklist.completed_by_id = current_user.id

        # Log checklist completion (only if just completed)
        if not was_completed:
            try:
                site_name = checklist.site.name if checklist.site else "Unknown"
                category_name = checklist.category.name if checklist.category else "Unknown"
                org_name = checklist.site.organization.name if checklist.site and checklist.site.organization else None
                org_id = checklist.site.organization_id if checklist.site else None
                log_activity(
                    db=db,
                    log_type=LogType.CHECKLIST_COMPLETED,
                    message=f"Checklist completed: {category_name} at {site_name}",
                    user_id=current_user.id,
                    user_email=current_user.email,
                    organization_id=org_id,
                    organization_name=org_name
                )
            except Exception as e:
                print(f"Failed to log checklist completion: {e}")
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


@router.post("/checklists/event-based", status_code=status.HTTP_201_CREATED)
def create_event_based_checklist(
    category_id: int,
    site_id: int,
    event_type: str = None,  # Optional: "batch", "delivery", or "manual"
    event_metadata: dict = None,  # Optional: Additional event data like batch number, delivery ID, etc.
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create an event-based checklist for PER_BATCH, PER_DELIVERY, or AS_NEEDED frequencies.
    
    This endpoint allows manual or programmatic creation of checklists that are triggered
    by specific events rather than time-based schedules.
    
    Parameters:
    - category_id: The category to create a checklist for
    - site_id: The site where the checklist should be created
    - event_type: Optional identifier for the event type (e.g., "batch", "delivery", "manual")
    - event_metadata: Optional JSON metadata about the event (e.g., {"batch_id": "B123", "product": "Chicken"})
    """
    from datetime import date
    
    # Verify category exists and is event-based
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    if category.frequency not in [ChecklistFrequency.PER_BATCH, ChecklistFrequency.PER_DELIVERY, ChecklistFrequency.AS_NEEDED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category must have PER_BATCH, PER_DELIVERY, or AS_NEEDED frequency. Current: {category.frequency}"
        )
    
    # Verify site exists
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found"
        )
    
    # Verify user has access to this site (if not super admin)
    if current_user.role not in [UserRole.SUPER_ADMIN] and site.organization_id != current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this site"
        )
    
    # Create new checklist
    today = date.today()
    new_checklist = Checklist(
        checklist_date=today,
        category_id=category.id,
        site_id=site.id,
        status=ChecklistStatus.PENDING
    )
    db.add(new_checklist)
    db.flush()
    
    # Get all active tasks for this category
    tasks = db.query(Task).filter(
        Task.category_id == category.id,
        Task.is_active == True
    ).order_by(Task.order_index).all()
    
    # Create checklist items for each task
    for task in tasks:
        checklist_item = ChecklistItem(
            checklist_id=new_checklist.id,
            task_id=task.id,
            item_name=task.name,
            is_completed=False
        )
        db.add(checklist_item)
    
    # Set totals
    new_checklist.total_items = len(tasks)
    new_checklist.completed_items = 0
    
    db.commit()
    db.refresh(new_checklist)
    
    return {
        "message": "Event-based checklist created successfully",
        "checklist_id": new_checklist.id,
        "category": category.name,
        "frequency": category.frequency,
        "total_items": new_checklist.total_items,
        "event_type": event_type,
        "event_metadata": event_metadata
    }
