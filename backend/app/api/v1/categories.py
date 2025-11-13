from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_org_admin, get_current_user
from app.models.user import User, UserRole
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse, CategoryWithTasks

router = APIRouter()


@router.post("/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_org_admin)
):
    """Create a new category (Org Admin or Super Admin)."""
    # Super admins can create global categories
    if current_user.role == UserRole.SUPER_ADMIN:
        is_global = category_data.is_global
        org_id = category_data.organization_id if not is_global else None
    else:
        # Org admins can only create categories for their org
        is_global = False
        org_id = current_user.organization_id

    new_category = Category(
        name=category_data.name,
        description=category_data.description,
        frequency=category_data.frequency,
        closes_at=category_data.closes_at,
        is_global=is_global,
        organization_id=org_id
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@router.get("/categories", response_model=List[CategoryWithTasks])
def list_categories(
    organization_id: int = None,
    include_global: bool = True,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List categories (global + org-specific)."""
    query = db.query(Category).filter(Category.is_active == True)

    if current_user.role == UserRole.SUPER_ADMIN:
        # Super admins can filter by org
        if organization_id:
            if include_global:
                query = query.filter(
                    (Category.organization_id == organization_id) | (Category.is_global == True)
                )
            else:
                query = query.filter(Category.organization_id == organization_id)
    else:
        # Non-super-admins see their org's categories + global ones
        if include_global:
            query = query.filter(
                (Category.organization_id == current_user.organization_id) | (Category.is_global == True)
            )
        else:
            query = query.filter(Category.organization_id == current_user.organization_id)

    categories = query.offset(skip).limit(limit).all()

    # Add task count
    result = []
    for cat in categories:
        cat_dict = {
            **cat.__dict__,
            "task_count": len(cat.tasks)
        }
        result.append(cat_dict)

    return result


@router.get("/categories/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get category by ID."""
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    # Check permissions
    if not category.is_global:
        if current_user.role != UserRole.SUPER_ADMIN:
            if current_user.organization_id != category.organization_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not enough permissions"
                )

    return category


@router.put("/categories/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_org_admin)
):
    """Update category (Org Admin or Super Admin)."""
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    # Check permissions
    if category.is_global and current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can edit global categories"
        )

    if not category.is_global:
        if current_user.role == UserRole.ORG_ADMIN and current_user.organization_id != category.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

    # Update fields
    update_data = category_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(category, field, value)

    db.commit()
    db.refresh(category)

    return category


@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_org_admin)
):
    """Delete category (Org Admin or Super Admin)."""
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    # Check permissions
    if category.is_global and current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can delete global categories"
        )

    if not category.is_global:
        if current_user.role == UserRole.ORG_ADMIN and current_user.organization_id != category.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

    db.delete(category)
    db.commit()

    return None
