"""
Module Access Service
Handles checking, granting, and revoking user access to modules (Training, COSHH, HACCP, etc.)
"""
from sqlalchemy.orm import Session
from typing import List
from app.models.user import User, UserRole
from app.models.user_module_access import UserModuleAccess
from app.models.organization_module import OrganizationModule


class ModuleAccessService:
    """Service for managing user module access"""

    @staticmethod
    def has_module_access(db: Session, user_id: int, module_name: str) -> bool:
        """
        Check if a user has access to a specific module

        Rules:
        - Super admins automatically have access to all modules
        - If organization has the module enabled, all users in that org have access
        - Explicit user-level grants also provide access
        """
        # Get user
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False

        # Super admins have access to everything
        if user.role == UserRole.SUPER_ADMIN:
            return True

        # Check if organization has this module enabled (auto-access for all users)
        if user.organization_id:
            org_module = db.query(OrganizationModule).filter(
                OrganizationModule.organization_id == user.organization_id,
                OrganizationModule.module_name == module_name,
                OrganizationModule.is_enabled == True
            ).first()
            if org_module:
                return True

        # Check if user has explicit access to this module
        access = db.query(UserModuleAccess).filter(
            UserModuleAccess.user_id == user_id,
            UserModuleAccess.module_name == module_name
        ).first()

        return access is not None

    @staticmethod
    def grant_module_access(
        db: Session,
        user_id: int,
        module_name: str,
        granted_by_user_id: int
    ) -> UserModuleAccess:
        """
        Grant a user access to a module

        Returns the UserModuleAccess record (creates if doesn't exist, returns existing if already granted)
        """
        # Check if access already exists
        existing = db.query(UserModuleAccess).filter(
            UserModuleAccess.user_id == user_id,
            UserModuleAccess.module_name == module_name
        ).first()

        if existing:
            return existing

        # Create new access
        access = UserModuleAccess(
            user_id=user_id,
            module_name=module_name,
            granted_by_user_id=granted_by_user_id
        )
        db.add(access)
        db.commit()
        db.refresh(access)

        return access

    @staticmethod
    def revoke_module_access(db: Session, user_id: int, module_name: str) -> bool:
        """
        Revoke a user's access to a module

        Returns True if access was revoked, False if no access existed
        """
        access = db.query(UserModuleAccess).filter(
            UserModuleAccess.user_id == user_id,
            UserModuleAccess.module_name == module_name
        ).first()

        if not access:
            return False

        db.delete(access)
        db.commit()
        return True

    @staticmethod
    def get_user_modules(db: Session, user_id: int) -> List[str]:
        """
        Get all modules a user has access to

        Returns list of module names
        """
        # Get user
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return []

        # Super admins have access to all modules
        if user.role == UserRole.SUPER_ADMIN:
            return ["TRAINING", "COSHH", "HACCP", "RECIPE_BOOK"]  # All available modules

        modules = set()

        # Get modules enabled for the organization (auto-access)
        if user.organization_id:
            org_modules = db.query(OrganizationModule).filter(
                OrganizationModule.organization_id == user.organization_id,
                OrganizationModule.is_enabled == True
            ).all()
            for org_module in org_modules:
                modules.add(org_module.module_name)

        # Get user's explicit access
        access_records = db.query(UserModuleAccess).filter(
            UserModuleAccess.user_id == user_id
        ).all()
        for access in access_records:
            modules.add(access.module_name)

        return list(modules)


# Singleton instance
module_access_service = ModuleAccessService()
