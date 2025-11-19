from fastapi import APIRouter, Depends
from app.core.email import email_service
from app.core.dependencies import get_current_super_admin
from app.models.user import User
from datetime import date, timedelta
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
        # Create sample data
        completion_rate = 85.5
        tasks_completed = 247
        defects = [
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
        ]
        
        recommendations = [
            "Total checklists completed: 35 out of 41",
            "Average completion rate: 85.5%",
            "3 active defects require attention",
            "Excellent performance this week - keep it up!"
        ]
        
        week_end = date.today() - timedelta(days=1)
        site_name = f"Demo Site - Week Ending {week_end.strftime('%B %d, %Y')}"
        
        email_service.send_weekly_performance_email(
            to_email=to_email,
            recipient_name="Test User",
            site_name=site_name,
            completion_rate=completion_rate,
            tasks_completed=tasks_completed,
            defects=defects,
            recommendations=recommendations
        )
        
        logger.info(f"Test weekly report sent successfully to {to_email}")
        
        return {
            "status": "success",
            "message": f"Test weekly report sent to {to_email}",
            "to_email": to_email
        }
        
    except Exception as e:
        logger.error(f"Error sending test weekly report: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "message": str(e)
        }
