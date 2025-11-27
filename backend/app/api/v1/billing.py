"""
Billing API endpoints for subscription management.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import uuid

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.organization import Organization
from app.models.subscription_package import SubscriptionPackage
from app.services.gocardless_service import get_gocardless_service

router = APIRouter()


class CheckoutRequest(BaseModel):
    """Request to start checkout flow."""
    package_id: int
    billing_cycle: str = "monthly"  # monthly or annual


class CheckoutResponse(BaseModel):
    """Response with redirect URL for checkout."""
    redirect_url: str
    session_token: str


class CompleteCheckoutRequest(BaseModel):
    """Request to complete checkout after redirect."""
    redirect_flow_id: str
    session_token: str


@router.post("/checkout", response_model=CheckoutResponse)
def start_checkout(
    request: CheckoutRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Start a checkout flow to set up Direct Debit.
    
    Returns a redirect URL to send the user to GoCardless.
    """
    if not current_user.organization_id:
        raise HTTPException(status_code=400, detail="User has no organization")
    
    org = db.query(Organization).filter(
        Organization.id == current_user.organization_id
    ).first()
    
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    # Get the package
    package = db.query(SubscriptionPackage).filter(
        SubscriptionPackage.id == request.package_id
    ).first()
    
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    
    # Generate session token
    session_token = str(uuid.uuid4())
    
    try:
        gc_service = get_gocardless_service()
        result = gc_service.create_redirect_flow(
            organization=org,
            session_token=session_token,
            description=f"Zynthio {package.name} Subscription"
        )
        
        return CheckoutResponse(
            redirect_url=result["redirect_url"],
            session_token=session_token
        )
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create checkout: {str(e)}")


@router.post("/checkout/complete")
def complete_checkout(
    request: CompleteCheckoutRequest,
    package_id: int,
    billing_cycle: str = "monthly",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Complete checkout after customer returns from GoCardless.
    
    This sets up the mandate and creates the subscription.
    """
    if not current_user.organization_id:
        raise HTTPException(status_code=400, detail="User has no organization")
    
    org = db.query(Organization).filter(
        Organization.id == current_user.organization_id
    ).first()
    
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    package = db.query(SubscriptionPackage).filter(
        SubscriptionPackage.id == package_id
    ).first()
    
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    
    try:
        gc_service = get_gocardless_service()
        
        # Complete the redirect flow
        flow_result = gc_service.complete_redirect_flow(
            redirect_flow_id=request.redirect_flow_id,
            session_token=request.session_token
        )
        
        # Update organization with GoCardless IDs
        org.gocardless_customer_id = flow_result["customer_id"]
        org.gocardless_mandate_id = flow_result["mandate_id"]
        
        # Calculate amount in pence
        if billing_cycle == "annual" and package.annual_price:
            amount_pence = int(package.annual_price * 100)
            interval = "yearly"
        else:
            amount_pence = int(package.monthly_price * 100)
            interval = "monthly"
        
        # Create subscription
        sub_result = gc_service.create_subscription(
            mandate_id=flow_result["mandate_id"],
            amount_pence=amount_pence,
            name=f"Zynthio {package.name}",
            interval_unit=interval,
            metadata={
                "organization_id": str(org.id),
                "package_id": str(package.id),
                "billing_cycle": billing_cycle
            }
        )
        
        # Update organization
        org.gocardless_subscription_id = sub_result["subscription_id"]
        org.package_id = package.id
        org.is_trial = False
        
        db.commit()
        
        return {
            "success": True,
            "subscription_id": sub_result["subscription_id"],
            "package": package.name,
            "amount": amount_pence / 100,
            "interval": interval
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to complete checkout: {str(e)}")


@router.get("/subscription")
def get_subscription_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current subscription status for the organization."""
    if not current_user.organization_id:
        raise HTTPException(status_code=400, detail="User has no organization")
    
    org = db.query(Organization).filter(
        Organization.id == current_user.organization_id
    ).first()
    
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    package = None
    if org.package_id:
        package = db.query(SubscriptionPackage).filter(
            SubscriptionPackage.id == org.package_id
        ).first()
    
    return {
        "organization_id": org.id,
        "organization_name": org.name,
        "is_trial": org.is_trial,
        "has_mandate": bool(org.gocardless_mandate_id),
        "has_subscription": bool(org.gocardless_subscription_id),
        "package": {
            "id": package.id,
            "name": package.name,
            "code": package.code,
            "monthly_price": package.monthly_price,
            "annual_price": package.annual_price
        } if package else None
    }


@router.post("/subscription/cancel")
def cancel_subscription(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cancel the current subscription."""
    if not current_user.organization_id:
        raise HTTPException(status_code=400, detail="User has no organization")
    
    org = db.query(Organization).filter(
        Organization.id == current_user.organization_id
    ).first()
    
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    if not org.gocardless_subscription_id:
        raise HTTPException(status_code=400, detail="No active subscription")
    
    try:
        gc_service = get_gocardless_service()
        gc_service.cancel_subscription(org.gocardless_subscription_id)
        
        org.gocardless_subscription_id = None
        db.commit()
        
        return {"success": True, "message": "Subscription cancelled"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to cancel: {str(e)}")
