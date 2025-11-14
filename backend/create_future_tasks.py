"""
Create test checklists with future dates for testing the Upcoming Checklists feature
"""
import sys
from datetime import datetime, timedelta, date

sys.path.insert(0, 'C:/Projects/AetherCoreFSM/backend')

from app.core.database import SessionLocal
from app.models.category import Category
from app.models.checklist import Checklist, ChecklistStatus
from app.models.checklist_item import ChecklistItem
from app.models.task import Task
from app.models.site_task import SiteTask


def create_future_checklists():
    db = SessionLocal()

    try:
        # Use site_id = 1 (same as the create_today_tasks.py script)
        site_id = 1
        print(f"Creating future checklists for Site ID: {site_id}")

        # Get existing categories for this site
        categories = db.query(Category).all()
        if not categories:
            print("No categories found. Please create categories first.")
            return

        print(f"Found {len(categories)} categories")

        # Define future dates
        today = date.today()
        tomorrow = today + timedelta(days=1)
        next_week = today + timedelta(days=7)
        next_month = today + timedelta(days=30)
        three_months = today + timedelta(days=90)

        future_dates = [
            (tomorrow, "Tomorrow"),
            (next_week, "Next Week"),
            (next_month, "Next Month"),
            (three_months, "3 Months")
        ]

        created_count = 0

        # Get tasks for each category to link checklist items
        category_tasks = {}
        for category in categories:
            tasks = db.query(Task).filter(
                Task.category_id == category.id,
                Task.is_active == True
            ).all()
            if tasks:
                category_tasks[category.id] = tasks[0]  # Use first task for simplicity

        # Sample checklist items to use
        sample_items = [
            "Complete initial inspection",
            "Verify all requirements are met",
            "Document findings and observations",
            "Review and sign off"
        ]

        # Create one checklist for each category on each future date
        for date_obj, date_name in future_dates:
            for category in categories:
                # Check if checklist already exists
                existing = db.query(Checklist).filter(
                    Checklist.site_id == site_id,
                    Checklist.category_id == category.id,
                    Checklist.checklist_date == date_obj
                ).first()

                if existing:
                    print(f"Checklist already exists for '{category.name}' on {date_name}")
                    continue

                # Get task for this category (if available)
                task = category_tasks.get(category.id)
                if not task:
                    print(f"No task found for category '{category.name}', skipping")
                    continue

                # Create checklist with items
                checklist = Checklist(
                    site_id=site_id,
                    category_id=category.id,
                    checklist_date=date_obj,
                    status=ChecklistStatus.PENDING,
                    total_items=len(sample_items),
                    completed_items=0,
                    completion_percentage=0.0
                )
                db.add(checklist)
                db.flush()  # Get checklist ID

                # Add checklist items
                for item_text in sample_items:
                    checklist_item = ChecklistItem(
                        checklist_id=checklist.id,
                        task_id=task.id,
                        item_name=item_text,
                        is_completed=False
                    )
                    db.add(checklist_item)

                created_count += 1
                print(f"Created checklist for '{category.name}' on {date_name} ({date_obj}) with {len(sample_items)} items")

        db.commit()
        print(f"\nSuccessfully created {created_count} future checklists!")
        print(f"\nBreakdown:")
        print(f"  - Tomorrow ({tomorrow}): {len(categories)} checklists")
        print(f"  - Next Week ({next_week}): {len(categories)} checklists")
        print(f"  - Next Month ({next_month}): {len(categories)} checklists")
        print(f"  - 3 Months ({three_months}): {len(categories)} checklists")

    except Exception as e:
        db.rollback()
        print(f"Error creating checklists: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    print("Creating future test checklists...")
    print("=" * 50)
    create_future_checklists()
