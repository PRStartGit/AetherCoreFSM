from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.core.database import get_db
from app.core.dependencies import get_current_org_admin, get_current_user
from app.models.user import User, UserRole
from app.models.task import Task
from app.models.task_field import TaskField
from app.models.task_field_response import TaskFieldResponse
from app.models.checklist_item import ChecklistItem
from app.models.checklist import Checklist, ChecklistStatus
from app.schemas.task_field import (
    TaskFieldCreate,
    TaskFieldUpdate,
    TaskFieldResponse as TaskFieldResponseSchema,
    TaskFieldBulkCreate,
    TaskFieldResponseCreate,
    TaskFieldResponseSchema as TaskFieldResponseSchemaResponse,
    TaskFieldResponseSubmission
)

router = APIRouter()


# ========== Task Fields CRUD ==========

@router.post("/task-fields", response_model=TaskFieldResponseSchema, status_code=status.HTTP_201_CREATED)
def create_task_field(
    field_data: TaskFieldCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_org_admin)
):
    """Create a new task field (Org Admin or Super Admin)."""
    # Verify task exists
    task = db.query(Task).filter(Task.id == field_data.task_id).first()

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

    new_field = TaskField(
        task_id=field_data.task_id,
        field_type=field_data.field_type,
        field_label=field_data.field_label,
        field_order=field_data.field_order,
        is_required=field_data.is_required,
        validation_rules=field_data.validation_rules,
        options=field_data.options,
        show_if=field_data.show_if
    )

    db.add(new_field)
    db.commit()
    db.refresh(new_field)

    return new_field


@router.post("/task-fields/bulk", response_model=List[TaskFieldResponseSchema], status_code=status.HTTP_201_CREATED)
def create_task_fields_bulk(
    bulk_data: TaskFieldBulkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_org_admin)
):
    """Create multiple task fields for a task (Org Admin or Super Admin)."""
    # Verify task exists
    task = db.query(Task).filter(Task.id == bulk_data.task_id).first()

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

    # Update task to indicate it has dynamic form
    task.has_dynamic_form = True

    # Create all fields
    created_fields = []
    for field_data in bulk_data.fields:
        new_field = TaskField(
            task_id=bulk_data.task_id,
            field_type=field_data.field_type,
            field_label=field_data.field_label,
            field_order=field_data.field_order,
            is_required=field_data.is_required,
            validation_rules=field_data.validation_rules,
            options=field_data.options,
            show_if=field_data.show_if
        )
        db.add(new_field)
        created_fields.append(new_field)

    db.commit()
    for field in created_fields:
        db.refresh(field)

    return created_fields


@router.get("/task-fields", response_model=List[TaskFieldResponseSchema])
def list_task_fields(
    task_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List task fields (optionally filtered by task)."""
    query = db.query(TaskField)

    if task_id:
        query = query.filter(TaskField.task_id == task_id)

    fields = query.order_by(TaskField.field_order).all()
    return fields


@router.get("/task-fields/{field_id}", response_model=TaskFieldResponseSchema)
def get_task_field(
    field_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get task field by ID."""
    field = db.query(TaskField).filter(TaskField.id == field_id).first()

    if not field:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task field not found"
        )

    return field


@router.put("/task-fields/{field_id}", response_model=TaskFieldResponseSchema)
def update_task_field(
    field_id: int,
    field_data: TaskFieldUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_org_admin)
):
    """Update task field (Org Admin or Super Admin)."""
    field = db.query(TaskField).filter(TaskField.id == field_id).first()

    if not field:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task field not found"
        )

    # Check permissions
    task = field.task
    category = task.category
    if not category.is_global:
        if current_user.role == UserRole.ORG_ADMIN and current_user.organization_id != category.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

    # Update fields
    update_data = field_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(field, key, value)

    db.commit()
    db.refresh(field)

    return field


