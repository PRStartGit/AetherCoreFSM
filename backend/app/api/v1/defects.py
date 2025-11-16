from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User, UserRole
from app.models.defect import Defect, DefectStatus, DefectSeverity
from app.schemas.defect import (
    DefectCreate, DefectUpdate, DefectResponse,
    DefectWithDetails, DefectClose
)

router = APIRouter()


@router.post("/defects", response_model=DefectResponse, status_code=status.HTTP_201_CREATED)
def create_defect(
    defect_data: DefectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new defect."""
    new_defect = Defect(
        title=defect_data.title,
        description=defect_data.description,
        severity=defect_data.severity,
        photo_url=defect_data.photo_url,
        site_id=defect_data.site_id,
        checklist_item_id=defect_data.checklist_item_id,
        reported_by_id=current_user.id,
        status=DefectStatus.OPEN
    )

    db.add(new_defect)
    db.commit()
    db.refresh(new_defect)

    return new_defect


@router.get("/defects", response_model=List[DefectWithDetails])
def list_defects(
    site_id: int = None,
    status_filter: DefectStatus = None,
    severity_filter: DefectSeverity = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List defects with filters."""
    query = db.query(Defect)

    # Filter by site
    if site_id:
        query = query.filter(Defect.site_id == site_id)

    # Filter by status
    if status_filter:
        query = query.filter(Defect.status == status_filter)

    # Filter by severity
    if severity_filter:
        query = query.filter(Defect.severity == severity_filter)

    # Filter by organization and user sites
    if current_user.role == UserRole.SUPER_ADMIN:
        # Super admins see all defects
        pass
    elif current_user.role == UserRole.ORG_ADMIN:
        # Org admins see all defects in their organization
        from app.models.site import Site
        query = query.join(Site).filter(Site.organization_id == current_user.organization_id)
    elif current_user.role == UserRole.SITE_USER:
        # Site users only see defects for their assigned sites
        assigned_site_ids = [us.site_id for us in current_user.user_sites]
        if not assigned_site_ids:
            # Return empty list if user has no assigned sites
            return []
        query = query.filter(Defect.site_id.in_(assigned_site_ids))

    defects = query.order_by(Defect.created_at.desc()).offset(skip).limit(limit).all()

    # Add details
    result = []
    for defect in defects:
        defect_dict = {
            **defect.__dict__,
            "reported_by": defect.reported_by_id,  # Add alias for frontend compatibility
            "reporter_name": defect.reported_by.full_name if defect.reported_by else None,
            "site_name": defect.site.name if defect.site else None
        }
        result.append(defect_dict)

    return result


@router.get("/defects/{defect_id}", response_model=DefectWithDetails)
def get_defect(
    defect_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get defect by ID."""
    defect = db.query(Defect).filter(Defect.id == defect_id).first()

    if not defect:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Defect not found"
        )

    # Check permissions
    if current_user.role != UserRole.SUPER_ADMIN:
        if current_user.organization_id != defect.site.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

    defect_dict = {
        **defect.__dict__,
        "reported_by": defect.reported_by_id,  # Add alias for frontend compatibility
        "reporter_name": defect.reported_by.full_name if defect.reported_by else None,
        "site_name": defect.site.name if defect.site else None
    }

    return defect_dict


@router.put("/defects/{defect_id}", response_model=DefectResponse)
def update_defect(
    defect_id: int,
    defect_data: DefectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update defect."""
    defect = db.query(Defect).filter(Defect.id == defect_id).first()

    if not defect:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Defect not found"
        )

    # Update fields
    update_data = defect_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(defect, field, value)

    db.commit()
    db.refresh(defect)

    return defect


@router.post("/defects/{defect_id}/close", response_model=DefectResponse)
def close_defect(
    defect_id: int,
    close_data: DefectClose,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Close a defect (anyone can close)."""
    defect = db.query(Defect).filter(Defect.id == defect_id).first()

    if not defect:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Defect not found"
        )

    if defect.status == DefectStatus.CLOSED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Defect is already closed"
        )

    defect.status = DefectStatus.CLOSED
    defect.closed_by_id = current_user.id
    defect.closed_at = datetime.utcnow()

    if close_data.notes:
        defect.description = (defect.description or "") + f"\n\nClosure notes: {close_data.notes}"

    db.commit()
    db.refresh(defect)

    return defect


@router.delete("/defects/{defect_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_defect(
    defect_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete defect."""
    defect = db.query(Defect).filter(Defect.id == defect_id).first()

    if not defect:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Defect not found"
        )

    db.delete(defect)
    db.commit()

    return None
