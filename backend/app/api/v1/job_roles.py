"""
Job Roles API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_super_admin
from app.models.job_role import JobRole
from app.models.user import User
from app.schemas.job_role import JobRoleResponse, JobRoleCreate, JobRoleUpdate

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


@router.get("/all", response_model=List[JobRoleResponse])
def list_all_job_roles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """
    List all job roles including system roles (Super Admin only)

    Used for job roles management interface
    """
    roles = db.query(JobRole).order_by(JobRole.name).all()
    return roles


@router.get("/{role_id}", response_model=JobRoleResponse)
def get_job_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """
    Get a specific job role by ID (Super Admin only)
    """
    role = db.query(JobRole).filter(JobRole.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job role not found"
        )
    return role


@router.post("", response_model=JobRoleResponse, status_code=status.HTTP_201_CREATED)
def create_job_role(
    role_data: JobRoleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """
    Create a new job role (Super Admin only)
    """
    # Check if job role with same name already exists
    existing_role = db.query(JobRole).filter(JobRole.name == role_data.name).first()
    if existing_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Job role '{role_data.name}' already exists"
        )

    new_role = JobRole(
        name=role_data.name,
        is_system_role=role_data.is_system_role
    )
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role


@router.put("/{role_id}", response_model=JobRoleResponse)
def update_job_role(
    role_id: int,
    role_data: JobRoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """
    Update a job role (Super Admin only)
    """
    role = db.query(JobRole).filter(JobRole.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job role not found"
        )

    # Check if another role with the same name exists
    existing_role = db.query(JobRole).filter(
        JobRole.name == role_data.name,
        JobRole.id != role_id
    ).first()
    if existing_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Job role '{role_data.name}' already exists"
        )

    role.name = role_data.name
    role.is_system_role = role_data.is_system_role
    db.commit()
    db.refresh(role)
    return role


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """
    Delete a job role (Super Admin only)

    System roles cannot be deleted
    """
    role = db.query(JobRole).filter(JobRole.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job role not found"
        )

    if role.is_system_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="System roles cannot be deleted"
        )

    db.delete(role)
    db.commit()
    return None
