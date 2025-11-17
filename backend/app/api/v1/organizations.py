from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import secrets
import string
from app.core.database import get_db
from app.core.dependencies import get_current_super_admin, get_current_user
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.organization import Organization
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationResponse,
    OrganizationWithStats
)
from app.services.email_service import send_welcome_email

router = APIRouter()


@router.post("/organizations", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
def create_organization(
    org_data: OrganizationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Create a new organization (Super Admin only)."""
    # Check if org_id already exists
    existing_org = db.query(Organization).filter(
        Organization.org_id == org_data.org_id
    ).first()

    if existing_org:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization ID already exists"
        )

    # Create organization
    new_org = Organization(
        name=org_data.name,
        org_id=org_data.org_id,
        contact_person=org_data.contact_person,
        contact_email=org_data.contact_email,
        contact_phone=org_data.contact_phone,
        address=org_data.address,
        subscription_tier=org_data.subscription_tier,
        custom_price_per_site=org_data.custom_price_per_site
    )

    db.add(new_org)
    db.commit()
    db.refresh(new_org)

    # Generate secure random password for the Org Admin
    def generate_password(length=12):
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        return password

    temp_password = generate_password()

    # Extract first and last name from contact person
    name_parts = org_data.contact_person.split(' ', 1) if org_data.contact_person else ["Admin", ""]
    first_name = name_parts[0]
    last_name = name_parts[1] if len(name_parts) > 1 else ""

    # Create Org Admin user
    org_admin = User(
        email=org_data.contact_email,
        hashed_password=get_password_hash(temp_password),
        first_name=first_name,
        last_name=last_name,
        role=UserRole.ORG_ADMIN,
        organization_id=new_org.id,
        must_change_password=True,
        is_active=True
    )

    db.add(org_admin)
    db.commit()
    db.refresh(org_admin)

    # Send welcome email
    try:
        send_welcome_email(
            email=org_data.contact_email,
            name=org_data.contact_person or "Admin",
            org_id=new_org.org_id,
            password=temp_password
        )
    except Exception as e:
        print(f"Failed to send welcome email: {str(e)}")
        # Don't fail the organization creation if email fails

    return new_org


@router.get("/organizations", response_model=List[OrganizationResponse])
def list_organizations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """List all organizations (Super Admin only)."""
    organizations = db.query(Organization).offset(skip).limit(limit).all()
    return organizations


@router.get("/organizations/{org_id}", response_model=OrganizationWithStats)
def get_organization(
    org_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get organization by ID."""
    organization = db.query(Organization).filter(Organization.id == org_id).first()

    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )

    # Check permissions (super admin or user from same org)
    if current_user.role.value != "super_admin" and current_user.organization_id != org_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    # Add stats
    total_sites = len(organization.sites)
    total_users = len(organization.users)
    active_modules = [m.module_name for m in organization.org_modules if m.is_enabled]

    org_dict = {
        **organization.__dict__,
        "total_sites": total_sites,
        "total_users": total_users,
        "active_modules": active_modules
    }

    return org_dict


@router.put("/organizations/{org_id}", response_model=OrganizationResponse)
def update_organization(
    org_id: int,
    org_data: OrganizationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Update organization (Super Admin only)."""
    organization = db.query(Organization).filter(Organization.id == org_id).first()

    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )

    # Update fields
    update_data = org_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(organization, field, value)

    db.commit()
    db.refresh(organization)

    return organization


@router.delete("/organizations/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_organization(
    org_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Delete organization (Super Admin only)."""
    organization = db.query(Organization).filter(Organization.id == org_id).first()

    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )

    db.delete(organization)
    db.commit()

    return None
