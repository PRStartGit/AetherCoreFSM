from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User, UserRole
from app.schemas.course import CourseCreate, CourseUpdate, CourseResponse, CourseWithModulesResponse
from app.schemas.course_module import CourseModuleCreate, CourseModuleUpdate, CourseModuleResponse, ReorderModulesRequest
from app.schemas.course_category import CourseCategoryCreate, CourseCategoryUpdate, CourseCategoryResponse
from app.services.course_service import CourseService

router = APIRouter()


# ========== Course Category Endpoints ==========
@router.get("/categories", response_model=List[CourseCategoryResponse])
def list_course_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all course categories."""
    return CourseService.get_all_categories(db)


@router.post("/categories", response_model=CourseCategoryResponse, status_code=status.HTTP_201_CREATED)
def create_course_category(
    category: CourseCategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new course category (Super Admin only)."""
    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can create course categories"
        )
    return CourseService.create_category(db, category)


@router.put("/categories/{category_id}", response_model=CourseCategoryResponse)
def update_course_category(
    category_id: int,
    category: CourseCategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a course category (Super Admin only)."""
    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can update course categories"
        )
    db_category = CourseService.update_category(db, category_id, category)
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course category not found"
        )
    return db_category


@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a course category (Super Admin only)."""
    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can delete course categories"
        )
    if not CourseService.delete_category(db, category_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course category not found"
        )


# ========== Course Endpoints ==========
@router.get("", response_model=List[CourseResponse])
def list_courses(
    published_only: bool = Query(False, description="Filter to only published courses"),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all courses with optional filters."""
    # Non-super admins can only see published courses
    if current_user.role != UserRole.SUPER_ADMIN:
        published_only = True

    return CourseService.get_all_courses(
        db,
        published_only=published_only,
        category_id=category_id,
        skip=skip,
        limit=limit
    )


@router.post("", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new course (Super Admin only)."""
    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can create courses"
        )
    return CourseService.create_course(db, course, current_user.id)


@router.get("/{course_id}", response_model=CourseWithModulesResponse)
def get_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a course by ID with its modules."""
    course = CourseService.get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    # Non-super admins can only view published courses
    if current_user.role != UserRole.SUPER_ADMIN and not course.is_published:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Course is not published"
        )

    return course


@router.put("/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: int,
    course: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a course (Super Admin only)."""
    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can update courses"
        )
    db_course = CourseService.update_course(db, course_id, course)
    if not db_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return db_course


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a course (Super Admin only)."""
    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can delete courses"
        )
    if not CourseService.delete_course(db, course_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )


# ========== Course Module Endpoints ==========
@router.post("/{course_id}/modules", response_model=CourseModuleResponse, status_code=status.HTTP_201_CREATED)
def create_course_module(
    course_id: int,
    module: CourseModuleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new course module (Super Admin only)."""
    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can create course modules"
        )

    # Verify course exists
    course = CourseService.get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    # Ensure module.course_id matches the path parameter
    module.course_id = course_id

    return CourseService.create_module(db, module)


@router.get("/{course_id}/modules", response_model=List[CourseModuleResponse])
def list_course_modules(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all modules for a course."""
    course = CourseService.get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    # Non-super admins can only view modules for published courses
    if current_user.role != UserRole.SUPER_ADMIN and not course.is_published:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Course is not published"
        )

    return CourseService.get_modules_by_course_id(db, course_id)


@router.put("/modules/{module_id}", response_model=CourseModuleResponse)
def update_course_module(
    module_id: int,
    module: CourseModuleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a course module (Super Admin only)."""
    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can update course modules"
        )
    db_module = CourseService.update_module(db, module_id, module)
    if not db_module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course module not found"
        )
    return db_module


@router.delete("/modules/{module_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course_module(
    module_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a course module (Super Admin only)."""
    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can delete course modules"
        )
    if not CourseService.delete_module(db, module_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course module not found"
        )


@router.post("/{course_id}/modules/reorder", status_code=status.HTTP_204_NO_CONTENT)
def reorder_course_modules(
    course_id: int,
    reorder_request: ReorderModulesRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Reorder course modules (Super Admin only)."""
    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can reorder course modules"
        )

    # Verify course exists
    course = CourseService.get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    CourseService.reorder_modules(db, course_id, reorder_request.module_orders)
