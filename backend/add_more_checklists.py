"""
Quick script to add more checklists for today and tomorrow
Run this to add test data, easy to identify and remove later
"""
from datetime import datetime, timedelta, date as dt_date

from app.core.database import SessionLocal, engine, Base
from app.models.checklist import Checklist, ChecklistStatus
from app.models.category import Category
from app.models.site import Site
from app.models.checklist_item import ChecklistItem
from app.models.task import Task
from app.models.user import User

def add_checklists():
    """Add more checklists for testing."""
    db = SessionLocal()

    try:
        print("\n[*] Adding more test checklists...")

        # Get site and categories
        site = db.query(Site).filter(Site.site_code == "VIG-001").first()
        site_user = db.query(User).filter(User.email == "siteuser@vivaitaliagroup.com").first()

        if not site or not site_user:
            print("[ERROR] Site or user not found!")
            return

        categories = db.query(Category).filter(Category.organization_id == site.organization_id).all()

        today = dt_date.today()
        tomorrow = today + timedelta(days=1)

        # Add more checklists for today
        print(f"\n[*] Adding checklists for TODAY ({today})...")
        for category in categories[:2]:  # Opening Checks and Fridge Temps
            existing = db.query(Checklist).filter(
                Checklist.site_id == site.id,
                Checklist.category_id == category.id,
                Checklist.checklist_date == today
            ).count()

            if existing < 2:  # Add one more if less than 2 exist
                checklist = Checklist(
                    site_id=site.id,
                    category_id=category.id,
                    checklist_date=today,
                    status=ChecklistStatus.PENDING,
                    total_items=3,
                    completed_items=0
                )
                db.add(checklist)
                db.flush()

                # Add items
                tasks = db.query(Task).filter(Task.category_id == category.id).limit(3).all()
                for task in tasks:
                    item = ChecklistItem(
                        checklist_id=checklist.id,
                        task_id=task.id,
                        item_name=task.name,
                        is_completed=False,
                        item_data={}
                    )
                    db.add(item)

                print(f"   [OK] Added {category.name} for today")

        # Add checklists for tomorrow
        print(f"\n[*] Adding checklists for TOMORROW ({tomorrow})...")
        for category in categories:  # All categories
            existing = db.query(Checklist).filter(
                Checklist.site_id == site.id,
                Checklist.category_id == category.id,
                Checklist.checklist_date == tomorrow
            ).first()

            if not existing:
                checklist = Checklist(
                    site_id=site.id,
                    category_id=category.id,
                    checklist_date=tomorrow,
                    status=ChecklistStatus.PENDING,
                    total_items=4,
                    completed_items=0
                )
                db.add(checklist)
                db.flush()

                # Add items
                tasks = db.query(Task).filter(Task.category_id == category.id).limit(4).all()
                for task in tasks:
                    item = ChecklistItem(
                        checklist_id=checklist.id,
                        task_id=task.id,
                        item_name=task.name,
                        is_completed=False,
                        item_data={}
                    )
                    db.add(item)

                print(f"   [OK] Added {category.name} for tomorrow")

        db.commit()
        print("\n[SUCCESS] More checklists added!")
        print(f"\nTo remove these later, delete checklists for dates: {today}, {tomorrow}")

    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    add_checklists()
