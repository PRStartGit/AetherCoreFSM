from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.models.module_progress import ModuleProgress
from app.models.course_enrollment import CourseEnrollment, EnrollmentStatus
from app.models.course_module import CourseModule
from app.schemas.module_progress import ModuleProgressCreate, ModuleProgressUpdate


class ModuleProgressService:
    """Service for module progress tracking."""

    @staticmethod
    def get_or_create_progress(db: Session, enrollment_id: int, module_id: int) -> ModuleProgress:
        """Get existing progress or create new one."""
        progress = db.query(ModuleProgress).filter(
            ModuleProgress.enrollment_id == enrollment_id,
            ModuleProgress.module_id == module_id
        ).first()

        if not progress:
            progress = ModuleProgress(
                enrollment_id=enrollment_id,
                module_id=module_id,
                is_completed=False,
                time_spent_seconds=0,
                last_position_seconds=0
            )
            db.add(progress)
            db.commit()
            db.refresh(progress)

        return progress

    @staticmethod
    def update_progress(
        db: Session,
        enrollment_id: int,
        module_id: int,
        update_data: ModuleProgressUpdate
    ) -> ModuleProgress:
        """Update module progress."""
        progress = ModuleProgressService.get_or_create_progress(db, enrollment_id, module_id)

        update_dict = update_data.model_dump(exclude_unset=True)

        # If marking as completed, set completed_at
        if update_dict.get('is_completed') and not progress.is_completed:
            progress.completed_at = datetime.utcnow()

        for key, value in update_dict.items():
            setattr(progress, key, value)

        db.commit()
        db.refresh(progress)

        # Update overall course progress
        ModuleProgressService.update_course_progress(db, enrollment_id)

        return progress

    @staticmethod
    def complete_module(
        db: Session,
        enrollment_id: int,
        module_id: int,
        time_spent_seconds: int = 0
    ) -> ModuleProgress:
        """Mark a module as completed."""
        progress = ModuleProgressService.get_or_create_progress(db, enrollment_id, module_id)

        if not progress.is_completed:
            progress.is_completed = True
            progress.completed_at = datetime.utcnow()
            progress.time_spent_seconds += time_spent_seconds

            db.commit()
            db.refresh(progress)

            # Update overall course progress
            ModuleProgressService.update_course_progress(db, enrollment_id)

        return progress

    @staticmethod
    def get_enrollment_progress(db: Session, enrollment_id: int) -> List[ModuleProgress]:
        """Get all module progress for an enrollment."""
        return db.query(ModuleProgress).filter(
            ModuleProgress.enrollment_id == enrollment_id
        ).all()

    @staticmethod
    def update_course_progress(db: Session, enrollment_id: int) -> None:
        """Update overall course completion percentage based on completed modules."""
        enrollment = db.query(CourseEnrollment).filter(
            CourseEnrollment.id == enrollment_id
        ).first()

        if not enrollment:
            return

        # Get total modules for the course
        total_modules = db.query(CourseModule).filter(
            CourseModule.course_id == enrollment.course_id
        ).count()

        if total_modules == 0:
            return

        # Get completed modules
        completed_modules = db.query(ModuleProgress).filter(
            ModuleProgress.enrollment_id == enrollment_id,
            ModuleProgress.is_completed == True
        ).count()

        # Calculate progress percentage
        progress_percentage = int((completed_modules / total_modules) * 100)
        enrollment.progress_percentage = progress_percentage

        # Update enrollment status based on progress
        if progress_percentage == 100 and enrollment.status != EnrollmentStatus.COMPLETED:
            enrollment.status = EnrollmentStatus.COMPLETED
            enrollment.completed_at = datetime.utcnow()
        elif progress_percentage > 0 and enrollment.status == EnrollmentStatus.NOT_STARTED:
            enrollment.status = EnrollmentStatus.IN_PROGRESS
            if not enrollment.started_at:
                enrollment.started_at = datetime.utcnow()

        db.commit()

    @staticmethod
    def get_next_incomplete_module(db: Session, enrollment_id: int) -> Optional[CourseModule]:
        """Get the next incomplete module for an enrollment."""
        enrollment = db.query(CourseEnrollment).filter(
            CourseEnrollment.id == enrollment_id
        ).first()

        if not enrollment:
            return None

        # Get all modules for the course
        modules = db.query(CourseModule).filter(
            CourseModule.course_id == enrollment.course_id
        ).order_by(CourseModule.order_index).all()

        # Get completed module IDs
        completed_module_ids = [
            p.module_id for p in db.query(ModuleProgress).filter(
                ModuleProgress.enrollment_id == enrollment_id,
                ModuleProgress.is_completed == True
            ).all()
        ]

        # Find first incomplete module
        for module in modules:
            if module.id not in completed_module_ids:
                return module

        return None
