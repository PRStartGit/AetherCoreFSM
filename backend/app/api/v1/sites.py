from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_org_admin, get_current_user
from app.models.user import User, UserRole
from app.models.site import Site
from app.models.organization import Organization
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
