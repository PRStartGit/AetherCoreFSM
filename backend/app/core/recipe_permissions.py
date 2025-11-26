"""
Recipe Permission Helpers
Functions to check user permissions for Recipe Book module
"""
from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.models.user_module_access import UserModuleAccess
from app.models.organization_module import OrganizationModule


def has_recipe_access(user: User, db: Session) -> bool:
    """
    Check if user has access to Recipe Book module

    Args:
        user: User object
        db: Database session

    Returns:
        True if user has access, False otherwise
    """
    # Super admin always has access
    if user.role == UserRole.SUPER_ADMIN:
        return True

    # Check if organization has the Recipe Book module enabled
    if not user.organization_id:
        return False

    org_module = db.query(OrganizationModule).filter(
        OrganizationModule.organization_id == user.organization_id,
        OrganizationModule.module_name == "recipes",
        OrganizationModule.is_enabled == True
    ).first()

    if not org_module:
        return False

    # Organization has the module enabled, now check user-level access
    # Org admin always has access if module is enabled for org
    if user.role == UserRole.ORG_ADMIN:
        return True

    # Check if user has "Zynthio Recipes" module access granted
    access = db.query(UserModuleAccess).filter(
        UserModuleAccess.user_id == user.id,
        UserModuleAccess.module_name == "Zynthio Recipes"
    ).first()

    return access is not None


def has_recipe_crud(user: User) -> bool:
    """
    Check if user can create/edit/delete recipes

    Args:
        user: User object

    Returns:
        True if user has CRUD permissions, False otherwise
    """
    # Super admin and org admin always have CRUD
    if user.role in [UserRole.SUPER_ADMIN, UserRole.ORG_ADMIN]:
        return True

    # Check job_role (Training module pattern - links to job_roles table)
    # CRUD roles: Head Chef, Sous Chef, General Manager, Assistant Manager
    if user.job_role and user.job_role.name in [
        "Head Chef",
        "Sous Chef",
        "General Manager",
        "Assistant Manager"
    ]:
        return True

    return False


def is_view_only(user: User, db: Session) -> bool:
    """
    Check if user has view-only access (can see but not edit)

    Args:
        user: User object
        db: Database session

    Returns:
        True if view-only, False otherwise
    """
    # If user has access but not CRUD, they're view-only
    return has_recipe_access(user, db) and not has_recipe_crud(user)
