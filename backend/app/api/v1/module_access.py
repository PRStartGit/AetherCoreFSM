"""
Module Access API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User, UserRole
from app.schemas.module_access import UserModuleAccessResponse, GrantModuleAccessRequest
from app.services.module_access_service import module_access_service

router = APIRouter()


def can_manage_module_access(current_user: User, target_user: User) -> bool:
    """
    Check if current user can manage module access for target user

    Rules:
    - Super admins can manage anyone's access
    - Org admins can manage access for users in their organization
    """
    if current_user.role == UserRole.SUPER_ADMIN:
        return True

    if current_user.role == UserRole.ORG_ADMIN:
        # Org admins can only manage users in their org
        return current_user.organization_id == target_user.organization_id

    return False


@router.get("/users/{user_id}/module-access", response_model=List[str])
def get_user_module_access(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get list of modules a user has access to

    Returns list of module names (e.g., ["TRAINING", "COSHH"])
    """
    # Users can view their own access, admins can view anyone's
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    if current_user.id != user_id and not can_manage_module_access(current_user, target_user):
        raise HTTPException(status_code=403, detail="Not authorized to view this user's module access")

    modules = module_access_service.get_user_modules(db, user_id)
    return modules


@router.post("/users/{user_id}/module-access", response_model=UserModuleAccessResponse)
def grant_user_module_access(
    user_id: int,
    request: GrantModuleAccessRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Grant a user access to a module

    Only super admins and org admins can grant access
    """
    # Check target user exists
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check permissions
    if not can_manage_module_access(current_user, target_user):
        raise HTTPException(status_code=403, detail="Not authorized to grant module access")

    # Grant access
    access = module_access_service.grant_module_access(
        db=db,
        user_id=user_id,
        module_name=request.module_name,
        granted_by_user_id=current_user.id
    )

    return access


@router.delete("/users/{user_id}/module-access/{module_name}")
def revoke_user_module_access(
    user_id: int,
    module_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Revoke a user's access to a module

    Only super admins and org admins can revoke access
    """
    # Check target user exists
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check permissions
    if not can_manage_module_access(current_user, target_user):
        raise HTTPException(status_code=403, detail="Not authorized to revoke module access")

    # Revoke access
    success = module_access_service.revoke_module_access(db, user_id, module_name)

    if not success:
        raise HTTPException(status_code=404, detail="Module access not found")

    return {"message": f"Module access to {module_name} revoked successfully"}
