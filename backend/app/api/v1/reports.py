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
        # Create sample data matching template expectations
        week_end = date.today() - timedelta(days=1)
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
