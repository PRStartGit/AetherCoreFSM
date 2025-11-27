"""
GoCardless Integration Service
"""
import gocardless_pro
from typing import Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.organization import Organization


class GoCardlessService:
    """Service for interacting with GoCardless API."""
    
    def __init__(self):
        if not settings.GOCARDLESS_ACCESS_TOKEN:
            raise ValueError("GOCARDLESS_ACCESS_TOKEN not configured")
        
        self.client = gocardless_pro.Client(
            access_token=settings.GOCARDLESS_ACCESS_TOKEN,
            environment=settings.GOCARDLESS_ENVIRONMENT
        )
    
    def create_redirect_flow(
        self,
        organization: Organization,
        session_token: str,
        description: str = "Zynthio Subscription"
    ) -> Dict[str, Any]:
        """Create a redirect flow for setting up a Direct Debit mandate."""
        redirect_flow = self.client.redirect_flows.create(
            params={
                "description": description,
                "session_token": session_token,
                "success_redirect_url": settings.GOCARDLESS_SUCCESS_REDIRECT_URL,
                "scheme": "bacs",
                "metadata": {
                    "organization_id": str(organization.id),
                    "org_name": organization.name
                }
            }
        )
        
        return {
            "redirect_flow_id": redirect_flow.id,
            "redirect_url": redirect_flow.redirect_url
        }
    
    def complete_redirect_flow(
        self,
        redirect_flow_id: str,
        session_token: str
    ) -> Dict[str, Any]:
        """Complete a redirect flow after customer returns from GoCardless."""
        completed_flow = self.client.redirect_flows.complete(
            redirect_flow_id,
            params={"session_token": session_token}
        )
        
        return {
            "customer_id": completed_flow.links.customer,
            "mandate_id": completed_flow.links.mandate,
            "confirmation_url": completed_flow.confirmation_url
        }
    
    def create_subscription(
        self,
        mandate_id: str,
        amount_pence: int,
        name: str,
        interval_unit: str = "monthly",
        day_of_month: int = 1,
        metadata: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Create a subscription for recurring payments."""
        subscription = self.client.subscriptions.create(
            params={
                "amount": str(amount_pence),
                "currency": "GBP",
                "name": name,
                "interval_unit": interval_unit,
                "day_of_month": str(day_of_month),
                "metadata": metadata or {},
                "links": {"mandate": mandate_id}
            }
        )
        
        return {
            "subscription_id": subscription.id,
            "status": subscription.status,
            "amount": subscription.amount,
            "start_date": subscription.start_date
        }
    
    def cancel_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """Cancel a subscription."""
        subscription = self.client.subscriptions.cancel(subscription_id)
        return {"subscription_id": subscription.id, "status": subscription.status}
    
    def get_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """Get subscription details."""
        subscription = self.client.subscriptions.get(subscription_id)
        return {
            "subscription_id": subscription.id,
            "status": subscription.status,
            "amount": subscription.amount,
            "interval_unit": subscription.interval_unit
        }
    
    def list_payments(self, subscription_id: Optional[str] = None, limit: int = 50) -> list:
        """List payments."""
        params = {"limit": limit}
        if subscription_id:
            params["subscription"] = subscription_id
        payments = self.client.payments.list(params=params)
        return [{"payment_id": p.id, "amount": p.amount, "status": p.status} for p in payments.records]


_gocardless_service: Optional[GoCardlessService] = None


def get_gocardless_service() -> GoCardlessService:
    """Get the GoCardless service singleton."""
    global _gocardless_service
    if _gocardless_service is None:
        _gocardless_service = GoCardlessService()
    return _gocardless_service
