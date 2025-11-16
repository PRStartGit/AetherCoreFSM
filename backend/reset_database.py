"""
Database reset script - Clears database and seeds with test data
"""
import sys
from datetime import datetime, date, time, timedelta
from sqlalchemy.orm import Session

# Add the backend directory to the path
sys.path.insert(0, 'C:/Projects/AetherCoreFSM/backend')

from app.core.database import SessionLocal, engine
from app.models.user import User, UserRole
from app.models.organization import Organization
from app.models.site import Site
from app.models.user_site import UserSite
from app.models.category import Category
from app.models.task import Task
from app.models.site_task import SiteTask
from app.models.checklist import Checklist, ChecklistStatus
from app.models.checklist_item import ChecklistItem
from app.models.defect import Defect
from app.core.security import get_password_hash
from app.core.database import Base


def reset_database():
    """Drop all tables and recreate them."""
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("Database reset complete!\n")


def seed_data():
    """Seed the database with test data."""
    db = SessionLocal()

    try:
        print("Starting database seeding...\n")

        # 1. Create Organization
        print("Creating organization...")
        org = Organization(
            name="Vivaitalia Group",
            org_id="vig",
            is_active=True,
            contact_person="Admin User",
            contact_email="admin@vivaitaliagroup.com",
            contact_phone="+1234567890",
            subscription_tier="PREMIUM",
            is_trial=False
        )
        db.add(org)
        db.commit()
        db.refresh(org)
        print(f"+ Created organization: {org.name} (ID: {org.id})")

        # 2. Create Users
        print("\nCreating users...")

        # Super Admin
        super_admin = User(
            email="superadmin@aethercore.com",
            hashed_password=get_password_hash("admin123"),
            first_name="Super",
            last_name="Admin",
            role=UserRole.SUPER_ADMIN,
            is_active=True
        )
        db.add(super_admin)

        # Org Admin
        org_admin = User(
            email="orgadmin@vivaitaliagroup.com",
            hashed_password=get_password_hash("admin123"),
            first_name="Org",
            last_name="Admin",
            role=UserRole.ORG_ADMIN,
            organization_id=org.id,
            is_active=True
        )
        db.add(org_admin)

        # Site User
        site_user = User(
            email="siteuser@vivaitaliagroup.com",
            hashed_password=get_password_hash("admin123"),
            first_name="Site",
            last_name="User",
            role=UserRole.SITE_USER,
            organization_id=org.id,
            is_active=True
        )
        db.add(site_user)

        db.commit()
        db.refresh(super_admin)
        db.refresh(org_admin)
        db.refresh(site_user)

        print(f"+ Created Super Admin: {super_admin.email}")
        print(f"+ Created Org Admin: {org_admin.email}")
        print(f"+ Created Site User: {site_user.email}")

        # 3. Create 10 Sites
        print("\nCreating sites...")
        sites = []
        for i in range(1, 11):
            site = Site(
                name=f"Site {i}",
                site_code=f"SITE{i:02d}",
                organization_id=org.id,
                is_active=True,
                address=f"{i}0 Main Street",
                city="London",
                postcode=f"SW{i} 1AA",
                country="United Kingdom"
            )
            db.add(site)
            sites.append(site)

        db.commit()
        for site in sites:
            db.refresh(site)
            print(f"+ Created {site.name} ({site.site_code})")

        # 4. Assign Site User to Site 1
        print("\nAssigning site user to Site 1...")
        user_site = UserSite(
            user_id=site_user.id,
            site_id=sites[0].id  # Site 1
        )
        db.add(user_site)
        db.commit()
        print(f"+ Assigned {site_user.email} to {sites[0].name}")

        # 5. Create Categories
        print("\nCreating categories...")
        categories = [
            Category(
                name="Morning Checks",
                description="Essential morning safety and operational checks",
                closes_at=time(13, 0),  # 1 PM
                is_active=True
            ),
            Category(
                name="Afternoon Checks",
                description="Mid-day operational checks",
                closes_at=time(18, 0),  # 6 PM
                is_active=True
            ),
            Category(
                name="Evening Checks",
                description="End of day safety checks",
                closes_at=time(22, 0),  # 10 PM
                is_active=True
            ),
            Category(
                name="Equipment Inspection",
                description="Daily equipment inspection",
                closes_at=time(17, 0),  # 5 PM
                is_active=True
            )
        ]

        for cat in categories:
            db.add(cat)
        db.commit()

        for cat in categories:
            db.refresh(cat)
            print(f"+ Created category: {cat.name}")

        # 6. Create Tasks
        print("\nCreating tasks...")
        tasks_data = [
            # Morning Checks tasks
            ("Check fire extinguishers", categories[0].id),
            ("Verify emergency exits", categories[0].id),
            ("Inspect safety equipment", categories[0].id),
            ("Check first aid kit", categories[0].id),

            # Afternoon Checks tasks
            ("Monitor temperature controls", categories[1].id),
            ("Check refrigeration units", categories[1].id),
            ("Verify cleaning schedules", categories[1].id),

            # Evening Checks tasks
            ("Secure all entrances", categories[2].id),
            ("Lock storage areas", categories[2].id),
            ("Turn off non-essential equipment", categories[2].id),
            ("Final safety walkthrough", categories[2].id),

            # Equipment Inspection tasks
            ("Inspect ovens and stoves", categories[3].id),
            ("Check ventilation systems", categories[3].id),
            ("Test alarm systems", categories[3].id),
        ]

        tasks = []
        for task_name, cat_id in tasks_data:
            task = Task(
                name=task_name,
                description=f"Complete {task_name.lower()}",
                category_id=cat_id,
                is_active=True
            )
            db.add(task)
            tasks.append(task)

        db.commit()
        for task in tasks:
            db.refresh(task)
            print(f"+ Created task: {task.name}")

        # 6b. Assign tasks to Site 1
        print("\nAssigning tasks to Site 1...")
        for task in tasks:
            site_task = SiteTask(
                site_id=sites[0].id,
                task_id=task.id
            )
            db.add(site_task)
        db.commit()
        print(f"+ Assigned {len(tasks)} tasks to {sites[0].name}")

        # 7. Create Checklists for today and next 7 days for Site 1
        print("\nCreating checklists for Site 1...")
        today = date.today()

        for day_offset in range(8):  # Today + next 7 days
            checklist_date = today + timedelta(days=day_offset)

            # Create checklists for each category
            for category in categories:
                # Get tasks for this category
                category_tasks = [t for t in tasks if t.category_id == category.id]

                if not category_tasks:
                    continue

                # Create checklist
                checklist = Checklist(
                    checklist_date=checklist_date,
                    category_id=category.id,
                    site_id=sites[0].id,  # Site 1
                    status=ChecklistStatus.PENDING,
                    total_items=len(category_tasks),
                    completed_items=0,
                    completion_percentage=0
                )
                db.add(checklist)
                db.commit()
                db.refresh(checklist)

                # Create checklist items for each task
                for task in category_tasks:
                    item = ChecklistItem(
                        checklist_id=checklist.id,
                        task_id=task.id,
                        item_name=task.name,
                        is_completed=False
                    )
                    db.add(item)

                db.commit()
                print(f"+ Created {category.name} checklist for {checklist_date} with {len(category_tasks)} items")

        print("\n" + "="*50)
        print("DATABASE SEEDING COMPLETE!")
        print("="*50)
        print("\nLogin Credentials:")
        print("-"*50)
        print("Super Admin:")
        print("  Email: superadmin@aethercore.com")
        print("  Password: admin123")
        print("\nOrg Admin (Vivaitalia Group):")
        print("  Org ID: vig")
        print("  Email: orgadmin@vivaitaliagroup.com")
        print("  Password: admin123")
        print("\nSite User (Site 1):")
        print("  Org ID: vig")
        print("  Email: siteuser@vivaitaliagroup.com")
        print("  Password: admin123")
        print("  Assigned to: Site 1")
        print("-"*50)
        print(f"\nSummary:")
        print(f"  Organizations: 1 (Vivaitalia Group)")
        print(f"  Sites: 10 (Site 1 - Site 10)")
        print(f"  Users: 3 (1 Super Admin, 1 Org Admin, 1 Site User)")
        print(f"  Categories: {len(categories)}")
        print(f"  Tasks: {len(tasks)}")
        print(f"  Checklists: Created for Site 1 for today + next 7 days")
        print("="*50)

    except Exception as e:
        print(f"\nX Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("="*50)
    print("DATABASE RESET & SEED SCRIPT")
    print("="*50)
    print("\nWARNING: This will DELETE all existing data!")
    print("\nPress Enter to continue or Ctrl+C to cancel...")
    input()

    reset_database()
    seed_data()
