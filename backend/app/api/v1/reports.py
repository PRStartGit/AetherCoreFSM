from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from app.core.email import email_service
from app.core.dependencies import get_current_super_admin, get_current_user
from app.core.database import get_db
from app.models.user import User, UserRole
from app.models.checklist import ChecklistStatus
from app.models.site import Site
from app.models.organization import Organization
from app.models.organization_module import OrganizationModule
from sqlalchemy.orm import Session
from datetime import date, timedelta
from typing import List, Optional
from io import BytesIO
import zipfile
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/reports/test-weekly-email")
def send_test_weekly_email(
    to_email: str = "hello@prstart.co.uk",
    current_user: User = Depends(get_current_super_admin)
):
    """Send a test weekly performance report email"""

    try:
        # Create sample data matching template expectations
        week_end = date.today()  # Current week ending today
        week_start = week_end - timedelta(days=6)

        report_data = {
            'completion_rate': 85.5,
            'tasks_completed': 247,
            'total_tasks': 289,
            'top_sites': [
                {
                    'site_name': 'Main Office - Building A',
                    'tasks_completed': 145,
                    'tasks_total': 156,
                    'performance_percentage': 93,
                    'performance_class': 'positive',
                    'performance_color': '#10b981'
                },
                {
                    'site_name': 'Warehouse North',
                    'tasks_completed': 78,
                    'tasks_total': 89,
                    'performance_percentage': 88,
                    'performance_class': 'positive',
                    'performance_color': '#10b981'
                }
            ],
            'attention_sites': [
                {
                    'site_name': 'Warehouse South',
                    'tasks_completed': 24,
                    'tasks_total': 44,
                    'performance_percentage': 55,
                    'performance_class': 'negative',
                    'performance_color': '#ef4444'
                }
            ],
            'category_stats': [
                {'category_name': 'Health & Safety', 'completion_rate': 92},
                {'category_name': 'Fire Safety', 'completion_rate': 88},
                {'category_name': 'Cleaning', 'completion_rate': 78}
            ],
            'insights': [
                'Fire Safety compliance improved by 12% this week',
                'Warehouse South requires attention - only 55% completion',
                '3 high-priority defects need immediate action'
            ],
            'defects': [
                {
                    'title': 'Fire extinguisher expired in Zone A',
                    'severity': 'HIGH',
                    'created_at': '2025-11-15',
                    'description': 'Annual inspection overdue'
                },
                {
                    'title': 'Emergency exit sign not illuminated',
                    'severity': 'CRITICAL',
                    'created_at': '2025-11-18',
                    'description': 'Located at rear exit door'
                },
                {
                    'title': 'Minor water leak in break room',
                    'severity': 'MEDIUM',
                    'created_at': '2025-11-12',
                    'description': 'Sink faucet dripping'
                }
            ],
            'recommendations': [
                "Total checklists completed: 35 out of 41",
                "Average completion rate: 85.5%",
                "3 active defects require attention",
                "Excellent performance this week - keep it up!"
            ]
        }

        email_service.send_weekly_performance_email(
            recipient_email=to_email,
            recipient_name="Test User",
            organization_name="Demo Organization - Weekly Report",
            week_start=week_start.strftime('%Y-%m-%d'),
            week_end=week_end.strftime('%Y-%m-%d'),
            report_data=report_data
        )

        logger.info(f"Test weekly report sent successfully to {to_email}")

        return {
            "status": "success",
            "message": f"Test weekly report sent to {to_email}",
            "to_email": to_email,
            "week_start": week_start.strftime('%Y-%m-%d'),
            "week_end": week_end.strftime('%Y-%m-%d')
        }

    except Exception as e:
        logger.error(f"Error sending test weekly report: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "message": str(e)
        }


