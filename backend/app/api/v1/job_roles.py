"""
Job Roles API endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.job_role import JobRole
from app.models.user import User
from app.schemas.job_role import JobRoleResponse

router = APIRouter()


@router.get("", response_model=List[JobRoleResponse])
def list_job_roles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all job roles (excluding system roles like Platform Manager)

    Used for dropdowns in user forms
    """
    # Get all job roles except system roles (Platform Manager)
    roles = db.query(JobRole).filter(JobRole.is_system_role == False).order_by(JobRole.name).all()

    return roles
