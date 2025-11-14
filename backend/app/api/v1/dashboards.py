from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_super_admin
from app.models.user import User, UserRole
from app.models.organization import Organization
from app.models.site import Site
from app.models.checklist import Checklist, ChecklistStatus
from app.models.defect import Defect, DefectStatus
from app.schemas.dashboard import SuperAdminDashboard, OrgAdminDashboard, SiteUserDashboard, RAGStatus
from app.services.rag_service import calculate_site_rag_status, get_organization_rag_summary

router = APIRouter()


@router.get("/dashboards/super-admin", response_model=SuperAdminDashboard)
def get_super_admin_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Get super admin dashboard with platform-wide metrics."""
    # Count totals
    total_orgs = db.query(Organization).filter(Organization.is_active == True).count()
    total_sites = db.query(Site).filter(Site.is_active == True).count()
    total_users = db.query(User).filter(User.is_active == True).count()

    # Active checklists (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    total_active_checklists = db.query(Checklist).filter(
        Checklist.created_at >= thirty_days_ago
    ).count()

    # Open defects
    total_open_defects = db.query(Defect).filter(
        Defect.status == DefectStatus.OPEN
    ).count()

    # Subscription summary
    subscription_summary = {
        "basic": db.query(Organization).filter(Organization.subscription_tier == "basic").count(),
        "professional": db.query(Organization).filter(Organization.subscription_tier == "professional").count(),
        "enterprise": db.query(Organization).filter(Organization.subscription_tier == "enterprise").count(),
        "trial": db.query(Organization).filter(Organization.is_trial == True).count()
    }

    # Recent activity (last 10 completed checklists)
    recent_checklists = db.query(Checklist).filter(
        Checklist.status == ChecklistStatus.COMPLETED
    ).order_by(Checklist.completed_at.desc()).limit(10).all()

    recent_activity = []
    for checklist in recent_checklists:
        recent_activity.append({
            "type": "checklist_completed",
            "site_name": checklist.site.name,
            "organization_name": checklist.site.organization.name,
            "date": checklist.completed_at.isoformat() if checklist.completed_at else None
        })

    return SuperAdminDashboard(
        total_organizations=total_orgs,
        total_sites=total_sites,
        total_users=total_users,
        total_active_checklists=total_active_checklists,
        total_open_defects=total_open_defects,
        subscription_summary=subscription_summary,
        recent_activity=recent_activity
    )


@router.get("/dashboards/org-admin", response_model=OrgAdminDashboard)
def get_org_admin_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get organization admin dashboard."""
    if current_user.role == UserRole.SITE_USER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    org_id = current_user.organization_id
    organization = db.query(Organization).filter(Organization.id == org_id).first()

    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )

    # Get totals
    total_sites = db.query(Site).filter(
        Site.organization_id == org_id,
        Site.is_active == True
    ).count()

    total_users = db.query(User).filter(
        User.organization_id == org_id,
        User.is_active == True
    ).count()

    # Get RAG summary
    rag_summary = get_organization_rag_summary(org_id, db)

    # Overdue checklists (pending status and past date)
    overdue_checklists = db.query(Checklist).join(Site).filter(
        Site.organization_id == org_id,
        Checklist.status == ChecklistStatus.PENDING,
        Checklist.checklist_date < datetime.utcnow().date()
    ).count()

    # Site performance
    sites = db.query(Site).filter(
        Site.organization_id == org_id,
        Site.is_active == True
    ).all()

    site_performance = []
    for site in sites:
        rag_data = calculate_site_rag_status(site.id, db)
        site_performance.append({
            "site_id": site.id,
            "site_name": site.name,
            "rag_status": rag_data["rag_status"],
            "completion_rate": rag_data["completion_rate"],
            "open_defects": rag_data["open_defects"]
        })

    # Recent activity
    recent_checklists = db.query(Checklist).join(Site).filter(
        Site.organization_id == org_id,
        Checklist.status == ChecklistStatus.COMPLETED
    ).order_by(Checklist.completed_at.desc()).limit(10).all()

    recent_activity = []
    for checklist in recent_checklists:
        recent_activity.append({
            "type": "checklist_completed",
            "site_name": checklist.site.name,
            "date": checklist.completed_at.isoformat() if checklist.completed_at else None
        })

    return OrgAdminDashboard(
        organization_name=organization.name,
        total_sites=total_sites,
        total_users=total_users,
        overall_rag_status=rag_summary["overall_rag"],
        completion_rate=rag_summary["average_completion_rate"],
        open_defects_count=rag_summary["total_open_defects"],
        overdue_checklists=overdue_checklists,
        site_performance=site_performance,
        recent_activity=recent_activity
    )