@router.delete("/task-fields/{field_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_field(
    field_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_org_admin)
):
    """Delete task field (Org Admin or Super Admin)."""
    field = db.query(TaskField).filter(TaskField.id == field_id).first()

    if not field:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task field not found"
        )

    # Check permissions
    task = field.task
    category = task.category
    if not category.is_global:
        if current_user.role == UserRole.ORG_ADMIN and current_user.organization_id != category.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

    db.delete(field)
    db.commit()

    return None


# ========== Task Field Responses ==========

@router.post("/task-field-responses", response_model=List[TaskFieldResponseSchemaResponse], status_code=status.HTTP_201_CREATED)
def submit_field_responses(
    submission: TaskFieldResponseSubmission,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit field responses for a checklist item."""
    from app.models.defect import Defect, DefectSeverity, DefectStatus

    # Verify checklist item exists
    checklist_item = db.query(ChecklistItem).filter(ChecklistItem.id == submission.checklist_item_id).first()

    if not checklist_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Checklist item not found"
        )

    # Get checklist for site_id
    checklist = db.query(Checklist).filter(Checklist.id == checklist_item.checklist_id).first()
    site_id = checklist.site_id if checklist else None
    
    # Check if checklist is overdue - prevent completion of overdue checklists
    if checklist:
        from datetime import date, datetime, time as dt_time
        from app.models.category import Category
        
        category = db.query(Category).filter(Category.id == checklist.category_id).first()
        today = date.today()
        now = datetime.now()
        
        # If checklist date is in the past, it's overdue
        if checklist.checklist_date < today:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot complete overdue checklist. This checklist was due on " + str(checklist.checklist_date)
            )
        
        # If checklist is for today but past closing time, it's overdue
        if checklist.checklist_date == today and category and category.closes_at:
            closes_at_time = category.closes_at
            current_time = now.time()
            if current_time > closes_at_time:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot complete checklist after closing time (" + str(closes_at_time) + ")"
                )

    # Create all responses
    created_responses = []
    for response_data in submission.responses:
        new_response = TaskFieldResponse(
            checklist_item_id=submission.checklist_item_id,
            task_field_id=response_data.task_field_id,
            text_value=response_data.text_value,
            number_value=response_data.number_value,
            boolean_value=response_data.boolean_value,
            json_value=response_data.json_value,
            file_url=response_data.file_url,
            completed_by=current_user.id
        )
        db.add(new_response)
        db.flush()  # Flush to get response ID for defect linking

        # Temperature validation and automatic defect creation
        task_field = db.query(TaskField).filter(TaskField.id == response_data.task_field_id).first()

        if task_field:
            # Check regular temperature fields
            if response_data.number_value is not None and task_field.field_type in ["TEMPERATURE", "NUMBER"]:
                temperature = response_data.number_value
                field_label_lower = task_field.field_label.lower()

                # Determine if it's a fridge or freezer based on field label
                is_fridge = any(keyword in field_label_lower for keyword in ["fridge", "refrigerator", "chiller"])
                is_freezer = any(keyword in field_label_lower for keyword in ["freezer", "frozen"])

                # Legal limits
                FRIDGE_MAX = 8  # Fridges must be below 8°C
                FREEZER_MAX = -18  # Freezers must be at or below -18°C

                violation = None
                if is_fridge and temperature >= FRIDGE_MAX:
                    violation = f"Fridge temperature {temperature}°C exceeds legal limit (must be < {FRIDGE_MAX}°C)"
                elif is_freezer and temperature > FREEZER_MAX:
                    violation = f"Freezer temperature {temperature}°C exceeds legal limit (must be ≤ {FREEZER_MAX}°C)"

                if violation and site_id:
                    # Create defect automatically
                    defect = Defect(
                        title=f"Temperature Violation: {task_field.field_label}",
                        description=violation,
                        severity=DefectSeverity.HIGH,
                        status=DefectStatus.OPEN,
                        site_id=site_id,
                        checklist_item_id=checklist_item.id,
                        reported_by_id=current_user.id
                    )
                    db.add(defect)
                    db.flush()  # Get defect ID

                    # Link defect to response
                    new_response.auto_defect_id = defect.id

            # Check repeating group temperature fields (JSON)
            elif response_data.json_value and isinstance(response_data.json_value, list):
                field_label_lower = task_field.field_label.lower()
                is_fridge = any(keyword in field_label_lower for keyword in ["fridge", "refrigerator", "chiller"])
                is_freezer = any(keyword in field_label_lower for keyword in ["freezer", "frozen"])

                # Legal limits
                FRIDGE_MAX = 8
                FREEZER_MAX = -18

                violations = []
                for idx, instance in enumerate(response_data.json_value):
                    if isinstance(instance, dict) and "temperature" in instance:
                        temperature = instance.get("temperature")
                        if temperature is not None:
                            try:
                                temp_value = float(temperature)
                                item_number = idx + 1

                                if is_fridge and temp_value >= FRIDGE_MAX:
                                    violations.append(f"Item {item_number}: {temp_value}°C exceeds limit (must be < {FRIDGE_MAX}°C)")
                                elif is_freezer and temp_value > FREEZER_MAX:
                                    violations.append(f"Item {item_number}: {temp_value}°C exceeds limit (must be ≤ {FREEZER_MAX}°C)")
                            except (ValueError, TypeError):
                                pass  # Skip invalid temperature values

                if violations and site_id:
                    # Create single defect for all violations in this group
                    violation_text = "\n".join(violations)
                    defect = Defect(
                        title=f"Temperature Violation: {task_field.field_label}",
                        description=f"Multiple temperature readings outside legal limits:\n{violation_text}",
                        severity=DefectSeverity.HIGH,
                        status=DefectStatus.OPEN,
                        site_id=site_id,
                        checklist_item_id=checklist_item.id,
                        reported_by_id=current_user.id
                    )
                    db.add(defect)
                    db.flush()

                    # Link defect to response
                    new_response.auto_defect_id = defect.id

        created_responses.append(new_response)

    # Mark checklist item as completed
    checklist_item.is_completed = True
    checklist_item.completed_at = datetime.utcnow()

    # Flush changes to database so the count query can see the updated item
    db.flush()

    # Update parent checklist completion statistics with row-level locking to prevent race conditions
    checklist = db.query(Checklist).filter(
        Checklist.id == checklist_item.checklist_id
    ).with_for_update().first()

    if checklist:
        # Count completed items
        completed_count = db.query(ChecklistItem).filter(
            ChecklistItem.checklist_id == checklist.id,
            ChecklistItem.is_completed == True
        ).count()

        checklist.completed_items = completed_count
        checklist.calculate_completion()

        # Update checklist status to in_progress
        if checklist.status == ChecklistStatus.PENDING:
            checklist.status = ChecklistStatus.IN_PROGRESS

        # If all items are completed, mark checklist as completed
        if checklist.completed_items == checklist.total_items and checklist.total_items > 0:
            checklist.status = ChecklistStatus.COMPLETED
            checklist.completed_at = datetime.utcnow()
            checklist.completed_by_id = current_user.id

    db.commit()
    for response in created_responses:
        db.refresh(response)

    return created_responses


@router.get("/task-field-responses", response_model=List[TaskFieldResponseSchemaResponse])
def list_field_responses(
    checklist_item_id: int = None,
    task_field_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List field responses (filtered by checklist item or field)."""
    query = db.query(TaskFieldResponse)

    if checklist_item_id:
        query = query.filter(TaskFieldResponse.checklist_item_id == checklist_item_id)

    if task_field_id:
        query = query.filter(TaskFieldResponse.task_field_id == task_field_id)

    responses = query.all()
    return responses


@router.get("/task-field-responses/{response_id}", response_model=TaskFieldResponseSchemaResponse)
def get_field_response(
    response_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get field response by ID."""
    response = db.query(TaskFieldResponse).filter(TaskFieldResponse.id == response_id).first()

    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Field response not found"
        )

    return response
