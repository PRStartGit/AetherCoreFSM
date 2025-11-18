"""
Generate checklists for today
"""
import sys
import os
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.category import Category, ChecklistFrequency
from app.models.site import Site
from app.models.task import Task
from app.models.checklist import Checklist, ChecklistStatus
from app.models.checklist_item import ChecklistItem


def generate_checklists_for_today():
    """Generate checklists for all active categories and sites for today."""
    db = SessionLocal()

    try:
        today = date.today()
        print(f"📅 Generating checklists for {today}")
        print("=" * 70)

        # Get all active sites
        sites = db.query(Site).filter(Site.is_active == True).all()
        print(f"Found {len(sites)} active sites")

        # Get all active daily categories
        categories = db.query(Category).filter(
            Category.is_active == True,
            Category.frequency == ChecklistFrequency.DAILY
        ).all()
        print(f"Found {len(categories)} active daily categories")
        print()

        created_count = 0

        for site in sites:
            print(f"Site: {site.name}")

            for category in categories:
                # Check if checklist already exists for this site/category/date
                existing = db.query(Checklist).filter(
                    Checklist.site_id == site.id,
                    Checklist.category_id == category.id,
                    Checklist.checklist_date == today
                ).first()

                if existing:
                    print(f"  ⏭️  {category.name} - Already exists")
                    continue

                # Get all active tasks for this category
                tasks = db.query(Task).filter(
                    Task.category_id == category.id,
                    Task.is_active == True
                ).order_by(Task.order_index).all()

                if not tasks:
                    print(f"  ⚠️  {category.name} - No tasks configured")
                    continue

                # Create checklist
                checklist = Checklist(
                    site_id=site.id,
                    category_id=category.id,
                    checklist_date=today,
                    status=ChecklistStatus.PENDING,
                    total_items=len(tasks),
                    completed_items=0,
                    completion_percentage=0
                )
                db.add(checklist)
                db.flush()

                # Create checklist items for each task
                for task in tasks:
                    item = ChecklistItem(
                        checklist_id=checklist.id,
                        task_id=task.id,
                        item_name=task.name,
                        is_completed=False
                    )
                    db.add(item)

                db.flush()
                created_count += 1
                print(f"  ✅ {category.name} - Created with {len(tasks)} items")

            print()

        db.commit()

        print("=" * 70)
        print(f"✅ Successfully generated {created_count} checklists for {today}")
        print("=" * 70)

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    generate_checklists_for_today()
