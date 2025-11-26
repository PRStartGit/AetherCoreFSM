from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.models.course_enrollment import CourseEnrollment, EnrollmentStatus
from app.models.course import Course
from app.models.user import User
from app.schemas.course_enrollment import EnrollmentCreate, EnrollmentUpdate


class EnrollmentService:
    """Service for course enrollment management."""

    @staticmethod
    def enroll_user(db: Session, enrollment: EnrollmentCreate, assigned_by_user_id: Optional[int] = None) -> CourseEnrollment:
        """Enroll a user in a course."""
        # Check if enrollment already exists
        existing = db.query(CourseEnrollment).filter(
            CourseEnrollment.user_id == enrollment.user_id,
            CourseEnrollment.course_id == enrollment.course_id
        ).first()

        if existing:
            return existing

        db_enrollment = CourseEnrollment(
            user_id=enrollment.user_id,
            course_id=enrollment.course_id,
            assigned_by_user_id=assigned_by_user_id,
            status=EnrollmentStatus.NOT_STARTED,
            progress_percentage=0
        )
        db.add(db_enrollment)
        db.commit()
        db.refresh(db_enrollment)
        return db_enrollment

    @staticmethod
    def bulk_enroll(db: Session, user_ids: List[int], course_ids: List[int], assigned_by_user_id: int) -> List[CourseEnrollment]:
        """Enroll multiple users in multiple courses."""
        enrollments = []
        for user_id in user_ids:
            for course_id in course_ids:
                enrollment = EnrollmentService.enroll_user(
                    db,
                    EnrollmentCreate(user_id=user_id, course_id=course_id),
                    assigned_by_user_id
                )
                enrollments.append(enrollment)
        return enrollments

    @staticmethod
    def get_user_enrollments(db: Session, user_id: int) -> List[CourseEnrollment]:
        """Get all enrollments for a user."""
        return db.query(CourseEnrollment).filter(
            CourseEnrollment.user_id == user_id
        ).order_by(CourseEnrollment.enrolled_at.desc()).all()

    @staticmethod
    def get_course_enrollments(db: Session, course_id: int) -> List[CourseEnrollment]:
        """Get all enrollments for a course."""
        return db.query(CourseEnrollment).filter(
            CourseEnrollment.course_id == course_id
        ).all()

    @staticmethod
    def get_enrollment_by_id(db: Session, enrollment_id: int) -> Optional[CourseEnrollment]:
        """Get an enrollment by ID."""
        return db.query(CourseEnrollment).filter(CourseEnrollment.id == enrollment_id).first()

    @staticmethod
    def update_enrollment(db: Session, enrollment_id: int, enrollment_update: EnrollmentUpdate) -> Optional[CourseEnrollment]:
        """Update an enrollment."""
        db_enrollment = db.query(CourseEnrollment).filter(CourseEnrollment.id == enrollment_id).first()
        if not db_enrollment:
            return None

        update_data = enrollment_update.model_dump(exclude_unset=True)

        # Auto-set timestamps based on status
        if 'status' in update_data:
            if update_data['status'] == EnrollmentStatus.IN_PROGRESS and not db_enrollment.started_at:
                db_enrollment.started_at = datetime.utcnow()
            elif update_data['status'] == EnrollmentStatus.COMPLETED:
                db_enrollment.completed_at = datetime.utcnow()
                update_data['progress_percentage'] = 100

        for key, value in update_data.items():
            setattr(db_enrollment, key, value)

        db.commit()
        db.refresh(db_enrollment)
        return db_enrollment

    @staticmethod
    def update_last_accessed(db: Session, enrollment_id: int) -> Optional[CourseEnrollment]:
        """Update the last accessed timestamp."""
        db_enrollment = db.query(CourseEnrollment).filter(CourseEnrollment.id == enrollment_id).first()
        if not db_enrollment:
            return None

        db_enrollment.last_accessed_at = datetime.utcnow()

        # If first access, set status to in_progress
        if db_enrollment.status == EnrollmentStatus.NOT_STARTED:
            db_enrollment.status = EnrollmentStatus.IN_PROGRESS
            db_enrollment.started_at = datetime.utcnow()

        db.commit()
        db.refresh(db_enrollment)
        return db_enrollment

    @staticmethod
    def unenroll_user(db: Session, enrollment_id: int) -> bool:
        """Remove a user's enrollment."""
        db_enrollment = db.query(CourseEnrollment).filter(CourseEnrollment.id == enrollment_id).first()
        if not db_enrollment:
            return False

        db.delete(db_enrollment)
        db.commit()
        return True

    @staticmethod
    def get_organization_enrollments(db: Session, organization_id: int) -> List[CourseEnrollment]:
        """Get all enrollments for users in an organization."""
        return db.query(CourseEnrollment).join(User).filter(
            User.organization_id == organization_id
        ).all()