@router.post("/reports/weekly/{site_id}")
def send_weekly_report_for_site(
    site_id: int,
    current_user: User = Depends(get_current_super_admin)
):
    """Generate and send weekly performance report for a specific site"""
    
    from app.models.site import Site
    from app.models.checklist import Checklist
    from app.models.defect import Defect
    from app.models.category import Category
    from sqlalchemy.orm import Session
    from app.core.database import SessionLocal
    from datetime import datetime
    
    db: Session = SessionLocal()
    
    try:
        # Get site
        site = db.query(Site).filter(Site.id == site_id).first()
        if not site:
            return {"status": "error", "message": f"Site {site_id} not found"}
        
        if not site.report_recipients:
            return {"status": "error", "message": "No report recipients configured for this site"}
        
        # Calculate week range - current week ending today
        week_end = date.today()
        week_start = week_end - timedelta(days=6)
        
        # Get checklists for the week
        checklists = db.query(Checklist).filter(
            Checklist.site_id == site_id,
            Checklist.checklist_date >= week_start,
            Checklist.checklist_date <= week_end
        ).all()
        
        total_checklists = len(checklists)
        completed_checklists = len([c for c in checklists if c.status == ChecklistStatus.COMPLETED])
        completion_rate = (completed_checklists / total_checklists * 100) if total_checklists > 0 else 0
        
        # Get defects
        defects = db.query(Defect).filter(
            Defect.site_id == site_id,
            Defect.created_at >= datetime.combine(week_start, datetime.min.time())
        ).all()
        
        defects_data = [{
            'title': d.title,
            'severity': d.severity,
            'created_at': d.created_at.strftime('%Y-%m-%d'),
            'description': d.description or ''
        } for d in defects]
        
        # Get category stats
        categories = db.query(Category).filter(Category.organization_id == site.organization_id).all()
        category_stats = []
        for cat in categories:
            cat_checklists = [c for c in checklists if c.category_id == cat.id]
            cat_total = len(cat_checklists)
            cat_completed = len([c for c in cat_checklists if c.status == ChecklistStatus.COMPLETED])
            cat_rate = (cat_completed / cat_total * 100) if cat_total > 0 else 0
            if cat_total > 0:
                category_stats.append({
                    'category_name': cat.name,
                    'completion_rate': round(cat_rate, 1)
                })
        
        report_data = {
            'completion_rate': round(completion_rate, 1),
            'tasks_completed': completed_checklists,
            'total_tasks': total_checklists,
            'defects': defects_data,
            'category_stats': sorted(category_stats, key=lambda x: x['completion_rate'], reverse=True)[:5],
            'insights': [],
            'recommendations': [
                f"Completed {completed_checklists} out of {total_checklists} checklists",
                f"Overall completion rate: {round(completion_rate, 1)}%",
                f"{len(defects_data)} defects reported this week"
            ],
            'top_sites': [],
            'attention_sites': []
        }
        
        # Send to all recipients
        recipients = [email.strip() for email in site.report_recipients.split(',')]
        for recipient in recipients:
            if recipient:
                email_service.send_weekly_performance_email(
                    recipient_email=recipient,
                    recipient_name="Site Manager",
                    organization_name=site.name,
                    week_start=week_start.strftime('%Y-%m-%d'),
                    week_end=week_end.strftime('%Y-%m-%d'),
                    report_data=report_data
                )
        
        logger.info(f"Weekly report sent for site {site_id} to {len(recipients)} recipients")
        
        return {
            "status": "success",
            "message": f"Weekly report sent to {len(recipients)} recipients",
            "site_name": site.name,
            "recipients": recipients,
            "completion_rate": round(completion_rate, 1),
            "week_start": week_start.strftime('%Y-%m-%d'),
            "week_end": week_end.strftime('%Y-%m-%d')
        }
        
    except Exception as e:
        logger.error(f"Error sending weekly report: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "message": str(e)
        }
    finally:
        db.close()


