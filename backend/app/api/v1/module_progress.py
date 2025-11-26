from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.auth.dependencies import get_current_user
from app.models.user import User
from app.models.course_enrollment import CourseEnrollment
from app.schemas.module_progress import (
    ModuleProgressResponse,
    ModuleProgressUpdate,
    CompleteModuleRequest
)
from app.services.module_progress_service import ModuleProgressService

router = APIRouter()


@router.get("/enrollments/{enrollment_id}/progress", response_model=List[ModuleProgressResponse])
def get_enrollment_module_progress(
    enrollment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all module progress for an enrollment."""
    # Check enrollment belongs to user
    enrollment = db.query(CourseEnrollment).filter(
        CourseEnrollment.id == enrollment_id
    ).first()

    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )

    if enrollment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own progress"
        )

    return ModuleProgressService.get_enrollment_progress(db, enrollment_id)


@router.put("/enrollments/{enrollment_id}/modules/{module_id}/progress", response_model=ModuleProgressResponse)
def update_module_progress(
    enrollment_id: int,
    module_id: int,
    progress_update: ModuleProgressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update progress for a specific module."""
    # Check enrollment belongs to user
    enrollment = db.query(CourseEnrollment).filter(
        CourseEnrollment.id == enrollment_id
    ).first()

    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )

    if enrollment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own progress"
        )

    return ModuleProgressService.update_progress(db, enrollment_id, module_id, progress_update)


@router.post("/enrollments/{enrollment_id}/modules/{module_id}/complete", response_model=ModuleProgressResponse)
def complete_module(
    enrollment_id: int,
    module_id: int,
    request: CompleteModuleRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark a module as completed."""
    # Check enrollment belongs to user
    enrollment = db.query(CourseEnrollment).filter(
        CourseEnrollment.id == enrollment_id
    ).first()

    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )

    if enrollment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own progress"
        )

    return ModuleProgressService.complete_module(
        db,
        enrollment_id,
        module_id,
        request.time_spent_seconds
    )
