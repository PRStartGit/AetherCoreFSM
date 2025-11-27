from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import date
from calendar import monthrange
from app.core.database import get_db
from app.core.dependencies import get_current_org_admin, get_current_user, get_current_super_admin
from app.models.user import User, UserRole
from app.models.site import Site
from app.models.organization import Organization
from app.models.category import Category, ChecklistFrequency
from app.models.checklist import Checklist, ChecklistStatus
from app.models.checklist_item import ChecklistItem
from app.models.task import Task
from app.schemas.site import SiteCreate, SiteUpdate, SiteResponse

router = APIRouter()


@router.post("/sites", response_model=SiteResponse, status_code=status.HTTP_201_CREATED)
def create_site(
    site_data: SiteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_org_admin)
):
    """Create a new site (Org Admin or Super Admin)."""
    # Check permissions
    if current_user.role == UserRole.ORG_ADMIN and current_user.organization_id != site_data.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    # Create site
    new_site = Site(
        name=site_data.name,
        site_code=site_data.site_code,
        organization_id=site_data.organization_id,
        address=site_data.address,
        city=site_data.city,
        postcode=site_data.postcode,
        country=site_data.country
    )

    db.add(new_site)
    db.commit()
    db.refresh(new_site)

    return new_site


@router.get("/sites/all", response_model=List[SiteResponse])
def list_all_sites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all sites across all organizations (Super Admin only)."""
    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can view all sites"
        )

    sites = db.query(Site).options(joinedload(Site.organization)).all()

    # Populate organization_name for each site
    for site in sites:
        if site.organization:
            site.organization_name = site.organization.name

    return sites


@router.get("/sites", response_model=List[SiteResponse])
def list_sites(
    organization_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List sites (filtered by organization for non-super-admins)."""
    query = db.query(Site).options(joinedload(Site.organization))

    # Filter by organization
    if current_user.role == UserRole.SUPER_ADMIN:
        if organization_id:
            query = query.filter(Site.organization_id == organization_id)
    else:
        # Non-super-admins can only see their org's sites
        query = query.filter(Site.organization_id == current_user.organization_id)

    sites = query.offset(skip).limit(limit).all()

    # Populate organization_name for each site
    for site in sites:
        if site.organization:
            site.organization_name = site.organization.name

    return sites


@router.get("/sites/{site_id}", response_model=SiteResponse)
def get_site(
    site_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get site by ID."""
    site = db.query(Site).filter(Site.id == site_id).first()

    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found"
        )

    # Check permissions
    if current_user.role != UserRole.SUPER_ADMIN and current_user.organization_id != site.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    return site


@router.put("/sites/{site_id}", response_model=SiteResponse)
def update_site(
    site_id: int,
    site_data: SiteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_org_admin)
):
    """Update site (Org Admin or Super Admin)."""
    site = db.query(Site).filter(Site.id == site_id).first()

    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found"
        )

    # Check permissions for org admins
    if current_user.role == UserRole.ORG_ADMIN:
        # Org admins can only update sites in their organization
        if current_user.organization_id != site.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        # Org admins cannot change the organization
        if site_data.organization_id and site_data.organization_id != site.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot change site organization"
            )

    # Update fields
    update_data = site_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(site, field, value)

    db.commit()
    db.refresh(site)

    return site


@router.delete("/sites/{site_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_site(
    site_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_org_admin)
):
    """Delete site (Org Admin or Super Admin)."""
    site = db.query(Site).filter(Site.id == site_id).first()

    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found"
        )

    # Check permissions
    if current_user.role == UserRole.ORG_ADMIN and current_user.organization_id != site.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    db.delete(site)
    db.commit()

    return None


@router.post("/sites/{site_id}/regenerate-checklists")
def regenerate_site_checklists(
    site_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """
    Regenerate checklists for a specific site (Super Admin only).
    Creates checklists for today for this site.
    """
    # Get the site
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found"
        )

    try:
        today = date.today()
        created_count = 0
        skipped_count = 0

        # Get active categories (global + organization-specific)
        categories = db.query(Category).filter(
            ((Category.is_global == True) | (Category.organization_id == site.organization_id)),
            Category.is_active == True
        ).all()

        for category in categories:
            # Determine if we should create a checklist based on frequency
            should_create = False
            checklist_date = today

            if category.frequency == ChecklistFrequency.DAILY:
                # Daily categories: create every day, due today
                should_create = True
                checklist_date = today
            elif category.frequency == ChecklistFrequency.MONTHLY:
                # Monthly categories: create for current month if not exists
                # Due date is the last day of the month
                should_create = True
                _, last_day = monthrange(today.year, today.month)
                checklist_date = date(today.year, today.month, last_day)
            elif category.frequency == ChecklistFrequency.WEEKLY:
                # Weekly categories: create for current week if not exists
                should_create = True
                checklist_date = today

            if not should_create:
                continue

            # Check if checklist already exists for this date
            existing = db.query(Checklist).filter(
                Checklist.checklist_date == checklist_date,
                Checklist.category_id == category.id,
                Checklist.site_id == site.id
            ).first()

            if existing:
                skipped_count += 1
                continue

            # Create new checklist
            new_checklist = Checklist(
                checklist_date=checklist_date,
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

            created_count += 1

        db.commit()

        return {
            "status": "success",
            "message": f"Successfully regenerated checklists for {site.name}",
            "created": created_count,
            "skipped": skipped_count,
            "site_name": site.name,
            "date": str(today)
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error regenerating checklists: {str(e)}"
        )
