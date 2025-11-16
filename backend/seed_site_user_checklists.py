"""
Script to create comprehensive test checklists for site users
Run this to test checklist functionality
"""
from datetime import datetime, timedelta, date as dt_date, time

from app.core.database import SessionLocal, engine, Base
from app.models.checklist import Checklist, ChecklistStatus
from app.models.category import Category, ChecklistFrequency
from app.models.site import Site
from app.models.checklist_item import ChecklistItem
from app.models.task import Task
from app.models.user import User
from app.models.organization import Organization

def seed_checklists():
    """Create test checklists with categories and tasks."""
    db = SessionLocal()

    try:
        print("\n[*] Creating test checklists for site users...")

        # Get organization and site
        org = db.query(Organization).filter(Organization.org_id == "vig").first()
        if not org:
            print("[ERROR] Organization 'vig' not found!")
            return

        site = db.query(Site).filter(Site.site_code == "VIG-001").first()
        if not site:
            print("[ERROR] Site 'VIG-001' not found!")
            return

        site_user = db.query(User).filter(User.email == "siteuser@vivaitaliagroup.com").first()
        if not site_user:
            print("[ERROR] Site user not found!")
            return

        print(f"[OK] Found organization: {org.name}")
        print(f"[OK] Found site: {site.name}")
        print(f"[OK] Found site user: {site_user.email}")

        # Create categories
        print("\n[*] Creating categories...")
        categories_data = [
            {
                "name": "Opening Procedures",
                "description": "Daily opening checklist for restaurant",
                "frequency": ChecklistFrequency.DAILY,
                "closes_at": time(11, 0),
                "tasks": [
                    "Unlock entrance and disable alarm",
                    "Turn on all lights",
                    "Check temperature of refrigerators",
                    "Check temperature of freezers",
                    "Inspect kitchen cleanliness",
                    "Turn on cooking equipment",
                    "Check gas supplies",
                    "Review reservations for the day"
                ]
            },
            {
                "name": "Food Safety Checks",
                "description": "Temperature and food safety monitoring",
                "frequency": ChecklistFrequency.DAILY,
                "closes_at": time(14, 0),
                "tasks": [
                    "Check fridge temp (should be 0-5°C)",
                    "Check freezer temp (should be -18°C or below)",
                    "Inspect all food for expiry dates",
                    "Check meat storage temperatures",
                    "Verify proper food labeling",
                    "Check hot holding temperatures (above 63°C)"
                ]
            },
            {
                "name": "Cleaning & Hygiene",
                "description": "Daily cleaning and hygiene tasks",
                "frequency": ChecklistFrequency.DAILY,
                "closes_at": time(16, 0),
                "tasks": [
                    "Clean and sanitize all work surfaces",
                    "Clean and sanitize cutting boards",
                    "Clean food preparation areas",
                    "Empty and clean all bins",
                    "Sweep and mop floors",
                    "Clean customer toilets",
                    "Restock hand soap and paper towels"
                ]
            },
            {
                "name": "Closing Procedures",
                "description": "End of day closing checklist",
                "frequency": ChecklistFrequency.DAILY,
                "closes_at": time(23, 59),
                "tasks": [
                    "Turn off all cooking equipment",
                    "Clean all cooking surfaces",
                    "Store all food properly",
                    "Take out all trash",
                    "Clean and sanitize floors",
                    "Turn off all lights",
                    "Set alarm and lock doors",
                    "Complete cash reconciliation"
                ]
            },
            {
                "name": "Weekly Deep Clean",
                "description": "Weekly deep cleaning tasks",
                "frequency": ChecklistFrequency.WEEKLY,
                "closes_at": time(12, 0),
                "tasks": [
                    "Deep clean ovens and grills",
                    "Clean behind all equipment",
                    "Descale coffee machines",
                    "Clean ventilation hoods",
                    "Deep clean refrigerators",
                    "Clean and organize dry storage areas",
                    "Clean windows and doors"
                ]
            }
        ]

        categories = {}
        for cat_data in categories_data:
            # Check if category exists
            existing = db.query(Category).filter(
                Category.name == cat_data["name"],
                Category.organization_id == org.id
            ).first()

            if existing:
                print(f"   [SKIP] Category '{cat_data['name']}' already exists")
                categories[cat_data["name"]] = existing
            else:
                category = Category(
                    name=cat_data["name"],
                    description=cat_data["description"],
                    organization_id=org.id,
                    frequency=cat_data["frequency"],
                    closes_at=cat_data["closes_at"],
                    is_active=True
                )
                db.add(category)
                db.flush()
                categories[cat_data["name"]] = category
                print(f"   [OK] Created category: {cat_data['name']}")

                # Create tasks for this category
                for task_name in cat_data["tasks"]:
                    task = Task(
                        name=task_name,
                        description=task_name,
                        category_id=category.id,
                        is_active=True
                    )
                    db.add(task)
                print(f"       [OK] Created {len(cat_data['tasks'])} tasks")

        db.commit()

        # Create checklists for today
        print("\n[*] Creating checklists for today...")
        today = dt_date.today()

        checklist_scenarios = [
            {
                "category": "Opening Procedures",
                "status": ChecklistStatus.COMPLETED,
                "completed_items": 8,
                "total_items": 8,
                "completed_at": datetime.now().replace(hour=9, minute=30)
            },
            {
                "category": "Food Safety Checks",
                "status": ChecklistStatus.IN_PROGRESS,
                "completed_items": 4,
                "total_items": 6,
            },
            {
                "category": "Cleaning & Hygiene",
                "status": ChecklistStatus.PENDING,
                "completed_items": 0,
                "total_items": 7,
            },
            {
                "category": "Closing Procedures",
                "status": ChecklistStatus.PENDING,
                "completed_items": 0,
                "total_items": 8,
            }
        ]

        for scenario in checklist_scenarios:
            category = categories[scenario["category"]]

            # Check if checklist already exists
            existing = db.query(Checklist).filter(
                Checklist.site_id == site.id,
                Checklist.category_id == category.id,
                Checklist.checklist_date == today
            ).first()

            if existing:
                print(f"   [SKIP] Checklist for '{scenario['category']}' already exists")
                continue

            checklist = Checklist(
                site_id=site.id,
                category_id=category.id,
                checklist_date=today,
                status=scenario["status"],
                total_items=scenario["total_items"],
                completed_items=scenario["completed_items"],
                completed_at=scenario.get("completed_at"),
                completed_by_id=site_user.id if scenario.get("completed_at") else None
            )
            db.add(checklist)
            db.flush()
            checklist.calculate_completion()

            # Create checklist items
            tasks = db.query(Task).filter(Task.category_id == category.id).limit(scenario["total_items"]).all()
            for i, task in enumerate(tasks):
                is_completed = i < scenario["completed_items"]
                item = ChecklistItem(
                    checklist_id=checklist.id,
                    task_id=task.id,
                    item_name=task.name,
                    is_completed=is_completed,
                    completed_at=scenario.get("completed_at") if is_completed else None,
                    item_data={}
                )
                db.add(item)

            print(f"   [OK] Created checklist: {scenario['category']} ({scenario['status']})")

        # Create an overdue checklist from yesterday
        print("\n[*] Creating overdue checklist from yesterday...")
        yesterday = today - timedelta(days=1)

        category = categories["Food Safety Checks"]
        existing = db.query(Checklist).filter(
            Checklist.site_id == site.id,
            Checklist.category_id == category.id,
            Checklist.checklist_date == yesterday
        ).first()

        if not existing:
            checklist = Checklist(
                site_id=site.id,
                category_id=category.id,
                checklist_date=yesterday,
                status=ChecklistStatus.OVERDUE,
                total_items=6,
                completed_items=2
            )
            db.add(checklist)
            db.flush()
            checklist.calculate_completion()

            tasks = db.query(Task).filter(Task.category_id == category.id).limit(6).all()
            for i, task in enumerate(tasks):
                is_completed = i < 2
                item = ChecklistItem(
                    checklist_id=checklist.id,
                    task_id=task.id,
                    item_name=task.name,
                    is_completed=is_completed,
                    item_data={}
                )
                db.add(item)

            print(f"   [OK] Created overdue checklist from yesterday")
        else:
            print(f"   [SKIP] Overdue checklist already exists")

        db.commit()

        print("\n[SUCCESS] Test checklists created successfully!")
        print(f"\nYou can now test with site user: {site_user.email}")
        print(f"Password: password123")
        print(f"Organization: vig")

        # Summary
        print("\n--- SUMMARY ---")
        print(f"Categories created: {len(categories)}")
        total_checklists = db.query(Checklist).filter(
            Checklist.site_id == site.id,
            Checklist.checklist_date >= yesterday
        ).count()
        print(f"Total checklists for testing: {total_checklists}")
        print(f"- Completed: 1")
        print(f"- In Progress: 1")
        print(f"- Pending: 2")
        print(f"- Overdue: 1")

    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_checklists()
