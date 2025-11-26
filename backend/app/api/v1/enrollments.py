from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User, UserRole
from app.schemas.course_enrollment import (
    EnrollmentCreate,
    EnrollmentUpdate,
    EnrollmentResponse,
    EnrollmentWithCourseResponse,
    AssignCoursesRequest
)
from app.services.enrollment_service import EnrollmentService

router = APIRouter()


@router.post("/assign", response_model=List[EnrollmentResponse], status_code=status.HTTP_201_CREATED)
def assign_courses_to_users(
    request: AssignCoursesRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Assign multiple courses to multiple users (Super Admin or Org Admin)."""
    # Only super admins and org admins can assign courses
    if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.ORG_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can assign courses"
        )

    # Org admins can only assign to users in their organization
    if current_user.role == UserRole.ORG_ADMIN:
        from app.models.user import User as UserModel
        users = db.query(UserModel).filter(UserModel.id.in_(request.user_ids)).all()
        if any(u.organization_id != current_user.organization_id for u in users):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only assign courses to users in your organization"
            )

    enrollments = EnrollmentService.bulk_enroll(
        db,
        request.user_ids,
        request.course_ids,
        current_user.id
    )
    return enrollments


@router.post("", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def create_enrollment(
    enrollment: EnrollmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a single enrollment (Super Admin or Org Admin)."""
    # Only super admins and org admins can create enrollments
    if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.ORG_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can create enrollments"
        )

    # Org admins can only enroll users in their organization
    if current_user.role == UserRole.ORG_ADMIN:
        from app.models.user import User as UserModel
        user = db.query(UserModel).filter(UserModel.id == enrollment.user_id).first()
        if not user or user.organization_id != current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only enroll users in your organization"
            )

    return EnrollmentService.enroll_user(db, enrollment, current_user.id)


@router.get("/my-courses", response_model=List[EnrollmentWithCourseResponse])
def get_my_enrollments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's course enrollments with course details."""
    enrollments = EnrollmentService.get_user_enrollments(db, current_user.id)

    # Build response with course details
    result = []
    for enrollment in enrollments:
        course = enrollment.course
        result.append({
            **EnrollmentResponse.model_validate(enrollment).model_dump(),
            "course_title": course.title,
            "course_description": course.description,
            "course_thumbnail_url": course.thumbnail_url,
            "course_category_name": course.category.name if course.category else None
        })

    return result


@router.get("/users/{user_id}", response_model=List[EnrollmentResponse])
def get_user_enrollments(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get enrollments for a specific user (Super Admin, Org Admin, or self)."""
    # Users can see their own enrollments
    if user_id != current_user.id:
        # Org admins can see enrollments for users in their organization
        if current_user.role == UserRole.ORG_ADMIN:
            from app.models.user import User as UserModel
            user = db.query(UserModel).filter(UserModel.id == user_id).first()
            if not user or user.organization_id != current_user.organization_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only view enrollments for users in your organization"
                )
        # Super admins can see all enrollments
        elif current_user.role != UserRole.SUPER_ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only view your own enrollments"
            )

    return EnrollmentService.get_user_enrollments(db, user_id)


@router.get("/courses/{course_id}", response_model=List[EnrollmentResponse])
def get_course_enrollments(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all enrollments for a course (Super Admin or Org Admin)."""
    if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.ORG_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can view course enrollments"
        )

    enrollments = EnrollmentService.get_course_enrollments(db, course_id)

    # Org admins can only see enrollments for users in their organization
    if current_user.role == UserRole.ORG_ADMIN:
        enrollments = [e for e in enrollments if e.user.organization_id == current_user.organization_id]

    return enrollments


@router.put("/{enrollment_id}", response_model=EnrollmentResponse)
def update_enrollment(
    enrollment_id: int,
    enrollment_update: EnrollmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an enrollment (user can update their own, admins can update any)."""
    db_enrollment = EnrollmentService.get_enrollment_by_id(db, enrollment_id)
    if not db_enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )

    # Users can only update their own enrollments
    if db_enrollment.user_id != current_user.id:
        if current_user.role == UserRole.ORG_ADMIN:
            if db_enrollment.user.organization_id != current_user.organization_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only update enrollments for users in your organization"
                )
        elif current_user.role != UserRole.SUPER_ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update your own enrollments"
            )

    updated = EnrollmentService.update_enrollment(db, enrollment_id, enrollment_update)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    return updated


@router.post("/{enrollment_id}/access", response_model=EnrollmentResponse)
def mark_enrollment_accessed(
    enrollment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark an enrollment as accessed (updates last_accessed_at)."""
    db_enrollment = EnrollmentService.get_enrollment_by_id(db, enrollment_id)
    if not db_enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )

    # Users can only access their own enrollments
    if db_enrollment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own enrollments"
        )

    updated = EnrollmentService.update_last_accessed(db, enrollment_id)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    return updated


@router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete an enrollment (Super Admin or Org Admin)."""
    db_enrollment = EnrollmentService.get_enrollment_by_id(db, enrollment_id)
    if not db_enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )

    # Only admins can delete enrollments
    if current_user.role == UserRole.ORG_ADMIN:
        if db_enrollment.user.organization_id != current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete enrollments for users in your organization"
            )
    elif current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can delete enrollments"
        )

    if not EnrollmentService.unenroll_user(db, enrollment_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
