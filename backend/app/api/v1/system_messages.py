from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List
from datetime import datetime
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.system_message import SystemMessage, MessageDismissal, VisibilityScope
from app.models.user import User, UserRole
from app.schemas.system_message import (
    SystemMessageCreate,
    SystemMessageResponse,
    SystemMessageList,
    VisibilityScopeEnum
)

router = APIRouter()


def can_create_message(user: User) -> bool:
    """Check if user can create system messages"""
    return user.role in [UserRole.SUPER_ADMIN, UserRole.ORG_ADMIN]


def get_user_messages_query(db: Session, user: User):
    """Build query for messages visible to a specific user"""
    now = datetime.utcnow()
    base_query = db.query(SystemMessage).filter(
        SystemMessage.is_active == True,
        SystemMessage.expiry_date > now
    )

    if user.role == UserRole.SUPER_ADMIN:
        # Super admin sees all messages
        return base_query

    elif user.role == UserRole.ORG_ADMIN:
        # Org admin sees:
        # 1. Global messages for org_admins or both
        # 2. Organization-specific messages for their org
        return base_query.filter(
            or_(
                # Global super admin messages for org admins
                and_(
                    SystemMessage.organization_id.is_(None),
                    SystemMessage.visibility_scope.in_([
                        VisibilityScope.ORG_ADMINS_ONLY.value,
                        VisibilityScope.BOTH.value
                    ])
                ),
                # Org-specific messages for their organization
                SystemMessage.organization_id == user.organization_id
            )
        )

    else:  # Site user
        # Site user sees:
        # 1. Global messages for site_users or both
        # 2. Organization-specific messages for their org
        return base_query.filter(
            or_(
                # Global super admin messages for site users
                and_(
                    SystemMessage.organization_id.is_(None),
                    SystemMessage.visibility_scope.in_([
                        VisibilityScope.SITE_USERS_ONLY.value,
                        VisibilityScope.BOTH.value
                    ])
                ),
                # Org-specific messages for their organization
                SystemMessage.organization_id == user.organization_id
            )
        )


@router.get("/system-messages", response_model=List[SystemMessageResponse])
def list_system_messages(
    include_dismissed: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all system messages visible to the current user"""
    query = get_user_messages_query(db, current_user)

    if not include_dismissed:
        # Exclude dismissed messages
        dismissed_ids = db.query(MessageDismissal.message_id).filter(
            MessageDismissal.user_id == current_user.id
        ).subquery()
        query = query.filter(~SystemMessage.id.in_(dismissed_ids))

    messages = query.order_by(SystemMessage.created_at.desc()).all()

    result = []
    for msg in messages:
        result.append(SystemMessageResponse(
            id=msg.id,
            message_content=msg.message_content,
            created_by_user_id=msg.created_by_user_id,
            created_by_name=f"{msg.created_by.first_name} {msg.created_by.last_name}" if msg.created_by else None,
            organization_id=msg.organization_id,
            organization_name=msg.organization.company_name if msg.organization else None,
            visibility_scope=msg.visibility_scope,
            expiry_date=msg.expiry_date,
            is_active=msg.is_active,
            created_at=msg.created_at,
            is_super_admin_message=msg.organization_id is None
        ))

    return result


@router.get("/system-messages/active", response_model=List[SystemMessageResponse])
def get_active_messages(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get active (non-dismissed) system messages for notifications"""
    query = get_user_messages_query(db, current_user)

    # Exclude dismissed messages
    dismissed_ids = db.query(MessageDismissal.message_id).filter(
        MessageDismissal.user_id == current_user.id
    ).subquery()
    query = query.filter(~SystemMessage.id.in_(dismissed_ids))

    messages = query.order_by(SystemMessage.created_at.desc()).all()

    result = []
    for msg in messages:
        result.append(SystemMessageResponse(
            id=msg.id,
            message_content=msg.message_content,
            created_by_user_id=msg.created_by_user_id,
            created_by_name=f"{msg.created_by.first_name} {msg.created_by.last_name}" if msg.created_by else None,
            organization_id=msg.organization_id,
            organization_name=msg.organization.company_name if msg.organization else None,
            visibility_scope=msg.visibility_scope,
            expiry_date=msg.expiry_date,
            is_active=msg.is_active,
            created_at=msg.created_at,
            is_super_admin_message=msg.organization_id is None
        ))

    return result


@router.post("/system-messages", response_model=SystemMessageResponse, status_code=status.HTTP_201_CREATED)
def create_system_message(
    message_data: SystemMessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new system message (Super Admin or Org Admin only)"""
    if not can_create_message(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Super Admins and Org Admins can create system messages"
        )

    # Determine organization_id and visibility based on user role
    if current_user.role == UserRole.SUPER_ADMIN:
        organization_id = None  # Global message
        visibility_scope = message_data.visibility_scope.value
    else:  # Org Admin
        organization_id = current_user.organization_id
        visibility_scope = VisibilityScope.ORGANIZATION.value

    new_message = SystemMessage(
        message_content=message_data.message_content,
        created_by_user_id=current_user.id,
        organization_id=organization_id,
        visibility_scope=visibility_scope,
        expiry_date=message_data.expiry_date,
        is_active=True
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return SystemMessageResponse(
        id=new_message.id,
        message_content=new_message.message_content,
        created_by_user_id=new_message.created_by_user_id,
        created_by_name=f"{current_user.first_name} {current_user.last_name}",
        organization_id=new_message.organization_id,
        organization_name=current_user.organization.company_name if current_user.organization else None,
        visibility_scope=new_message.visibility_scope,
        expiry_date=new_message.expiry_date,
        is_active=new_message.is_active,
        created_at=new_message.created_at,
        is_super_admin_message=new_message.organization_id is None
    )


@router.post("/system-messages/{message_id}/dismiss", status_code=status.HTTP_200_OK)
def dismiss_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Dismiss a system message for the current user"""
    message = db.query(SystemMessage).filter(SystemMessage.id == message_id).first()

    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    # Check if already dismissed
    existing = db.query(MessageDismissal).filter(
        MessageDismissal.message_id == message_id,
        MessageDismissal.user_id == current_user.id
    ).first()

    if existing:
        return {"message": "Already dismissed"}

    dismissal = MessageDismissal(
        message_id=message_id,
        user_id=current_user.id
    )

    db.add(dismissal)
    db.commit()

    return {"message": "Message dismissed"}


@router.delete("/system-messages/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_system_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a system message (only creator or super admin)"""
    message = db.query(SystemMessage).filter(SystemMessage.id == message_id).first()

    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    # Check permissions
    if current_user.role != UserRole.SUPER_ADMIN and message.created_by_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own messages"
        )

    db.delete(message)
    db.commit()

    return None