@router.post("/reports/organization/{org_id}")
def send_org_wide_report(
    org_id: int,
    current_user: User = Depends(get_current_super_admin)
):
    """Generate and send organization-wide weekly performance report"""

    from app.models.organization import Organization
    from app.models.site import Site
    from app.models.checklist import Checklist
    from app.models.defect import Defect
    from app.models.category import Category
    from sqlalchemy.orm import Session
    from app.core.database import SessionLocal
    from datetime import datetime

    db: Session = SessionLocal()

    try:
        # Get organization
        organization = db.query(Organization).filter(Organization.id == org_id).first()
        if not organization:
            return {"status": "error", "message": f"Organization {org_id} not found"}

        if not organization.org_report_recipients:
            return {"status": "error", "message": "No report recipients configured for this organization"}

        # Calculate week range
        week_end = date.today()
        week_start = week_end - timedelta(days=6)

        # Get all active sites for this organization
        sites = db.query(Site).filter(
            Site.organization_id == org_id,
            Site.is_active == True
        ).all()

        if not sites:
            return {"status": "error", "message": "No active sites found for this organization"}

        # Aggregate data across all sites
        total_checklists = 0
        completed_checklists = 0
        all_defects = []
        site_stats = []

        for site in sites:
            # Get checklists for the week for this site
            site_checklists = db.query(Checklist).filter(
                Checklist.site_id == site.id,
                Checklist.checklist_date >= week_start,
                Checklist.checklist_date <= week_end
            ).all()

            site_total = len(site_checklists)
            site_completed = len([c for c in site_checklists if c.status == ChecklistStatus.COMPLETED])
            site_rate = (site_completed / site_total * 100) if site_total > 0 else 0

            total_checklists += site_total
            completed_checklists += site_completed

            # Get defects for this site
            site_defects = db.query(Defect).filter(
                Defect.site_id == site.id,
                Defect.created_at >= datetime.combine(week_start, datetime.min.time())
            ).all()

            for d in site_defects:
                all_defects.append({
                    'title': f"[{site.name}] {d.title}",
                    'severity': d.severity,
                    'created_at': d.created_at.strftime('%Y-%m-%d'),
                    'description': d.description or ''
                })

            # Determine performance class
            if site_rate >= 80:
                perf_class = 'positive'
                perf_color = '#10b981'
            else:
                perf_class = 'negative'
                perf_color = '#ef4444'

            site_stats.append({
                'site_name': site.name,
                'tasks_completed': site_completed,
                'tasks_total': site_total,
                'performance_percentage': round(site_rate),
                'performance_class': perf_class,
                'performance_color': perf_color
            })

        # Sort sites by performance
        site_stats.sort(key=lambda x: x['performance_percentage'], reverse=True)
        top_sites = [s for s in site_stats if s['performance_percentage'] >= 80][:5]
        attention_sites = [s for s in site_stats if s['performance_percentage'] < 80]

        # Calculate overall completion rate
        overall_rate = (completed_checklists / total_checklists * 100) if total_checklists > 0 else 0

        # Get category stats across all sites
        categories = db.query(Category).filter(
            Category.organization_id == org_id,
            Category.is_active == True
        ).all()

        category_stats = []
        for cat in categories:
            cat_checklists = db.query(Checklist).filter(
                Checklist.category_id == cat.id,
                Checklist.site_id.in_([s.id for s in sites]),
                Checklist.checklist_date >= week_start,
                Checklist.checklist_date <= week_end
            ).all()
            cat_total = len(cat_checklists)
            cat_completed = len([c for c in cat_checklists if c.status == ChecklistStatus.COMPLETED])
            cat_rate = (cat_completed / cat_total * 100) if cat_total > 0 else 0
            if cat_total > 0:
                category_stats.append({
                    'category_name': cat.name,
                    'completion_rate': round(cat_rate, 1)
                })

        # Build insights
        insights = []
        if attention_sites:
            insights.append(f"{len(attention_sites)} site(s) need attention (below 80% completion)")
        if top_sites:
            insights.append(f"{len(top_sites)} site(s) performing excellently (80%+ completion)")
        if all_defects:
            critical_defects = len([d for d in all_defects if d['severity'] == 'CRITICAL'])
            if critical_defects > 0:
                insights.append(f"{critical_defects} critical defect(s) require immediate attention")

        report_data = {
            'completion_rate': round(overall_rate, 1),
            'tasks_completed': completed_checklists,
            'total_tasks': total_checklists,
            'top_sites': top_sites,
            'attention_sites': attention_sites,
            'category_stats': sorted(category_stats, key=lambda x: x['completion_rate'], reverse=True)[:5],
            'insights': insights,
            'defects': sorted(all_defects, key=lambda x: ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW').index(x['severity']) if x['severity'] in ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW') else 4)[:10],
            'recommendations': [
                f"Total sites monitored: {len(sites)}",
                f"Completed {completed_checklists} out of {total_checklists} checklists organization-wide",
                f"Overall completion rate: {round(overall_rate, 1)}%",
                f"{len(all_defects)} defects reported this week across all sites"
            ]
        }

        # Send to all recipients
        recipients = [email.strip() for email in organization.org_report_recipients.split(',')]
        for recipient in recipients:
            if recipient:
                email_service.send_weekly_performance_email(
                    recipient_email=recipient,
                    recipient_name="Organization Admin",
                    organization_name=f"{organization.name} - Organization Wide Report",
                    week_start=week_start.strftime('%Y-%m-%d'),
                    week_end=week_end.strftime('%Y-%m-%d'),
                    report_data=report_data
                )

        logger.info(f"Organization-wide report sent for org {org_id} to {len(recipients)} recipients")

        return {
            "status": "success",
            "message": f"Organization-wide report sent to {len(recipients)} recipients",
            "organization_name": organization.name,
            "recipients": recipients,
            "sites_included": len(sites),
            "completion_rate": round(overall_rate, 1),
            "week_start": week_start.strftime('%Y-%m-%d'),
            "week_end": week_end.strftime('%Y-%m-%d')
        }

    except Exception as e:
        logger.error(f"Error sending org-wide report: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "message": str(e)
        }
    finally:
        db.close()


