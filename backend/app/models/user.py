from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class UserRole(str, enum.Enum):
    """User role enumeration."""
    SUPER_ADMIN = "super_admin"
    ORG_ADMIN = "org_admin"
    SITE_USER = "site_user"


class Department(str, enum.Enum):
    """User department enumeration."""
    MANAGEMENT = "management"
    BOH = "boh"  # Back of House
    FOH = "foh"  # Front of House


class JobTitle(str, enum.Enum):
    """User job title enumeration."""
    # Management Level - Can see all tasks
    GENERAL_MANAGER = "general_manager"
    ASSISTANT_MANAGER = "assistant_manager"
    HEAD_CHEF = "head_chef"
    SOUS_CHEF = "sous_chef"
    SUPERVISOR = "supervisor"

    # Regular Staff - See only department tasks
    TEAM_MEMBER = "team_member"

    @property
    def is_management(self) -> bool:
        """Check if job title is management level."""
        return self in [
            JobTitle.GENERAL_MANAGER,
            JobTitle.ASSISTANT_MANAGER,
            JobTitle.HEAD_CHEF,
            JobTitle.SOUS_CHEF,
            JobTitle.SUPERVISOR
        ]


class User(Base):
    """User model."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    phone = Column(String, nullable=True)

    # Department and Job Title
    department = Column(SQLEnum(Department), nullable=True)
    job_title = Column(SQLEnum(JobTitle), nullable=True)

    # Foreign Keys
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    organization = relationship("Organization", back_populates="users")
    user_sites = relationship("UserSite", back_populates="user", cascade="all, delete-orphan")
    created_checklists = relationship("Checklist", back_populates="completed_by", foreign_keys="Checklist.completed_by_id")

    @property
    def full_name(self):
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}"

    @property
    def site_ids(self):
        """Get list of site IDs assigned to this user."""
        return [us.site_id for us in self.user_sites]

    @property
    def is_management_level(self) -> bool:
        """Check if user is management level (can see all tasks)."""
        if not self.job_title:
            return False
        return self.job_title in [
            JobTitle.GENERAL_MANAGER,
            JobTitle.ASSISTANT_MANAGER,
            JobTitle.HEAD_CHEF,
            JobTitle.SOUS_CHEF,
            JobTitle.SUPERVISOR
        ]

    def can_see_task(self, task_departments: list) -> bool:
        """
        Check if user can see a task based on department allocation.

        Args:
            task_departments: List of departments the task is allocated to

        Returns:
            bool: True if user can see the task
        """
        # Super admins and org admins see everything
        if self.role in [UserRole.SUPER_ADMIN, UserRole.ORG_ADMIN]:
            return True

        # Management level users see all tasks
        if self.is_management_level:
            return True

        # If task has no department restrictions, everyone can see it
        if not task_departments:
            return True

        # Regular staff can only see tasks for their department
        return self.department in task_departments if self.department else False

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"
