from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel

from app.core.database import get_db
from app.core.dependencies import get_current_super_admin
from app.models.activity_log import ActivityLog, LogType
from app.models.user import User
from app.models.checklist import Checklist, ChecklistStatus

router = APIRouter()


class ActivityLogResponse(BaseModel):
    id: int
    log_type: str
    message: str
    details: Optional[str] = None
    user_email: Optional[str] = None
    organization_name: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class LogsResponse(BaseModel):
    logs: List[ActivityLogResponse]
    total: int


@router.get("/logs/task-completions", response_model=LogsResponse)
def get_task_completion_logs(
    days: int = Query(30, ge=1, le=365),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Get task/checklist completion logs."""
    since = datetime.utcnow() - timedelta(days=days)

    # Get from activity_logs table
    query = db.query(ActivityLog).filter(
        ActivityLog.log_type.in_([LogType.TASK_COMPLETED.value, LogType.CHECKLIST_COMPLETED.value]),
        ActivityLog.created_at >= since
    )

    total = query.count()
    logs = query.order_by(desc(ActivityLog.created_at)).offset(offset).limit(limit).all()

    # If no logs in activity_logs, fall back to checklists table
    if total == 0:
        checklists = db.query(Checklist).filter(
            Checklist.status == ChecklistStatus.COMPLETED,
            Checklist.completed_at >= since
        ).order_by(desc(Checklist.completed_at)).offset(offset).limit(limit).all()

        total = db.query(Checklist).filter(
            Checklist.status == ChecklistStatus.COMPLETED,
            Checklist.completed_at >= since
        ).count()

        logs = [
            ActivityLogResponse(
                id=c.id,
                log_type="checklist_completed",
                message=f"Checklist completed: {c.category.name if c.category else 'Unknown'} at {c.site.name if c.site else 'Unknown'}",
                details=None,
                user_email=c.completed_by.email if c.completed_by else None,
                organization_name=c.site.organization.name if c.site and c.site.organization else None,
                ip_address=None,
                created_at=c.completed_at or c.created_at
            ) for c in checklists
        ]
        return LogsResponse(logs=logs, total=total)

    return LogsResponse(
        logs=[ActivityLogResponse.model_validate(log) for log in logs],
        total=total
    )


@router.get("/logs/logins", response_model=LogsResponse)
def get_login_logs(
    days: int = Query(30, ge=1, le=365),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Get user login logs."""
    since = datetime.utcnow() - timedelta(days=days)

    query = db.query(ActivityLog).filter(
        ActivityLog.log_type.in_([LogType.LOGIN.value, LogType.LOGOUT.value]),
        ActivityLog.created_at >= since
    )

    total = query.count()
    logs = query.order_by(desc(ActivityLog.created_at)).offset(offset).limit(limit).all()

    return LogsResponse(
        logs=[ActivityLogResponse.model_validate(log) for log in logs],
        total=total
    )


@router.get("/logs/registrations", response_model=LogsResponse)
def get_registration_logs(
    days: int = Query(30, ge=1, le=365),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Get user and organization registration logs."""
    since = datetime.utcnow() - timedelta(days=days)

    query = db.query(ActivityLog).filter(
        ActivityLog.log_type.in_([LogType.REGISTRATION.value, LogType.ORG_REGISTRATION.value]),
        ActivityLog.created_at >= since
    )

    total = query.count()
    logs = query.order_by(desc(ActivityLog.created_at)).offset(offset).limit(limit).all()

    return LogsResponse(
        logs=[ActivityLogResponse.model_validate(log) for log in logs],
        total=total
    )


@router.get("/logs/errors", response_model=LogsResponse)
def get_error_logs(
    days: int = Query(30, ge=1, le=365),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Get error logs."""
    since = datetime.utcnow() - timedelta(days=days)

    query = db.query(ActivityLog).filter(
        ActivityLog.log_type == LogType.ERROR.value,
        ActivityLog.created_at >= since
    )

    total = query.count()
    logs = query.order_by(desc(ActivityLog.created_at)).offset(offset).limit(limit).all()

    return LogsResponse(
        logs=[ActivityLogResponse.model_validate(log) for log in logs],
        total=total
    )


# Helper function to log activities (used by other modules)
def log_activity(
    db: Session,
    log_type: LogType,
    message: str,
    user_id: Optional[int] = None,
    user_email: Optional[str] = None,
    organization_id: Optional[int] = None,
    organization_name: Optional[str] = None,
    details: Optional[str] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
):
    """Helper function to create activity log entries."""
    log = ActivityLog(
        log_type=log_type.value,
        message=message,
        user_id=user_id,
        user_email=user_email,
        organization_id=organization_id,
        organization_name=organization_name,
        details=details,
        ip_address=ip_address,
        user_agent=user_agent
    )
    db.add(log)
    db.commit()
    return log
