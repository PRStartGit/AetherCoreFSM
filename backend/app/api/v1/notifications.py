"""
Notifications API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.notification import Notification
from app.schemas.notification import NotificationResponse, NotificationMarkRead

router = APIRouter()


@router.get("", response_model=List[NotificationResponse])
def get_notifications(
    unread_only: bool = False,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get notifications for the current user"""
    query = db.query(Notification).filter(Notification.user_id == current_user.id)

    if unread_only:
        query = query.filter(Notification.is_read == False)

    notifications = query.order_by(Notification.created_at.desc()).limit(limit).all()
    return notifications


@router.get("/unread-count")
def get_unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get count of unread notifications"""
    count = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).count()
    return {"count": count}


@router.post("/mark-read")
def mark_notifications_read(
    data: NotificationMarkRead,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark specific notifications as read"""
    notifications = db.query(Notification).filter(
        Notification.id.in_(data.notification_ids),
        Notification.user_id == current_user.id
    ).all()

    for notification in notifications:
        notification.mark_as_read()

    db.commit()
    return {"success": True, "marked_count": len(notifications)}


@router.post("/mark-all-read")
def mark_all_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark all notifications as read for the current user"""
    count = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).update({
        "is_read": True,
        "read_at": datetime.utcnow()
    })
    db.commit()
    return {"success": True, "marked_count": count}


@router.delete("/{notification_id}")
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a specific notification"""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    db.delete(notification)
    db.commit()
    return {"success": True}
