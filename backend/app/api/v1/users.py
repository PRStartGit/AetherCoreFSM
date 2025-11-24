from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
import secrets
import string
import logging
from app.core.database import get_db

logger = logging.getLogger(__name__)
from app.core.dependencies import get_current_org_admin, get_current_user
from app.core.security import get_password_hash
from app.core.email import send_welcome_email
from app.api.v1.activity_logs import log_activity
from app.models.activity_log import LogType
from app.models.user import User, UserRole
from app.models.user_site import UserSite
from app.models.organization import Organization
from app.models.site import Site
from app.schemas.user import UserCreate, UserUpdate, UserResponse

router = APIRouter()


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_org_admin)
):
    """Create a new user (Org Admin or Super Admin)."""
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Check permissions
    if current_user.role == UserRole.ORG_ADMIN:
        # Org admins can only create users for their organization
        if user_data.organization_id != current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        # Org admins cannot create super admins
        if user_data.role == UserRole.SUPER_ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot create super admin users"
            )

    # Super Admins must not have an organization_id
    final_organization_id = None if user_data.role == UserRole.SUPER_ADMIN else user_data.organization_id

    # Create user
    new_user = User(
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        role=user_data.role,
        phone=user_data.phone,
        organization_id=final_organization_id,
        is_active=user_data.is_active,
        must_change_password=True  # Force password change on first login
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Assign sites if provided
    if user_data.site_ids:
        for site_id in user_data.site_ids:
            user_site = UserSite(user_id=new_user.id, site_id=site_id)
            db.add(user_site)
        db.commit()

    # Refresh to get relationships
    db.refresh(new_user)

    # Send welcome email
    try:
        # Get organization name
        organization = db.query(Organization).filter(Organization.id == user_data.organization_id).first()
        organization_name = organization.name if organization else "Your Organization"

        # Get assigned site names
        assigned_sites = "All sites" if not user_data.site_ids else ", ".join(
            [site.name for site in db.query(Site).filter(Site.id.in_(user_data.site_ids)).all()]
        )

        # Log email attempt
        logger.info(f"Attempting to send welcome email to {new_user.email} (role: {new_user.role.value})")

        # Send welcome email with temporary password
        email_sent = send_welcome_email(
            user_email=new_user.email,
            user_name=f"{new_user.first_name} {new_user.last_name}",
            organization_name=organization_name,
            user_role=new_user.role.value,
            temporary_password=user_data.password,  # Original password before hashing
            assigned_sites=assigned_sites,
            login_url="https://zynthio.com/login"
        )

        if email_sent:
            logger.info(f"Welcome email sent successfully to {new_user.email}")
        else:
            logger.warning(f"Welcome email failed to send to {new_user.email} (no exception raised)")
    except Exception as e:
        # Log error but don't fail user creation
        import traceback
        logger.error(f"Failed to send welcome email to {new_user.email}: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")

    # Log user registration
    try:
        log_activity(
            db=db,
            log_type=LogType.REGISTRATION,
            message=f"New user created: {new_user.email} ({new_user.role.value})",
            user_id=new_user.id,
            user_email=new_user.email,
            organization_id=new_user.organization_id,
            organization_name=organization_name
        )
    except Exception as e:
        logger.error(f"Failed to log user registration: {e}")

    return new_user


@router.get("/users", response_model=List[UserResponse])
def list_users(
    organization_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List users (filtered by organization for non-super-admins)."""
    query = db.query(User)

    # Filter by organization
    if current_user.role == UserRole.SUPER_ADMIN:
        if organization_id:
            query = query.filter(User.organization_id == organization_id)
    else:
        # Non-super-admins can only see their org's users
        query = query.filter(User.organization_id == current_user.organization_id)

    users = query.offset(skip).limit(limit).all()
    return users


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user by ID."""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Check permissions
    if current_user.role != UserRole.SUPER_ADMIN:
        if current_user.organization_id != user.organization_id and current_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

    return user


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_org_admin)
):
    """Update user (Org Admin or Super Admin)."""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Check permissions
    if current_user.role == UserRole.ORG_ADMIN:
        if current_user.organization_id != user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        # Org admins cannot change role to super admin
        if user_data.role == UserRole.SUPER_ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot set super admin role"
            )

    # Update fields
    update_data = user_data.model_dump(exclude_unset=True)
    site_ids = update_data.pop('site_ids', None)

    for field, value in update_data.items():
        setattr(user, field, value)

    # If role is being changed to SUPER_ADMIN, ensure organization_id is NULL
    if user.role == UserRole.SUPER_ADMIN:
        user.organization_id = None

    # Update site assignments if provided
    if site_ids is not None:
        # Remove existing site assignments
        db.query(UserSite).filter(UserSite.user_id == user_id).delete()

        # Add new site assignments
        for site_id in site_ids:
            user_site = UserSite(user_id=user_id, site_id=site_id)
            db.add(user_site)

    db.commit()
    db.refresh(user)

    return user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_org_admin)
):
    """Delete user (Org Admin or Super Admin)."""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Check permissions
    if current_user.role == UserRole.ORG_ADMIN and current_user.organization_id != user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    # Don't allow deleting yourself
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )

    # Delete all related records before deleting user
    from app.models.password_reset_token import PasswordResetToken
    from app.models.user_site import UserSite
    from app.models.system_message import SystemMessage
    from app.models.activity_log import ActivityLog
    
    # Delete password reset tokens
    db.query(PasswordResetToken).filter(PasswordResetToken.user_id == user_id).delete()
    
    # Delete user site assignments
    db.query(UserSite).filter(UserSite.user_id == user_id).delete()
    
    # Delete message dismissals (if table exists)
    try:
        db.execute(text("DELETE FROM message_dismissals WHERE user_id = :uid"), {"uid": user_id})
    except:
        pass
    
    # Set system messages created_by to NULL instead of deleting
    db.query(SystemMessage).filter(SystemMessage.created_by_user_id == user_id).update({"created_by_user_id": None})
    
    # Set activity logs user_id to NULL instead of deleting (preserve audit trail)
    db.query(ActivityLog).filter(ActivityLog.user_id == user_id).update({"user_id": None})
    
    db.delete(user)
    db.commit()

    return None
