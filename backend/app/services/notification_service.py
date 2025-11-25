"""
Notification service for creating and managing user notifications
"""
from sqlalchemy.orm import Session
from typing import List
from app.models.notification import Notification
from app.models.user import User, UserRole


class NotificationService:
    """Service for managing user notifications"""

    @staticmethod
    def create_notification(
        db: Session,
        user_id: int,
        title: str,
        message: str,
        notification_type: str,
        related_id: int = None,
        related_url: str = None
    ) -> Notification:
        """Create a single notification for a user"""
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            related_id=related_id,
            related_url=related_url
        )
        db.add(notification)
        return notification

    @staticmethod
    def create_notifications_for_users(
        db: Session,
        user_ids: List[int],
        title: str,
        message: str,
        notification_type: str,
        related_id: int = None,
        related_url: str = None
    ) -> List[Notification]:
        """Create notifications for multiple users"""
        notifications = []
        for user_id in user_ids:
            notification = NotificationService.create_notification(
                db=db,
                user_id=user_id,
                title=title,
                message=message,
                notification_type=notification_type,
                related_id=related_id,
                related_url=related_url
            )
            notifications.append(notification)
        return notifications

    @staticmethod
    def notify_all_super_admins(
        db: Session,
        title: str,
        message: str,
        notification_type: str,
        related_id: int = None,
        related_url: str = None
    ) -> List[Notification]:
        """Create notifications for all super admin users"""
        super_admins = db.query(User).filter(User.role == UserRole.SUPER_ADMIN).all()
        super_admin_ids = [admin.id for admin in super_admins]

        return NotificationService.create_notifications_for_users(
            db=db,
            user_ids=super_admin_ids,
            title=title,
            message=message,
            notification_type=notification_type,
            related_id=related_id,
            related_url=related_url
        )

    @staticmethod
    def notify_ticket_new(db: Session, ticket_number: str, subject: str, ticket_id: int):
        """Notify all super admins of a new ticket"""
        return NotificationService.notify_all_super_admins(
            db=db,
            title=f"New Support Ticket: {ticket_number}",
            message=f"New ticket created: {subject}",
            notification_type="ticket_new",
            related_id=ticket_id,
            related_url=f"/super-admin/tickets/{ticket_id}"
        )

    @staticmethod
    def notify_ticket_reply(
        db: Session,
        user_id: int,
        ticket_number: str,
        subject: str,
        ticket_id: int,
        from_support: bool = False
    ):
        """Notify user of a new ticket reply"""
        if from_support:
            title = f"Support Reply: {ticket_number}"
            message = f"Support has replied to your ticket: {subject}"
        else:
            title = f"New Reply: {ticket_number}"
            message = f"New reply added to ticket: {subject}"

        return NotificationService.create_notification(
            db=db,
            user_id=user_id,
            title=title,
            message=message,
            notification_type="ticket_reply",
            related_id=ticket_id,
            related_url=f"/support/tickets/{ticket_id}"
        )

    @staticmethod
    def notify_ticket_status_change(
        db: Session,
        user_id: int,
        ticket_number: str,
        subject: str,
        new_status: str,
        ticket_id: int
    ):
        """Notify user of ticket status change"""
        return NotificationService.create_notification(
            db=db,
            user_id=user_id,
            title=f"Ticket Status Updated: {ticket_number}",
            message=f"Your ticket status changed to: {new_status}. Subject: {subject}",
            notification_type="ticket_status",
            related_id=ticket_id,
            related_url=f"/support/tickets/{ticket_id}"
        )


# Singleton instance
notification_service = NotificationService()
