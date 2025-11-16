"""
RAG (Red/Amber/Green) Status Calculation Service

Rules:
- Green: 95%+ checklists completed in last 30 days, ≤2 overdue defects
- Amber: 90-94% completion OR 3-5 overdue defects
- Red: <90% completion OR >5 overdue defects
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.models.site import Site
from app.models.checklist import Checklist, ChecklistStatus
from app.models.defect import Defect, DefectStatus


def calculate_site_rag_status(site_id: int, db: Session) -> dict:
    """
    Calculate RAG status for a specific site.

    Returns:
        dict: {
            "rag_status": "green"|"amber"|"red",
            "completion_rate": float,
            "open_defects": int,
            "overdue_defects": int
        }
    """
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)

    # Get checklist completion rate (last 30 days)
    total_checklists = db.query(Checklist).filter(
        Checklist.site_id == site_id,
        Checklist.created_at >= thirty_days_ago
    ).count()

    completed_checklists = db.query(Checklist).filter(
        Checklist.site_id == site_id,
        Checklist.created_at >= thirty_days_ago,
        Checklist.status == ChecklistStatus.COMPLETED
    ).count()

    completion_rate = (completed_checklists / total_checklists * 100) if total_checklists > 0 else 100.0

    # Get open defects count
    open_defects = db.query(Defect).filter(
        Defect.site_id == site_id,
        Defect.status == DefectStatus.OPEN
    ).count()

    # Get overdue defects (open for more than 7 days)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    overdue_defects = db.query(Defect).filter(
        Defect.site_id == site_id,
        Defect.status == DefectStatus.OPEN,
        Defect.created_at < seven_days_ago
    ).count()

    # Calculate RAG status
    if completion_rate >= 95 and overdue_defects <= 2:
        rag_status = "green"
    elif completion_rate >= 90 or (overdue_defects >= 3 and overdue_defects <= 5):
        rag_status = "amber"
    else:
        rag_status = "red"

    return {
        "rag_status": rag_status,
        "completion_rate": round(completion_rate, 2),
        "open_defects": open_defects,
        "overdue_defects": overdue_defects
    }


def get_organization_rag_summary(organization_id: int, db: Session) -> dict:
    """
    Get RAG status summary for an entire organization.

    Returns:
        dict: {
            "overall_rag": "green"|"amber"|"red",
            "green_sites": int,
            "amber_sites": int,
            "red_sites": int,
            "average_completion_rate": float,
            "total_open_defects": int
        }
    """
    sites = db.query(Site).filter(
        Site.organization_id == organization_id,
        Site.is_active == True
    ).all()

    green_count = 0
    amber_count = 0
    red_count = 0
    total_completion = 0
    total_defects = 0

    for site in sites:
        rag_data = calculate_site_rag_status(site.id, db)

        if rag_data["rag_status"] == "green":
            green_count += 1
        elif rag_data["rag_status"] == "amber":
            amber_count += 1
        else:
            red_count += 1

        total_completion += rag_data["completion_rate"]
        total_defects += rag_data["open_defects"]

    total_sites = len(sites)
    avg_completion = (total_completion / total_sites) if total_sites > 0 else 0

    # Overall RAG: worst status determines overall
    if red_count > 0:
        overall_rag = "red"
    elif amber_count > 0:
        overall_rag = "amber"
    else:
        overall_rag = "green"

    return {
        "overall_rag": overall_rag,
        "green_sites": green_count,
        "amber_sites": amber_count,
        "red_sites": red_count,
        "average_completion_rate": round(avg_completion, 2),
        "total_open_defects": total_defects
    }
