"""
Create dummy tasks and checklists for today for site user testing
"""
import sys
from datetime import datetime, date, time

sys.path.insert(0, 'C:/Projects/AetherCoreFSM/backend')

from app.core.database import SessionLocal
from app.models.category import Category
from app.models.task import Task
from app.models.site_task import SiteTask
from app.models.checklist import Checklist, ChecklistStatus
from app.models.checklist_item import ChecklistItem

def create_today_tasks():
    """Create tasks and checklists for today."""
    db = SessionLocal()

    try:
        print("Creating tasks and checklists for today...\n")

        # 1. Create Categories
        print("1. Creating categories...")

        categories_data = [
            {"name": "Opening Checks", "description": "Tasks to complete when opening"},
            {"name": "Closing Checks", "description": "Tasks to complete when closing"},
            {"name": "Cleaning", "description": "Cleaning and sanitation tasks"},
            {"name": "Food Safety", "description": "Food safety and temperature checks"},
        ]

        categories = []
        for cat_data in categories_data:
            existing = db.query(Category).filter(Category.name == cat_data["name"]).first()
            if not existing:
                category = Category(
                    name=cat_data["name"],
                    description=cat_data["description"],
                    organization_id=1  # Vivaitalia Group
                )
                db.add(category)
                categories.append(category)
                print(f"  + Created category: {cat_data['name']}")
            else:
                categories.append(existing)
                print(f"  - Category already exists: {cat_data['name']}")

        db.commit()
        for cat in categories:
            db.refresh(cat)

        # 2. Create Tasks
        print("\n2. Creating tasks...")

        tasks_data = [
            {
                "name": "Morning Temperature Checks",
                "description": "Check and record all fridge and freezer temperatures",
                "category": "Food Safety",
                "items": [
                    "Check walk-in fridge temperature (should be 0-5°C)",
                    "Check freezer temperature (should be -18°C or below)",
                    "Record all readings in logbook",
                    "Report any temperature issues immediately"
                ]
            },
            {
                "name": "Opening Kitchen Prep",
                "description": "Prepare kitchen for service",
                "category": "Opening Checks",
                "items": [
                    "Check all equipment is working",
                    "Verify stock levels for today's menu",
                    "Set up prep stations",
                    "Check cleanliness of cooking areas"
                ]
            },
            {
                "name": "Deep Clean Kitchen",
                "description": "Thorough cleaning of kitchen areas",
                "category": "Cleaning",
                "items": [
                    "Clean all cooking surfaces",
                    "Mop kitchen floors",
                    "Clean and sanitize prep areas",
                    "Empty and clean grease traps",
                    "Wipe down all equipment"
                ]
            },
            {
                "name": "Closing Procedures",
                "description": "End of day closing tasks",
                "category": "Closing Checks",
                "items": [
                    "Turn off all equipment properly",
                    "Check all fridges/freezers are closed",
                    "Complete end-of-day cleaning",
                    "Secure all food storage",
                    "Lock all doors and windows"
                ]
            },
        ]

        tasks = []
        for task_data in tasks_data:
            category = next((c for c in categories if c.name == task_data["category"]), categories[0])

            existing = db.query(Task).filter(Task.name == task_data["name"]).first()
            if not existing:
                task = Task(
                    name=task_data["name"],
                    description=task_data["description"],
                    category_id=category.id,
                    is_active=True
                )
                db.add(task)
                db.flush()

                # Assign to Site 1
                site_task = SiteTask(
                    site_id=1,
                    task_id=task.id
                )
                db.add(site_task)

                tasks.append((task, task_data["items"]))
                print(f"  + Created task: {task_data['name']}")
            else:
                # Check if assigned to site 1
                site_task = db.query(SiteTask).filter(
                    SiteTask.site_id == 1,
                    SiteTask.task_id == existing.id
                ).first()
                if not site_task:
                    site_task = SiteTask(site_id=1, task_id=existing.id)
                    db.add(site_task)

                tasks.append((existing, task_data["items"]))
                print(f"  - Task already exists: {task_data['name']}")

        db.commit()

        # 3. Create Checklists for Today
        print("\n3. Creating checklists for today...")

        today = date.today()

        for task, items in tasks:
            # Check if checklist already exists for today
            existing_checklist = db.query(Checklist).filter(
                Checklist.category_id == task.category_id,
                Checklist.site_id == 1,
                Checklist.checklist_date == today
            ).first()

            if not existing_checklist:
                checklist = Checklist(
                    checklist_date=today,
                    status=ChecklistStatus.PENDING,
                    category_id=task.category_id,
                    site_id=1,
                    total_items=len(items),
                    completed_items=0,
                    completion_percentage=0.0
                )
                db.add(checklist)
                db.flush()

                # Add checklist items
                for idx, item_text in enumerate(items, 1):
                    checklist_item = ChecklistItem(
                        checklist_id=checklist.id,
                        task_id=task.id,
                        item_name=item_text,
                        is_completed=False
                    )
                    db.add(checklist_item)

                print(f"  + Created checklist for: {task.name} ({len(items)} items)")
            else:
                print(f"  - Checklist already exists for: {task.name}")

        db.commit()

        print("\n✅ Successfully created tasks and checklists!")
        print(f"\nSummary:")
        print(f"  - Categories: {len(categories)}")
        print(f"  - Tasks: {len(tasks)}")
        print(f"  - Checklists for today: {len(tasks)}")
        print(f"\nLogin as siteuser@vivaitaliagroup.com to see the tasks!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_today_tasks()
