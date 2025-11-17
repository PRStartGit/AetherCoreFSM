"""
Celery Background Tasks
"""
import logging
from datetime import date, timedelta
from sqlalchemy.orm import Session

from app.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.category import Category
from app.models.site import Site
from app.models.checklist import Checklist, ChecklistStatus
from app.models.checklist_item import ChecklistItem
from app.models.task import Task

logger = logging.getLogger(__name__)


@celery_app.task(name='app.celery_tasks.generate_daily_checklists')
def generate_daily_checklists():
    """
    Scheduled task to generate checklists for all sites and categories
    Runs daily at midnight (00:01) via Celery Beat
    """
    db: Session = SessionLocal()
    try:
        today = date.today()
        logger.info(f"Starting daily checklist generation for {today}")

        created_count = 0
        skipped_count = 0

        # Get all active sites
        sites = db.query(Site).filter(Site.is_active == True).all()
        logger.info(f"Found {len(sites)} active sites")

        for site in sites:
            # Get active categories (global + organization-specific)
            categories = db.query(Category).filter(
                ((Category.is_global == True) | (Category.organization_id == site.organization_id)),
                Category.is_active == True
            ).all()

            for category in categories:
                # Check if checklist already exists
                existing = db.query(Checklist).filter(
                    Checklist.checklist_date == today,
                    Checklist.category_id == category.id,
                    Checklist.site_id == site.id
                ).first()

                if existing:
                    skipped_count += 1
                    logger.debug(f"Checklist already exists for site {site.name}, category {category.name}")
                    continue

                # Create new checklist
                new_checklist = Checklist(
                    checklist_date=today,
                    category_id=category.id,
                    site_id=site.id,
                    status=ChecklistStatus.PENDING
                )
                db.add(new_checklist)
                db.flush()

                # Get all active tasks for this category
                tasks = db.query(Task).filter(
                    Task.category_id == category.id,
                    Task.is_active == True
                ).order_by(Task.order_index).all()

                # Create checklist items for each task
                for task in tasks:
                    checklist_item = ChecklistItem(
                        checklist_id=new_checklist.id,
                        task_id=task.id,
                        item_name=task.name,
                        is_completed=False
                    )
                    db.add(checklist_item)

                # Set totals
                new_checklist.total_items = len(tasks)
                new_checklist.completed_items = 0

                created_count += 1
                logger.info(f"Created checklist for site {site.name}, category {category.name} with {len(tasks)} items")

        db.commit()

        logger.info(f"Daily checklist generation complete: {created_count} created, {skipped_count} skipped")

        return {
            "status": "success",
            "date": str(today),
            "created": created_count,
            "skipped": skipped_count,
            "total_sites": len(sites)
        }

    except Exception as e:
        db.rollback()
        logger.error(f"Error generating daily checklists: {str(e)}", exc_info=True)
        raise
    finally:
        db.close()


@celery_app.task(name='app.celery_tasks.test_task')
def test_task():
    """
    Simple test task to verify Celery is working
    """
    logger.info("Test task executed successfully")
    return {"status": "success", "message": "Test task completed"}
