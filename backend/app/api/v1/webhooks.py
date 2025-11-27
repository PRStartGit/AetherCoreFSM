"""
Webhook handlers for external service integrations.
"""
from fastapi import APIRouter, Request, HTTPException, Depends, Header
from sqlalchemy.orm import Session
import hmac
import hashlib
import json
from typing import Optional

from app.core.database import get_db
from app.core.config import settings
from app.models.organization import Organization

router = APIRouter()


def verify_gocardless_signature(
    body: bytes,
    signature: str,
    secret: str
) -> bool:
    """Verify GoCardless webhook signature."""
    expected = hmac.new(
        secret.encode(),
        body,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


@router.post("/gocardless")
async def gocardless_webhook(
    request: Request,
    db: Session = Depends(get_db),
    webhook_signature: Optional[str] = Header(None, alias="Webhook-Signature")
):
    """
    Handle GoCardless webhook events.
    
    Events handled:
    - payments: confirmed, failed, cancelled
    - mandates: created, cancelled, failed
    - subscriptions: created, cancelled, finished
    """
    body = await request.body()
    
    # Verify signature if webhook secret is configured
    if settings.GOCARDLESS_WEBHOOK_SECRET:
        if not webhook_signature:
            raise HTTPException(status_code=401, detail="Missing webhook signature")
        
        if not verify_gocardless_signature(body, webhook_signature, settings.GOCARDLESS_WEBHOOK_SECRET):
            raise HTTPException(status_code=401, detail="Invalid webhook signature")
    
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    events = payload.get("events", [])
    
    for event in events:
        event_type = event.get("resource_type")
        action = event.get("action")
        links = event.get("links", {})
        
        # Handle payment events
        if event_type == "payments":
            await handle_payment_event(action, links, event, db)
        
        # Handle mandate events
        elif event_type == "mandates":
            await handle_mandate_event(action, links, event, db)
        
        # Handle subscription events
        elif event_type == "subscriptions":
            await handle_subscription_event(action, links, event, db)
    
    return {"status": "ok", "events_processed": len(events)}


async def handle_payment_event(action: str, links: dict, event: dict, db: Session):
    """Handle payment-related webhook events."""
    subscription_id = links.get("subscription")
    
    if not subscription_id:
        return
    
    # Find organization by subscription ID
    org = db.query(Organization).filter(
        Organization.gocardless_subscription_id == subscription_id
    ).first()
    
    if not org:
        return
    
    if action == "confirmed":
        # Payment successful - ensure subscription is active
        org.is_trial = False
        db.commit()
        print(f"Payment confirmed for org {org.id}")
    
    elif action == "failed":
        # Payment failed - may need to notify admin
        print(f"Payment failed for org {org.id}")
    
    elif action == "cancelled":
        print(f"Payment cancelled for org {org.id}")


async def handle_mandate_event(action: str, links: dict, event: dict, db: Session):
    """Handle mandate-related webhook events."""
    mandate_id = links.get("mandate")
    customer_id = links.get("customer")
    
    if action == "created":
        # Mandate created - customer has authorized Direct Debit
        print(f"Mandate created: {mandate_id} for customer {customer_id}")
    
    elif action == "cancelled" or action == "failed":
        # Mandate cancelled - find and update organization
        org = db.query(Organization).filter(
            Organization.gocardless_mandate_id == mandate_id
        ).first()
        
        if org:
            org.gocardless_mandate_id = None
            org.gocardless_subscription_id = None
            db.commit()
            print(f"Mandate {action} for org {org.id}")


async def handle_subscription_event(action: str, links: dict, event: dict, db: Session):
    """Handle subscription-related webhook events."""
    subscription_id = links.get("subscription")
    
    org = db.query(Organization).filter(
        Organization.gocardless_subscription_id == subscription_id
    ).first()
    
    if not org:
        return
    
    if action == "created":
        print(f"Subscription created for org {org.id}")
    
    elif action == "cancelled" or action == "finished":
        org.gocardless_subscription_id = None
        # Optionally downgrade to free tier
        db.commit()
        print(f"Subscription {action} for org {org.id}")