@router.post("/reports/daily/{site_id}")
def send_daily_report_for_site(
    site_id: int,
    current_user: User = Depends(get_current_super_admin)
):
    """Generate and send daily performance report for a specific site"""

    from app.models.site import Site
    from app.models.checklist import Checklist
    from app.models.defect import Defect
    from app.models.category import Category
    from sqlalchemy.orm import Session
    from app.core.database import SessionLocal
    from datetime import datetime

    db: Session = SessionLocal()
    
    try:
        # Get site
        site = db.query(Site).filter(Site.id == site_id).first()
        if not site:
            return {"status": "error", "message": f"Site {site_id} not found"}
        
        if not site.report_recipients:
            return {"status": "error", "message": "No report recipients configured for this site"}
        
        # Yesterday's date for daily report
        yesterday = date.today() - timedelta(days=1)

        # Get yesterday's checklists
        checklists = db.query(Checklist).filter(
            Checklist.site_id == site_id,
            Checklist.checklist_date == yesterday
        ).all()

        total_checklists = len(checklists)
        completed_checklists = len([c for c in checklists if c.status == ChecklistStatus.COMPLETED])
        completion_rate = (completed_checklists / total_checklists * 100) if total_checklists > 0 else 0

        # Get yesterday's defects
        defects = db.query(Defect).filter(
            Defect.site_id == site_id,
            Defect.created_at >= datetime.combine(yesterday, datetime.min.time()),
            Defect.created_at < datetime.combine(yesterday + timedelta(days=1), datetime.min.time())
        ).all()
        
        defects_data = [{
            'title': d.title,
            'severity': d.severity,
            'created_at': d.created_at.strftime('%Y-%m-%d'),
            'description': d.description or ''
        } for d in defects]
        
        # Get category stats for yesterday
        categories = db.query(Category).filter(Category.organization_id == site.organization_id).all()
        category_stats = []
        for cat in categories:
            cat_checklists = [c for c in checklists if c.category_id == cat.id]
            cat_total = len(cat_checklists)
            cat_completed = len([c for c in cat_checklists if c.status == ChecklistStatus.COMPLETED])
            cat_rate = (cat_completed / cat_total * 100) if cat_total > 0 else 0
            if cat_total > 0:
                category_stats.append({
                    'category_name': cat.name,
                    'completion_rate': round(cat_rate, 1)
                })

        report_data = {
            'completion_rate': round(completion_rate, 1),
            'tasks_completed': completed_checklists,
            'total_tasks': total_checklists,
            'defects': defects_data,
            'category_stats': sorted(category_stats, key=lambda x: x['completion_rate'], reverse=True),
            'insights': [],
            'recommendations': [
                f"Completed {completed_checklists} out of {total_checklists} checklists yesterday",
                f"Overall completion rate: {round(completion_rate, 1)}%",
                f"{len(defects_data)} defects reported yesterday"
            ],
            'top_sites': [],
            'attention_sites': []
        }
        
        # Send to all recipients (using weekly template for now)
        recipients = [email.strip() for email in site.report_recipients.split(',')]
        for recipient in recipients:
            if recipient:
                email_service.send_weekly_performance_email(
                    recipient_email=recipient,
                    recipient_name="Site Manager",
                    organization_name=site.name + " - Daily Report",
                    week_start=yesterday.strftime('%Y-%m-%d'),
                    week_end=yesterday.strftime('%Y-%m-%d'),
                    report_data=report_data
                )

        logger.info(f"Daily report sent for site {site_id} to {len(recipients)} recipients")

        return {
            "status": "success",
            "message": f"Daily report sent to {len(recipients)} recipients",
            "site_name": site.name,
            "recipients": recipients,
            "completion_rate": round(completion_rate, 1),
            "report_date": yesterday.strftime('%Y-%m-%d')
        }

    except Exception as e:
        logger.error(f"Error sending daily report: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "message": str(e)
        }
    finally:
        db.close()


# ============================================
# PDF Report Generation Endpoints
# ============================================

