"""
Ticket API endpoints for support ticket system
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
import uuid

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User, UserRole
from app.models.ticket import Ticket, TicketMessage, TicketStatus, TicketPriority, TicketType
from app.core.email import email_service

router = APIRouter()


# Pydantic schemas
class TicketCreate(BaseModel):
    subject: str
    description: str
    ticket_type: TicketType = TicketType.GENERAL
    priority: TicketPriority = TicketPriority.MEDIUM


class TicketUpdate(BaseModel):
    status: Optional[TicketStatus] = None
    priority: Optional[TicketPriority] = None
    assigned_to_user_id: Optional[int] = None


class TicketMessageCreate(BaseModel):
    message: str
    is_internal_note: bool = False


class TicketMessageResponse(BaseModel):
    id: int
    ticket_id: int
    user_id: int
    user_name: str
    user_role: str
    message: str
    is_internal_note: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TicketResponse(BaseModel):
    id: int
    ticket_number: str
    subject: str
    description: str
    status: TicketStatus
    priority: TicketPriority
    ticket_type: TicketType
    created_by_user_id: int
    created_by_user_name: str
    organization_id: Optional[int]
    organization_name: Optional[str]
    assigned_to_user_id: Optional[int]
    assigned_to_user_name: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    resolved_at: Optional[datetime]
    closed_at: Optional[datetime]
    message_count: int

    class Config:
        from_attributes = True


class TicketDetailResponse(TicketResponse):
    messages: List[TicketMessageResponse]


def generate_ticket_number():
    """Generate unique ticket number like TKT-ABC123"""
    return f"TKT-{uuid.uuid4().hex[:6].upper()}"


def can_view_ticket(user: User, ticket: Ticket) -> bool:
    """Check if user can view a ticket"""
    if user.role == UserRole.SUPER_ADMIN:
        return True
    # Users can view their own tickets
    if ticket.created_by_user_id == user.id:
        return True
    # Org admins can view tickets from their organization
    if user.role == UserRole.ORG_ADMIN and ticket.organization_id == user.organization_id:
        return True
    return False


def can_respond_to_ticket(user: User) -> bool:
    """Check if user can respond to tickets as support"""
    return user.role == UserRole.SUPER_ADMIN


@router.post("", response_model=TicketResponse)
def create_ticket(
    ticket_data: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new support ticket"""
    ticket = Ticket(
        ticket_number=generate_ticket_number(),
        subject=ticket_data.subject,
        description=ticket_data.description,
        ticket_type=ticket_data.ticket_type,
        priority=ticket_data.priority,
        created_by_user_id=current_user.id,
        organization_id=current_user.organization_id,
        status=TicketStatus.OPEN
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    # Send email notification to support
    try:
        email_service.send_email_sendgrid(
            to_email="hello@zynthio.co.uk",
            subject=f"[New Ticket] {ticket.ticket_number}: {ticket.subject}",
            html_content=f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <h2 style="color: #0EA5E9;">New Support Ticket</h2>
                <p><strong>Ticket Number:</strong> {ticket.ticket_number}</p>
                <p><strong>Type:</strong> {ticket.ticket_type.value.replace('_', ' ').title()}</p>
                <p><strong>Priority:</strong> {ticket.priority.value.title()}</p>
                <p><strong>Subject:</strong> {ticket.subject}</p>
                <hr style="border: 1px solid #eee;">
                <h3>Description</h3>
                <p>{ticket.description}</p>
                <hr style="border: 1px solid #eee;">
                <p><strong>Submitted by:</strong> {current_user.full_name} ({current_user.email})</p>
                <p><strong>Organization:</strong> {current_user.organization.name if current_user.organization else 'N/A'}</p>
                <p style="color: #666; font-size: 12px;">Submitted at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
            </body>
            </html>
            """,
            to_name="Zynthio Support"
        )
    except Exception as e:
        print(f"Failed to send ticket notification email: {e}")

    return _ticket_to_response(ticket)


@router.get("", response_model=List[TicketResponse])
def list_tickets(
    status: Optional[TicketStatus] = None,
    ticket_type: Optional[TicketType] = None,
    priority: Optional[TicketPriority] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List tickets based on user role"""
    query = db.query(Ticket)

    # Filter based on user role
    if current_user.role == UserRole.SUPER_ADMIN:
        # Super admin sees all tickets
        pass
    elif current_user.role == UserRole.ORG_ADMIN:
        # Org admin sees their own tickets and their org's tickets
        query = query.filter(
            or_(
                Ticket.created_by_user_id == current_user.id,
                Ticket.organization_id == current_user.organization_id
            )
        )
    else:
        # Site users see only their own tickets
        query = query.filter(Ticket.created_by_user_id == current_user.id)

    # Apply filters
    if status:
        query = query.filter(Ticket.status == status)
    if ticket_type:
        query = query.filter(Ticket.ticket_type == ticket_type)
    if priority:
        query = query.filter(Ticket.priority == priority)

    tickets = query.order_by(Ticket.created_at.desc()).all()
    return [_ticket_to_response(t) for t in tickets]


@router.get("/stats")
def get_ticket_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get ticket statistics for dashboard"""
    query = db.query(Ticket)

    # Filter based on role
    if current_user.role != UserRole.SUPER_ADMIN:
        query = query.filter(Ticket.created_by_user_id == current_user.id)

    tickets = query.all()

    stats = {
        "total": len(tickets),
        "open": sum(1 for t in tickets if t.status == TicketStatus.OPEN),
        "in_progress": sum(1 for t in tickets if t.status == TicketStatus.IN_PROGRESS),
        "resolved": sum(1 for t in tickets if t.status == TicketStatus.RESOLVED),
        "closed": sum(1 for t in tickets if t.status == TicketStatus.CLOSED)
    }
    return stats


@router.get("/{ticket_id}", response_model=TicketDetailResponse)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get ticket details with messages"""
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if not can_view_ticket(current_user, ticket):
        raise HTTPException(status_code=403, detail="Not authorized to view this ticket")

    return _ticket_to_detail_response(ticket, current_user)


@router.patch("/{ticket_id}", response_model=TicketResponse)
def update_ticket(
    ticket_id: int,
    ticket_data: TicketUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update ticket status/priority/assignment (support only)"""
    if not can_respond_to_ticket(current_user):
        raise HTTPException(status_code=403, detail="Only support staff can update tickets")

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    old_status = ticket.status

    if ticket_data.status is not None:
        ticket.status = ticket_data.status
        if ticket_data.status == TicketStatus.RESOLVED:
            ticket.resolved_at = datetime.utcnow()
        elif ticket_data.status == TicketStatus.CLOSED:
            ticket.closed_at = datetime.utcnow()

    if ticket_data.priority is not None:
        ticket.priority = ticket_data.priority

    if ticket_data.assigned_to_user_id is not None:
        ticket.assigned_to_user_id = ticket_data.assigned_to_user_id

    ticket.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(ticket)

    # Notify user of status change
    if ticket_data.status and ticket_data.status != old_status:
        try:
            email_service.send_email_sendgrid(
                to_email=ticket.created_by_user.email,
                subject=f"[Ticket Update] {ticket.ticket_number}: Status changed to {ticket.status.value.replace('_', ' ').title()}",
                html_content=f"""
                <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <h2 style="color: #0EA5E9;">Ticket Status Update</h2>
                    <p><strong>Ticket Number:</strong> {ticket.ticket_number}</p>
                    <p><strong>Subject:</strong> {ticket.subject}</p>
                    <p><strong>New Status:</strong> {ticket.status.value.replace('_', ' ').title()}</p>
                    <hr style="border: 1px solid #eee;">
                    <p>You can view your ticket at <a href="https://zynthio.co.uk/support/tickets/{ticket.id}">zynthio.co.uk</a></p>
                    <p>Best regards,<br>Zynthio Support Team</p>
                </body>
                </html>
                """,
                to_name=ticket.created_by_user.full_name
            )
        except Exception as e:
            print(f"Failed to send status update email: {e}")

    return _ticket_to_response(ticket)


@router.post("/{ticket_id}/messages", response_model=TicketMessageResponse)
def add_message(
    ticket_id: int,
    message_data: TicketMessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a message/reply to a ticket"""
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if not can_view_ticket(current_user, ticket):
        raise HTTPException(status_code=403, detail="Not authorized to reply to this ticket")

    # Only support can add internal notes
    if message_data.is_internal_note and not can_respond_to_ticket(current_user):
        raise HTTPException(status_code=403, detail="Only support staff can add internal notes")

    message = TicketMessage(
        ticket_id=ticket.id,
        user_id=current_user.id,
        message=message_data.message,
        is_internal_note=1 if message_data.is_internal_note else 0
    )
    db.add(message)

    # Update ticket timestamp
    ticket.updated_at = datetime.utcnow()

    # If support is responding and ticket is open, set to in progress
    if can_respond_to_ticket(current_user) and ticket.status == TicketStatus.OPEN:
        ticket.status = TicketStatus.IN_PROGRESS

    db.commit()
    db.refresh(message)

    # Send email notification
    if not message_data.is_internal_note:
        try:
            # If support is replying, notify user
            if can_respond_to_ticket(current_user):
                email_service.send_email_sendgrid(
                    to_email=ticket.created_by_user.email,
                    subject=f"[Ticket Reply] {ticket.ticket_number}: {ticket.subject}",
                    html_content=f"""
                    <html>
                    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                        <h2 style="color: #0EA5E9;">New Reply on Your Ticket</h2>
                        <p><strong>Ticket Number:</strong> {ticket.ticket_number}</p>
                        <p><strong>Subject:</strong> {ticket.subject}</p>
                        <hr style="border: 1px solid #eee;">
                        <h3>Reply from Support</h3>
                        <p>{message_data.message}</p>
                        <hr style="border: 1px solid #eee;">
                        <p>You can view and reply to this ticket at <a href="https://zynthio.co.uk/support/tickets/{ticket.id}">zynthio.co.uk</a></p>
                        <p>Best regards,<br>Zynthio Support Team</p>
                    </body>
                    </html>
                    """,
                    to_name=ticket.created_by_user.full_name
                )
            # If user is replying, notify support
            else:
                email_service.send_email_sendgrid(
                    to_email="hello@zynthio.co.uk",
                    subject=f"[Ticket Reply] {ticket.ticket_number}: New message from {current_user.full_name}",
                    html_content=f"""
                    <html>
                    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                        <h2 style="color: #0EA5E9;">New Reply on Ticket</h2>
                        <p><strong>Ticket Number:</strong> {ticket.ticket_number}</p>
                        <p><strong>Subject:</strong> {ticket.subject}</p>
                        <p><strong>From:</strong> {current_user.full_name} ({current_user.email})</p>
                        <hr style="border: 1px solid #eee;">
                        <h3>Message</h3>
                        <p>{message_data.message}</p>
                        <hr style="border: 1px solid #eee;">
                        <p style="color: #666; font-size: 12px;">Submitted at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
                    </body>
                    </html>
                    """,
                    to_name="Zynthio Support"
                )
        except Exception as e:
            print(f"Failed to send reply notification email: {e}")

    return _message_to_response(message)


@router.post("/{ticket_id}/close", response_model=TicketResponse)
def close_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Close a ticket (ticket owner or support)"""
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Only ticket owner or support can close
    if ticket.created_by_user_id != current_user.id and not can_respond_to_ticket(current_user):
        raise HTTPException(status_code=403, detail="Not authorized to close this ticket")

    ticket.status = TicketStatus.CLOSED
    ticket.closed_at = datetime.utcnow()
    ticket.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(ticket)

    return _ticket_to_response(ticket)


@router.post("/{ticket_id}/reopen", response_model=TicketResponse)
def reopen_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Reopen a closed ticket"""
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if not can_view_ticket(current_user, ticket):
        raise HTTPException(status_code=403, detail="Not authorized to reopen this ticket")

    if ticket.status != TicketStatus.CLOSED:
        raise HTTPException(status_code=400, detail="Only closed tickets can be reopened")

    ticket.status = TicketStatus.OPEN
    ticket.closed_at = None
    ticket.resolved_at = None
    ticket.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(ticket)

    # Notify support of reopened ticket
    try:
        email_service.send_email_sendgrid(
            to_email="hello@zynthio.co.uk",
            subject=f"[Ticket Reopened] {ticket.ticket_number}: {ticket.subject}",
            html_content=f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <h2 style="color: #0EA5E9;">Ticket Reopened</h2>
                <p><strong>Ticket Number:</strong> {ticket.ticket_number}</p>
                <p><strong>Subject:</strong> {ticket.subject}</p>
                <p><strong>Reopened by:</strong> {current_user.full_name} ({current_user.email})</p>
                <hr style="border: 1px solid #eee;">
                <p style="color: #666; font-size: 12px;">Reopened at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
            </body>
            </html>
            """,
            to_name="Zynthio Support"
        )
    except Exception as e:
        print(f"Failed to send reopen notification email: {e}")

    return _ticket_to_response(ticket)


def _ticket_to_response(ticket: Ticket) -> TicketResponse:
    """Convert ticket model to response"""
    return TicketResponse(
        id=ticket.id,
        ticket_number=ticket.ticket_number,
        subject=ticket.subject,
        description=ticket.description,
        status=ticket.status,
        priority=ticket.priority,
        ticket_type=ticket.ticket_type,
        created_by_user_id=ticket.created_by_user_id,
        created_by_user_name=ticket.created_by_user.full_name if ticket.created_by_user else "Unknown",
        organization_id=ticket.organization_id,
        organization_name=ticket.organization.name if ticket.organization else None,
        assigned_to_user_id=ticket.assigned_to_user_id,
        assigned_to_user_name=ticket.assigned_to_user.full_name if ticket.assigned_to_user else None,
        created_at=ticket.created_at,
        updated_at=ticket.updated_at,
        resolved_at=ticket.resolved_at,
        closed_at=ticket.closed_at,
        message_count=len(ticket.messages) if ticket.messages else 0
    )


def _ticket_to_detail_response(ticket: Ticket, current_user: User) -> TicketDetailResponse:
    """Convert ticket model to detail response with messages"""
    messages = ticket.messages or []

    # Filter out internal notes for non-support users
    if not can_respond_to_ticket(current_user):
        messages = [m for m in messages if not m.is_internal_note]

    return TicketDetailResponse(
        id=ticket.id,
        ticket_number=ticket.ticket_number,
        subject=ticket.subject,
        description=ticket.description,
        status=ticket.status,
        priority=ticket.priority,
        ticket_type=ticket.ticket_type,
        created_by_user_id=ticket.created_by_user_id,
        created_by_user_name=ticket.created_by_user.full_name if ticket.created_by_user else "Unknown",
        organization_id=ticket.organization_id,
        organization_name=ticket.organization.name if ticket.organization else None,
        assigned_to_user_id=ticket.assigned_to_user_id,
        assigned_to_user_name=ticket.assigned_to_user.full_name if ticket.assigned_to_user else None,
        created_at=ticket.created_at,
        updated_at=ticket.updated_at,
        resolved_at=ticket.resolved_at,
        closed_at=ticket.closed_at,
        message_count=len(ticket.messages) if ticket.messages else 0,
        messages=[_message_to_response(m) for m in messages]
    )


def _message_to_response(message: TicketMessage) -> TicketMessageResponse:
    """Convert message model to response"""
    return TicketMessageResponse(
        id=message.id,
        ticket_id=message.ticket_id,
        user_id=message.user_id,
        user_name=message.user.full_name if message.user else "Unknown",
        user_role=message.user.role.value if message.user else "unknown",
        message=message.message,
        is_internal_note=bool(message.is_internal_note),
        created_at=message.created_at
    )
