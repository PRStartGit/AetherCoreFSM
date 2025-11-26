from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.course import Course
from app.models.course_module import CourseModule
from app.models.course_category import CourseCategory
from app.schemas.course import CourseCreate, CourseUpdate
from app.schemas.course_module import CourseModuleCreate, CourseModuleUpdate
from app.schemas.course_category import CourseCategoryCreate, CourseCategoryUpdate


class CourseService:
    """Service for course management."""

    # ========== Course CRUD ==========
    @staticmethod
    def create_course(db: Session, course: CourseCreate, created_by_user_id: int) -> Course:
        """Create a new course."""
        db_course = Course(
            **course.model_dump(),
            created_by_user_id=created_by_user_id
        )
        db.add(db_course)
        db.commit()
        db.refresh(db_course)
        return db_course

    @staticmethod
    def get_course_by_id(db: Session, course_id: int) -> Optional[Course]:
        """Get a course by ID."""
        return db.query(Course).filter(Course.id == course_id).first()

    @staticmethod
    def get_all_courses(
        db: Session,
        published_only: bool = False,
        category_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Course]:
        """Get all courses with optional filters."""
        query = db.query(Course)

        if published_only:
            query = query.filter(Course.is_published == True)

        if category_id:
            query = query.filter(Course.category_id == category_id)

        return query.order_by(Course.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def update_course(db: Session, course_id: int, course_update: CourseUpdate) -> Optional[Course]:
        """Update a course."""
        db_course = db.query(Course).filter(Course.id == course_id).first()
        if not db_course:
            return None

        update_data = course_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_course, key, value)

        db.commit()
        db.refresh(db_course)
        return db_course

    @staticmethod
    def delete_course(db: Session, course_id: int) -> bool:
        """Delete a course."""
        db_course = db.query(Course).filter(Course.id == course_id).first()
        if not db_course:
            return False

        db.delete(db_course)
        db.commit()
        return True

    # ========== Course Module CRUD ==========
    @staticmethod
    def create_module(db: Session, module: CourseModuleCreate) -> CourseModule:
        """Create a new course module."""
        db_module = CourseModule(**module.model_dump())
        db.add(db_module)
        db.commit()
        db.refresh(db_module)
        return db_module

    @staticmethod
    def get_module_by_id(db: Session, module_id: int) -> Optional[CourseModule]:
        """Get a course module by ID."""
        return db.query(CourseModule).filter(CourseModule.id == module_id).first()

    @staticmethod
    def get_modules_by_course_id(db: Session, course_id: int) -> List[CourseModule]:
        """Get all modules for a course, ordered by order_index."""
        return db.query(CourseModule).filter(
            CourseModule.course_id == course_id
        ).order_by(CourseModule.order_index).all()

    @staticmethod
    def update_module(db: Session, module_id: int, module_update: CourseModuleUpdate) -> Optional[CourseModule]:
        """Update a course module."""
        db_module = db.query(CourseModule).filter(CourseModule.id == module_id).first()
        if not db_module:
            return None

        update_data = module_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_module, key, value)

        db.commit()
        db.refresh(db_module)
        return db_module

    @staticmethod
    def delete_module(db: Session, module_id: int) -> bool:
        """Delete a course module."""
        db_module = db.query(CourseModule).filter(CourseModule.id == module_id).first()
        if not db_module:
            return False

        db.delete(db_module)
        db.commit()
        return True

    @staticmethod
    def reorder_modules(db: Session, course_id: int, module_orders: dict[int, int]) -> bool:
        """Reorder course modules."""
        for module_id, new_order in module_orders.items():
            db_module = db.query(CourseModule).filter(
                CourseModule.id == module_id,
                CourseModule.course_id == course_id
            ).first()
            if db_module:
                db_module.order_index = new_order

        db.commit()
        return True

    # ========== Course Category CRUD ==========
    @staticmethod
    def create_category(db: Session, category: CourseCategoryCreate) -> CourseCategory:
        """Create a new course category."""
        db_category = CourseCategory(**category.model_dump())
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category

    @staticmethod
    def get_category_by_id(db: Session, category_id: int) -> Optional[CourseCategory]:
        """Get a course category by ID."""
        return db.query(CourseCategory).filter(CourseCategory.id == category_id).first()

    @staticmethod
    def get_all_categories(db: Session) -> List[CourseCategory]:
        """Get all course categories."""
        return db.query(CourseCategory).order_by(CourseCategory.name).all()

    @staticmethod
    def update_category(db: Session, category_id: int, category_update: CourseCategoryUpdate) -> Optional[CourseCategory]:
        """Update a course category."""
        db_category = db.query(CourseCategory).filter(CourseCategory.id == category_id).first()
        if not db_category:
            return None

        update_data = category_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_category, key, value)

        db.commit()
        db.refresh(db_category)
        return db_category

    @staticmethod
    def delete_category(db: Session, category_id: int) -> bool:
        """Delete a course category."""
        db_category = db.query(CourseCategory).filter(CourseCategory.id == category_id).first()
        if not db_category:
            return False

        db.delete(db_category)
        db.commit()
        return True