def check_reporting_module_enabled(db: Session, organization_id: int) -> bool:
    """Check if the reporting module is enabled for an organization."""
    module = db.query(OrganizationModule).filter(
        OrganizationModule.organization_id == organization_id,
        OrganizationModule.module_name == "reporting"
    ).first()
    return module.is_enabled if module else False


@router.get("/reports/pdf/checklist")
def generate_checklist_pdf(
    site_id: int,
    report_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Generate a PDF report for a single day's checklists at a site.

    All user roles can access this endpoint for sites they have access to.
    """
    from app.services.pdf_service import pdf_service

    # Get site and verify access
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    # Check user has access to this site
    if current_user.role == UserRole.SITE_USER:
        user_site_ids = [us.site_id for us in current_user.user_sites]
        if site_id not in user_site_ids:
            raise HTTPException(status_code=403, detail="You don't have access to this site")
    elif current_user.role == UserRole.ORG_ADMIN:
        if site.organization_id != current_user.organization_id:
            raise HTTPException(status_code=403, detail="You don't have access to this site")

    # Check if reporting module is enabled (skip for super admins)
    if current_user.role != UserRole.SUPER_ADMIN:
        if not check_reporting_module_enabled(db, site.organization_id):
            raise HTTPException(
                status_code=403,
                detail="Reporting module is not enabled for your organization"
            )

    # Get organization name
    organization = db.query(Organization).filter(Organization.id == site.organization_id).first()
    org_name = organization.name if organization else "Unknown"

    # Generate PDF
    try:
        pdf_buffer = pdf_service.generate_daily_checklist_report(
            db=db,
            site_id=site_id,
            report_date=report_date,
            organization_name=org_name,
            site_name=site.name
        )

        filename = pdf_service.generate_filename(org_name, site.name, report_date)

        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except Exception as e:
        logger.error(f"Error generating PDF report: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {str(e)}")


@router.get("/reports/pdf/checklist/range")
def generate_checklist_pdf_range(
    site_id: int,
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Generate PDF reports for a date range (one PDF per day).

    Returns a ZIP file containing all PDFs if multiple days,
    or a single PDF if only one day.
    """
    from app.services.pdf_service import pdf_service

    # Validate date range
    if end_date < start_date:
        raise HTTPException(status_code=400, detail="End date must be after start date")

    if (end_date - start_date).days > 31:
        raise HTTPException(status_code=400, detail="Date range cannot exceed 31 days")

    # Get site and verify access
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    # Check user has access to this site
    if current_user.role == UserRole.SITE_USER:
        user_site_ids = [us.site_id for us in current_user.user_sites]
        if site_id not in user_site_ids:
            raise HTTPException(status_code=403, detail="You don't have access to this site")
    elif current_user.role == UserRole.ORG_ADMIN:
        if site.organization_id != current_user.organization_id:
            raise HTTPException(status_code=403, detail="You don't have access to this site")

    # Check if reporting module is enabled (skip for super admins)
    if current_user.role != UserRole.SUPER_ADMIN:
        if not check_reporting_module_enabled(db, site.organization_id):
            raise HTTPException(
                status_code=403,
                detail="Reporting module is not enabled for your organization"
            )

    # Get organization name
    organization = db.query(Organization).filter(Organization.id == site.organization_id).first()
    org_name = organization.name if organization else "Unknown"

    try:
        # If single day, return single PDF
        if start_date == end_date:
            pdf_buffer = pdf_service.generate_daily_checklist_report(
                db=db,
                site_id=site_id,
                report_date=start_date,
                organization_name=org_name,
                site_name=site.name
            )
            filename = pdf_service.generate_filename(org_name, site.name, start_date)
            return StreamingResponse(
                pdf_buffer,
                media_type="application/pdf",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        # Multiple days - create ZIP file
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            current_date = start_date
            while current_date <= end_date:
                pdf_buffer = pdf_service.generate_daily_checklist_report(
                    db=db,
                    site_id=site_id,
                    report_date=current_date,
                    organization_name=org_name,
                    site_name=site.name
                )
                filename = pdf_service.generate_filename(org_name, site.name, current_date)
                zip_file.writestr(filename, pdf_buffer.getvalue())
                current_date += timedelta(days=1)

        zip_buffer.seek(0)
        zip_filename = pdf_service.generate_filename(org_name, site.name, start_date, end_date).replace('.pdf', '.zip')

        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename={zip_filename}"}
        )

    except Exception as e:
        logger.error(f"Error generating PDF reports: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate PDFs: {str(e)}")
