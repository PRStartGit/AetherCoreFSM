from pydantic import BaseModel
from typing import Optional, Dict, Any, List, Union
from datetime import datetime


class TaskFieldBase(BaseModel):
    """Base task field schema."""
    field_type: str  # number, text, temperature, yes_no, dropdown, photo, repeating_group
    field_label: str
    field_order: int
    is_required: bool = True
    validation_rules: Optional[Dict[str, Any]] = None
    options: Optional[List[str]] = None  # For dropdown fields
    show_if: Optional[Dict[str, Any]] = None  # Conditional logic


class TaskFieldCreate(TaskFieldBase):
    """Task field creation schema."""
    task_id: int


class TaskFieldUpdate(BaseModel):
    """Task field update schema."""
    field_type: Optional[str] = None
    field_label: Optional[str] = None
    field_order: Optional[int] = None
    is_required: Optional[bool] = None
    validation_rules: Optional[Dict[str, Any]] = None
    options: Optional[List[str]] = None
    show_if: Optional[Dict[str, Any]] = None


class TaskFieldResponse(TaskFieldBase):
    """Task field response schema."""
    id: int
    task_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TaskFieldBulkCreate(BaseModel):
    """Bulk create task fields for a task."""
    task_id: int
    fields: List[TaskFieldBase]


class TaskFieldResponseCreate(BaseModel):
    """Task field response creation schema."""
    checklist_item_id: int
    task_field_id: int
    # Only one of these should be populated
    text_value: Optional[str] = None
    number_value: Optional[float] = None
    boolean_value: Optional[bool] = None
    json_value: Optional[Union[Dict[str, Any], List[Any]]] = None
    file_url: Optional[str] = None
    completed_by: Optional[int] = None


class TaskFieldResponseUpdate(BaseModel):
    """Task field response update schema."""
    text_value: Optional[str] = None
    number_value: Optional[float] = None
    boolean_value: Optional[bool] = None
    json_value: Optional[Union[Dict[str, Any], List[Any]]] = None
    file_url: Optional[str] = None


class TaskFieldResponseSchema(BaseModel):
    """Task field response schema."""
    id: int
    checklist_item_id: int
    task_field_id: int
    text_value: Optional[str] = None
    number_value: Optional[float] = None
    boolean_value: Optional[bool] = None
    json_value: Optional[Union[Dict[str, Any], List[Any]]] = None
    file_url: Optional[str] = None
    auto_defect_id: Optional[int] = None
    completed_at: datetime
    completed_by: Optional[int] = None

    class Config:
        from_attributes = True


class TaskFieldResponseSubmission(BaseModel):
    """Submit multiple field responses at once."""
    checklist_item_id: int
    responses: List[TaskFieldResponseCreate]