@router.get("/dashboards/site-user", response_model=SiteUserDashboard)
def get_site_user_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get site user dashboard."""
    from app.models.user_site import UserSite

    # Get user's assigned site IDs
    assigned_site_ids = [us.site_id for us in current_user.user_sites]

    # Get user's assigned sites
    assigned_sites = []
    for user_site in current_user.user_sites:
        site = user_site.site
        rag_data = calculate_site_rag_status(site.id, db)
        assigned_sites.append({
            "site_id": site.id,
            "site_name": site.name,
            "rag_status": rag_data["rag_status"]
        })

    # Today's checklists (only for assigned sites)
    today = datetime.utcnow().date()
    todays_checklists_query = db.query(Checklist).filter(
        Checklist.checklist_date == today,
        Checklist.site_id.in_(assigned_site_ids)
    )

    todays_checklists = []
    for checklist in todays_checklists_query.all():
        todays_checklists.append({
            "checklist_id": checklist.id,
            "site_name": checklist.site.name,
            "status": checklist.status.value,
            "completion_percentage": checklist.completion_percentage
        })

    # Assigned checklists (pending) - only for assigned sites
    assigned_checklists_query = db.query(Checklist).filter(
        Checklist.site_id.in_(assigned_site_ids),
        Checklist.status.in_([ChecklistStatus.PENDING, ChecklistStatus.IN_PROGRESS])
    ).order_by(Checklist.checklist_date.desc()).limit(20)

    assigned_checklists = []
    for checklist in assigned_checklists_query.all():
        assigned_checklists.append({
            "checklist_id": checklist.id,
            "site_name": checklist.site.name,
            "checklist_date": checklist.checklist_date.isoformat(),
            "status": checklist.status.value,
            "completion_percentage": checklist.completion_percentage
        })

    # Open defects - only for assigned sites
    open_defects_query = db.query(Defect).filter(
        Defect.site_id.in_(assigned_site_ids),
        Defect.status == DefectStatus.OPEN
    ).order_by(Defect.created_at.desc()).limit(20)

    open_defects = []
    for defect in open_defects_query.all():
        open_defects.append({
            "defect_id": defect.id,
            "title": defect.title,
            "site_name": defect.site.name,
            "severity": defect.severity.value,
            "created_at": defect.created_at.isoformat()
        })

    # Recent completed - only for assigned sites
    recent_completed_query = db.query(Checklist).filter(
        Checklist.site_id.in_(assigned_site_ids),
        Checklist.status == ChecklistStatus.COMPLETED
    ).order_by(Checklist.completed_at.desc()).limit(10)

    recent_completed = []
    for checklist in recent_completed_query.all():
        recent_completed.append({
            "checklist_id": checklist.id,
            "site_name": checklist.site.name,
            "completed_at": checklist.completed_at.isoformat() if checklist.completed_at else None
        })

    return SiteUserDashboard(
        assigned_sites=assigned_sites,
        todays_checklists=todays_checklists,
        assigned_checklists=assigned_checklists,
        open_defects=open_defects,
        recent_completed=recent_completed
    )


@router.get("/sites/{site_id}/rag-status", response_model=RAGStatus)
def get_site_rag_status(
    site_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get RAG status for a specific site."""
    site = db.query(Site).filter(Site.id == site_id).first()

    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found"
        )

    # Check permissions
    if current_user.role != UserRole.SUPER_ADMIN:
        if current_user.organization_id != site.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

    rag_data = calculate_site_rag_status(site_id, db)

    return RAGStatus(
        site_id=site.id,
        site_name=site.name,
        rag_status=rag_data["rag_status"],
        completion_rate=rag_data["completion_rate"],
        open_defects=rag_data["open_defects"],
        overdue_defects=rag_data["overdue_defects"],
        last_30_days_completion=rag_data["completion_rate"]
    )
