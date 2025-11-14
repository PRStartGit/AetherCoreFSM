"""
Comprehensive test data seeding script
Creates realistic data for testing the Site User Dashboard:
- Categories (Opening Checks, Closing Checks, Fridge Temps, etc.)
- Tasks for each category
- Site user with proper assignments
- Checklists with various statuses (overdue, due today, opening later, completed)
- Test defects
"""
import sys
from datetime import datetime, timedelta, date as dt_date, time

from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.organization import Organization
from app.models.site import Site
from app.models.category import Category, ChecklistFrequency
from app.models.task import Task
from app.models.checklist import Checklist, ChecklistStatus
from app.models.checklist_item import ChecklistItem
from app.models.defect import Defect, DefectStatus, DefectSeverity


def seed_test_data():
    """Seed comprehensive test data for Site User Dashboard testing."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        print("\n[*] Seeding test data for Site User Dashboard...")

        # Get or create test organization
        org = db.query(Organization).filter(Organization.org_id == "vig").first()
        if not org:
            print("\n[!] Organization 'vig' not found. Run seed_db.py first!")
            return

        # Get or create test site
        site = db.query(Site).filter(Site.site_code == "VIG-001").first()
        if not site:
            print("\n[!] Site 'VIG-001' not found. Run seed_db.py first!")
            return

        print(f"\n[OK] Using Organization: {org.name} (ID: {org.id})")
        print(f"[OK] Using Site: {site.name} (ID: {site.id})")

        # 1. Create Site User with site assignment
        print("\n1. Creating Test Site User...")
        existing_user = db.query(User).filter(User.email == "siteuser@vivaitaliagroup.com").first()
        if existing_user:
            site_user = existing_user
            print(f"   [EXISTS] Site User: {site_user.email}")
        else:
            site_user = User(
                email="siteuser@vivaitaliagroup.com",
                hashed_password=get_password_hash("password123"),
                first_name="Antonio",
                last_name="Ricci",
                role=UserRole.SITE_USER,
                organization_id=org.id,
                phone="+44 20 7123 9999",
                is_active=True
            )
            db.add(site_user)
            db.flush()
            print(f"   [OK] Site User created: {site_user.email} / password123")

        # 2. Create Categories
        print("\n2. Creating Categories...")

        categories_data = [
            {
                "name": "Opening Checks",
                "description": "Daily opening checks to be completed at start of shift",
                "frequency": ChecklistFrequency.DAILY,
                "closes_at": time(13, 0)  # 1 PM
            },
            {
                "name": "Fridge Temperature Checks",
                "description": "Mandatory fridge temperature monitoring",
                "frequency": ChecklistFrequency.DAILY,
                "closes_at": time(14, 0)  # 2 PM
            },
            {
                "name": "Closing Checks",
                "description": "End of day closing procedures",
                "frequency": ChecklistFrequency.DAILY,
                "closes_at": time(23, 59)  # 11:59 PM
            },
            {
                "name": "Kitchen Deep Clean",
                "description": "Weekly deep cleaning checklist",
                "frequency": ChecklistFrequency.WEEKLY,
                "closes_at": time(20, 0)  # 8 PM
            }
        ]

        categories = {}
        for cat_data in categories_data:
            existing_cat = db.query(Category).filter(
                Category.name == cat_data["name"],
                Category.organization_id == org.id
            ).first()

            if existing_cat:
                categories[cat_data["name"]] = existing_cat
                print(f"   [EXISTS] {cat_data['name']}")
            else:
                category = Category(
                    name=cat_data["name"],
                    description=cat_data["description"],
                    frequency=cat_data["frequency"],
                    closes_at=cat_data["closes_at"],
                    organization_id=org.id,
                    is_global=False,
                    is_active=True
                )
                db.add(category)
                db.flush()
                categories[cat_data["name"]] = category
                print(f"   [OK] {cat_data['name']}")

        # 3. Create Tasks for each category
        print("\n3. Creating Tasks...")

        opening_tasks = [
            {"name": "Check lights are working", "order": 1},
            {"name": "Turn on all equipment", "order": 2},
            {"name": "Check cleanliness of dining area", "order": 3},
            {"name": "Verify POS system is operational", "order": 4},
            {"name": "Stock check - napkins, cutlery, condiments", "order": 5}
        ]

        fridge_tasks = [
            {"name": "Fridge 1 - Walk-in chiller temperature", "order": 1},
            {"name": "Fridge 2 - Salad prep fridge temperature", "order": 2},
            {"name": "Fridge 3 - Dessert display fridge temperature", "order": 3},
            {"name": "Freezer 1 - Main freezer temperature", "order": 4}
        ]

        closing_tasks = [
            {"name": "Clean and sanitize all surfaces", "order": 1},
            {"name": "Turn off kitchen equipment", "order": 2},
            {"name": "Empty all bins and replace liners", "order": 3},
            {"name": "Lock all doors and windows", "order": 4},
            {"name": "Set alarm system", "order": 5},
            {"name": "Complete cash reconciliation", "order": 6}
        ]

        deep_clean_tasks = [
            {"name": "Deep clean ovens and grills", "order": 1},
            {"name": "Clean extraction system filters", "order": 2},
            {"name": "Descale dishwasher", "order": 3},
            {"name": "Clean behind all equipment", "order": 4},
            {"name": "Wash walls and ceilings", "order": 5}
        ]

        task_sets = {
            "Opening Checks": opening_tasks,
            "Fridge Temperature Checks": fridge_tasks,
            "Closing Checks": closing_tasks,
            "Kitchen Deep Clean": deep_clean_tasks
        }

        for cat_name, tasks_data in task_sets.items():
            category = categories[cat_name]
            for task_data in tasks_data:
                existing_task = db.query(Task).filter(
                    Task.name == task_data["name"],
                    Task.category_id == category.id
                ).first()

                if not existing_task:
                    task = Task(
                        category_id=category.id,
                        name=task_data["name"],
                        description=f"{task_data['name']} - part of {cat_name}",
                        order_index=task_data["order"],
                        form_config={},
                        is_active=True
                    )
                    db.add(task)

            print(f"   [OK] Tasks for {cat_name}")

        db.flush()

        # 4. Create Checklists with various statuses
        print("\n4. Creating Test Checklists...")

        today = dt_date.today()

        checklist_scenarios = [
            # OVERDUE - Opening Checks (yesterday)
            {
                "category": "Opening Checks",
                "checklist_date": today - timedelta(days=1),
                "status": ChecklistStatus.OVERDUE,
                "completed": 2,
                "total": 5
            },
            # DUE TODAY - Opening Checks
            {
                "category": "Opening Checks",
                "checklist_date": today,
                "status": ChecklistStatus.IN_PROGRESS,
                "completed": 3,
                "total": 5
            },
            # DUE TODAY - Fridge Temps
            {
                "category": "Fridge Temperature Checks",
                "checklist_date": today,
                "status": ChecklistStatus.PENDING,
                "completed": 0,
                "total": 4
            },
            # DUE TODAY - Closing (opens later)
            {
                "category": "Closing Checks",
                "checklist_date": today,
                "status": ChecklistStatus.PENDING,
                "completed": 0,
                "total": 6
            },
            # COMPLETED TODAY
            {
                "category": "Fridge Temperature Checks",
                "checklist_date": today,
                "status": ChecklistStatus.COMPLETED,
                "completed": 4,
                "total": 4,
                "completed_at": datetime.utcnow()
            },
            # COMPLETED YESTERDAY
            {
                "category": "Closing Checks",
                "checklist_date": today - timedelta(days=1),
                "status": ChecklistStatus.COMPLETED,
                "completed": 6,
                "total": 6,
                "completed_at": datetime.utcnow() - timedelta(days=1)
            }
        ]

        for scenario in checklist_scenarios:
            category = categories[scenario["category"]]

            # Check if checklist already exists
            existing = db.query(Checklist).filter(
                Checklist.site_id == site.id,
                Checklist.category_id == category.id,
                Checklist.checklist_date == scenario["checklist_date"]
            ).first()

            if not existing:
                checklist = Checklist(
                    site_id=site.id,
                    category_id=category.id,
                    checklist_date=scenario["checklist_date"],
                    status=scenario["status"],
                    total_items=scenario["total"],
                    completed_items=scenario["completed"],
                    completed_at=scenario.get("completed_at"),
                    completed_by_id=site_user.id if scenario.get("completed_at") else None
                )
                db.add(checklist)
                db.flush()

                # Create checklist items
                tasks = db.query(Task).filter(Task.category_id == category.id).all()
                for i, task in enumerate(tasks[:scenario["total"]]):
                    is_completed = i < scenario["completed"]
                    item = ChecklistItem(
                        checklist_id=checklist.id,
                        task_id=task.id,
                        item_name=task.name,
                        is_completed=is_completed,
                        completed_at=scenario.get("completed_at") if is_completed else None,
                        item_data={}
                    )
                    db.add(item)

                print(f"   [OK] {scenario['category']} - {scenario['status']}")

        db.flush()

        # 5. Create Test Defects
        print("\n5. Creating Test Defects...")

        defects_data = [
            {
                "title": "Fridge 2 temperature fluctuating",
                "description": "Salad prep fridge showing inconsistent temperatures between 2°C and 8°C",
                "severity": DefectSeverity.HIGH,
                "status": DefectStatus.OPEN
            },
            {
                "title": "Broken light in storage room",
                "description": "Ceiling light not working, making it difficult to see stock",
                "severity": DefectSeverity.MEDIUM,
                "status": DefectStatus.OPEN
            },
            {
                "title": "Leaking tap in kitchen",
                "description": "Constant drip from main sink tap, wasting water",
                "severity": DefectSeverity.LOW,
                "status": DefectStatus.OPEN
            }
        ]

        for defect_data in defects_data:
            existing_defect = db.query(Defect).filter(
                Defect.title == defect_data["title"],
                Defect.site_id == site.id
            ).first()

            if not existing_defect:
                defect = Defect(
                    site_id=site.id,
                    title=defect_data["title"],
                    description=defect_data["description"],
                    severity=defect_data["severity"],
                    status=defect_data["status"],
                    reported_by_id=site_user.id
                )
                db.add(defect)

                print(f"   [OK] {defect_data['severity']} - {defect_data['title']}")

        # Commit all changes
        db.commit()

        print("\n[SUCCESS] Test data seeding completed successfully!")
        print("\n[SUMMARY]")
        print(f"   - 4 Categories (Opening, Fridge Temps, Closing, Deep Clean)")
        print(f"   - ~20 Tasks across categories")
        print(f"   - 6 Checklists (1 overdue, 2 due today, 1 opening later, 2 completed)")
        print(f"   - 3 Test Defects")
        print(f"   - 1 Site User assigned to {site.name}")
        print("\n[TEST LOGIN CREDENTIALS]")
        print(f"   Organization: vig")
        print(f"   Email: siteuser@vivaitaliagroup.com")
        print(f"   Password: password123")
        print(f"\n[READY TO TEST]")
        print(f"   URL: http://localhost:4200")

    except Exception as e:
        print(f"\n[ERROR] Error seeding test data: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    seed_test_data()
