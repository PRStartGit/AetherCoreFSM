from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_org_admin, get_current_user
from app.models.user import User, UserRole
from app.models.task import Task
from app.models.site_task import SiteTask
from app.models.category import Category
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskWithSites, TaskAssignment

router = APIRouter()


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_org_admin)
):
    """Create a new task (Org Admin or Super Admin)."""
    # Verify category exists and user has permission
    category = db.query(Category).filter(Category.id == task_data.category_id).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    # Check permissions
    if not category.is_global:
        if current_user.role == UserRole.ORG_ADMIN and current_user.organization_id != category.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

    new_task = Task(
        name=task_data.name,
        description=task_data.description,
        order_index=task_data.order_index,
        form_config=task_data.form_config,
        category_id=task_data.category_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@router.get("/tasks", response_model=List[TaskResponse])
def list_tasks(
    category_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List tasks (optionally filtered by category)."""
    query = db.query(Task).filter(Task.is_active == True)

    if category_id:
        query = query.filter(Task.category_id == category_id)

    # Filter by organization (non-super-admins)
    if current_user.role != UserRole.SUPER_ADMIN:
        query = query.join(Category).filter(
            (Category.organization_id == current_user.organization_id) | (Category.is_global == True)
        )

    tasks = query.offset(skip).limit(limit).all()
    return tasks


@router.get("/tasks/{task_id}", response_model=TaskWithSites)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get task by ID with assigned sites."""
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Get assigned site IDs
    site_ids = [st.site_id for st in task.site_tasks]

    task_dict = {
        **task.__dict__,
        "site_ids": site_ids
    }

    return task_dict


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_org_admin)
):
    """Update task (Org Admin or Super Admin)."""
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Check permissions
    category = task.category
    if not category.is_global:
        if current_user.role == UserRole.ORG_ADMIN and current_user.organization_id != category.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

    # Update fields
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_org_admin)
):
    """Delete task (Org Admin or Super Admin)."""
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Check permissions
    category = task.category
    if not category.is_global:
        if current_user.role == UserRole.ORG_ADMIN and current_user.organization_id != category.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

    db.delete(task)
    db.commit()

    return None


@router.post("/tasks/{task_id}/assign", status_code=status.HTTP_200_OK)
def assign_task_to_sites(
    task_id: int,
    assignment: TaskAssignment,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_org_admin)
):
    """Assign task to multiple sites."""
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Remove existing assignments
    db.query(SiteTask).filter(SiteTask.task_id == task_id).delete()

    # Add new assignments
    for site_id in assignment.site_ids:
        site_task = SiteTask(
            task_id=task_id,
            site_id=site_id
        )
        db.add(site_task)

    db.commit()

    return {"message": f"Task assigned to {len(assignment.site_ids)} sites"}
