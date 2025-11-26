"""
Module Access Service
Handles checking, granting, and revoking user access to modules (Training, COSHH, HACCP, etc.)
"""
from sqlalchemy.orm import Session
from typing import List
from app.models.user import User, UserRole
from app.models.user_module_access import UserModuleAccess


class ModuleAccessService:
    """Service for managing user module access"""

    @staticmethod
    def has_module_access(db: Session, user_id: int, module_name: str) -> bool:
        """
        Check if a user has access to a specific module

        Rules:
        - Super admins automatically have access to all modules
        - Other users must have explicit module access granted
        """
        # Get user
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False

        # Super admins have access to everything
        if user.role == UserRole.SUPER_ADMIN:
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
            return ["TRAINING", "COSHH", "HACCP"]  # All available modules

        # Get user's explicit access
        access_records = db.query(UserModuleAccess).filter(
            UserModuleAccess.user_id == user_id
        ).all()

        return [access.module_name for access in access_records]


# Singleton instance
module_access_service = ModuleAccessService()
