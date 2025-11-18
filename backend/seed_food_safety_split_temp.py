"""
Seed script for Food Safety Core System with SPLIT Temperature Monitoring
This version splits temperature checks into AM and PM categories with proper time windows
"""
import sys
import os
from datetime import date, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.category import Category, ChecklistFrequency
from app.models.task import Task
from app.models.task_field import TaskField
from app.models.site import Site
from app.models.checklist import Checklist
from app.models.checklist_item import ChecklistItem


def purge_todays_checklists(db: Session):
    """Delete all checklists for today."""
    today = date.today()
    print(f"🗑️  Purging checklists for {today}...")

    todays_checklists = db.query(Checklist).filter(
        Checklist.checklist_date == today
    ).all()

    checklist_ids = [c.id for c in todays_checklists]

    if checklist_ids:
        # First delete checklist items (foreign key constraint)
        items_deleted = db.query(ChecklistItem).filter(
            ChecklistItem.checklist_id.in_(checklist_ids)
        ).delete(synchronize_session=False)

        # Then delete checklists
        checklists_deleted = db.query(Checklist).filter(
            Checklist.id.in_(checklist_ids)
        ).delete(synchronize_session=False)

        db.commit()
        print(f"✅ Deleted {items_deleted} checklist items")
        print(f"✅ Deleted {checklists_deleted} checklists")
    else:
        print("ℹ️  No checklists found for today")


def deactivate_old_categories(db: Session):
    """Deactivate old temperature monitoring categories."""
    print("\n🔄 Deactivating old categories...")

    old_categories = [
        "Temperature Monitoring",
        "Opening Checks (Temp)",
        "Closing Checks (Temp)"
    ]

    for cat_name in old_categories:
        cat = db.query(Category).filter(Category.name == cat_name).first()
        if cat:
            cat.is_active = False
            print(f"  ✅ Deactivated: {cat_name}")

    db.commit()


def seed_food_safety_split():
    """Seed the food safety system with split AM/PM temperature categories."""
    db = SessionLocal()

    try:
        print("=" * 70)
        print("🌡️  FOOD SAFETY SYSTEM - SPLIT TEMPERATURE MONITORING")
        print("=" * 70)

        # Purge today's checklists
        purge_todays_checklists(db)

        # Deactivate old categories
        deactivate_old_categories(db)

        print("\n📦 Creating new categories with proper time windows...")

        # ============================================
        # CATEGORY 1: AM Temperature Monitoring
        # Opens: 08:00, Closes: 12:00
        # ============================================
        am_temp_category = Category(
            name="AM Temperature Monitoring",
            description="Morning temperature checks for fridges and freezers",
            icon="🌡️",
            is_global=True,
            frequency=ChecklistFrequency.DAILY,
            opens_at=time(8, 0),    # Opens at 8:00 AM
            closes_at=time(12, 0),  # Must complete by 12:00 PM
            is_active=True
        )
        db.add(am_temp_category)
        db.flush()
        print(f"✅ Created AM Temperature Monitoring (ID: {am_temp_category.id}) - 08:00 to 12:00")

        # Task: Opening Fridge Checks
        task_am_fridge = Task(
            category_id=am_temp_category.id,
            name="Opening Fridge Temperature Checks",
            description="Check and record all fridge temperatures with photos",
            order_index=1,
            is_active=True,
            has_dynamic_form=True
        )
        db.add(task_am_fridge)
        db.flush()

        # Field 1: Number of Fridges
        field_am_fridge_count = TaskField(
            task_id=task_am_fridge.id,
            field_type="number",
            field_label="How many fridges need checking?",
            field_order=1,
            is_required=True,
            validation_rules={"min": 1, "max": 20}
        )
        db.add(field_am_fridge_count)
        db.flush()

        # Field 2: Repeating Group for Fridges
        field_am_fridge_repeating = TaskField(
            task_id=task_am_fridge.id,
            field_type="repeating_group",
            field_label="Fridge Temperature Records",
            field_order=2,
            is_required=True,
            validation_rules={
                "repeat_count_field_id": field_am_fridge_count.id,
                "repeat_label": "Fridge",
                "repeat_template": [
                    {
                        "type": "temperature",
                        "label": "Temperature (°C)",
                        "min": 0,
                        "max": 5,
                        "create_defect_if": "out_of_range"
                    },
                    {
                        "type": "photo",
                        "label": "Fridge Photo"
                    }
                ]
            }
        )
        db.add(field_am_fridge_repeating)
        print("  ✅ Added Opening Fridge Checks with dynamic repeating fields")

        # Task: Freezer Checks
        task_freezer = Task(
            category_id=am_temp_category.id,
            name="Freezer Temperature Checks",
            description="Check and record all freezer temperatures with photos",
            order_index=2,
            is_active=True,
            has_dynamic_form=True
        )
        db.add(task_freezer)
        db.flush()

        # Field 1: Number of Freezers
        field_freezer_count = TaskField(
            task_id=task_freezer.id,
            field_type="number",
            field_label="How many freezers need checking?",
            field_order=1,
            is_required=True,
            validation_rules={"min": 1, "max": 20}
        )
        db.add(field_freezer_count)
        db.flush()

        # Field 2: Repeating Group for Freezers
        field_freezer_repeating = TaskField(
            task_id=task_freezer.id,
            field_type="repeating_group",
            field_label="Freezer Temperature Records",
            field_order=2,
            is_required=True,
            validation_rules={
                "repeat_count_field_id": field_freezer_count.id,
                "repeat_label": "Freezer",
                "repeat_template": [
                    {
                        "type": "temperature",
                        "label": "Temperature (°C)",
                        "min": -25,
                        "max": -18,
                        "create_defect_if": "out_of_range"
                    },
                    {
                        "type": "photo",
                        "label": "Freezer Photo"
                    }
                ]
            }
        )
        db.add(field_freezer_repeating)
        print("  ✅ Added Freezer Checks with dynamic repeating fields")

        # ============================================
        # CATEGORY 2: PM Temperature Monitoring
        # Opens: 17:00, Closes: 23:59
        # ============================================
        pm_temp_category = Category(
            name="PM Temperature Monitoring",
            description="Evening temperature checks for fridges",
            icon="🌡️",
            is_global=True,
            frequency=ChecklistFrequency.DAILY,
            opens_at=time(17, 0),   # Opens at 5:00 PM
            closes_at=time(23, 59), # Must complete by midnight
            is_active=True
        )
        db.add(pm_temp_category)
        db.flush()
        print(f"✅ Created PM Temperature Monitoring (ID: {pm_temp_category.id}) - 17:00 to 23:59")

        # Task: Closing Fridge Checks
        task_pm_fridge = Task(
            category_id=pm_temp_category.id,
            name="Closing Fridge Temperature Checks",
            description="Check and record all fridge temperatures with photos",
            order_index=1,
            is_active=True,
            has_dynamic_form=True
        )
        db.add(task_pm_fridge)
        db.flush()

        # Field 1: Number of Fridges
        field_pm_fridge_count = TaskField(
            task_id=task_pm_fridge.id,
            field_type="number",
            field_label="How many fridges need checking?",
            field_order=1,
            is_required=True,
            validation_rules={"min": 1, "max": 20}
        )
        db.add(field_pm_fridge_count)
        db.flush()

        # Field 2: Repeating Group for Fridges
        field_pm_fridge_repeating = TaskField(
            task_id=task_pm_fridge.id,
            field_type="repeating_group",
            field_label="Fridge Temperature Records",
            field_order=2,
            is_required=True,
            validation_rules={
                "repeat_count_field_id": field_pm_fridge_count.id,
                "repeat_label": "Fridge",
                "repeat_template": [
                    {
                        "type": "temperature",
                        "label": "Temperature (°C)",
                        "min": 0,
                        "max": 5,
                        "create_defect_if": "out_of_range"
                    },
                    {
                        "type": "photo",
                        "label": "Fridge Photo"
                    }
                ]
            }
        )
        db.add(field_pm_fridge_repeating)
        print("  ✅ Added Closing Fridge Checks with dynamic repeating fields")

        # ============================================
        # CATEGORY 3: Opening Checks
        # Opens: 08:00, Closes: 12:00
        # ============================================
        opening_category = Category(
            name="Opening Checks",
            description="Daily opening procedures and safety checks",
            icon="🔓",
            is_global=True,
            frequency=ChecklistFrequency.DAILY,
            opens_at=time(8, 0),
            closes_at=time(12, 0),
            is_active=True
        )
        db.add(opening_category)
        db.flush()
        print(f"✅ Created Opening Checks (ID: {opening_category.id}) - 08:00 to 12:00")

        # Add opening tasks
        opening_tasks = [
            ("Unlock premises", "Unlock all doors and disable alarm", 1),
            ("Check for damage", "Visual inspection of premises for damage", 2),
            ("Turn on equipment", "Switch on all necessary kitchen equipment", 3),
            ("Check stock levels", "Verify adequate stock for the day", 4)
        ]

        for task_name, task_desc, order in opening_tasks:
            task = Task(
                category_id=opening_category.id,
                name=task_name,
                description=task_desc,
                order_index=order,
                is_active=True,
                has_dynamic_form=False
            )
            db.add(task)

        print(f"  ✅ Added {len(opening_tasks)} opening tasks")

        # ============================================
        # CATEGORY 4: Closing Checks
        # Opens: 17:00, Closes: 23:59
        # ============================================
        closing_category = Category(
            name="Closing Checks",
            description="End of day procedures and security",
            icon="🔒",
            is_global=True,
            frequency=ChecklistFrequency.DAILY,
            opens_at=time(17, 0),
            closes_at=time(23, 59),
            is_active=True
        )
        db.add(closing_category)
        db.flush()
        print(f"✅ Created Closing Checks (ID: {closing_category.id}) - 17:00 to 23:59")

        # Add closing tasks
        closing_tasks = [
            ("Clean all surfaces", "Wipe down all work surfaces and equipment", 1),
            ("Empty bins", "Empty all waste bins and replace liners", 2),
            ("Turn off equipment", "Switch off all non-essential equipment", 3),
            ("Lock premises", "Secure all doors and windows, activate alarm", 4)
        ]

        for task_name, task_desc, order in closing_tasks:
            task = Task(
                category_id=closing_category.id,
                name=task_name,
                description=task_desc,
                order_index=order,
                is_active=True,
                has_dynamic_form=False
            )
            db.add(task)

        print(f"  ✅ Added {len(closing_tasks)} closing tasks")

        db.commit()

        print("\n" + "=" * 70)
        print("✅ SEED COMPLETE - Summary:")
        print("=" * 70)
        print(f"📊 Created 4 categories:")
        print(f"   1. AM Temperature Monitoring (08:00-12:00) - 2 tasks")
        print(f"   2. PM Temperature Monitoring (17:00-23:59) - 1 task")
        print(f"   3. Opening Checks (08:00-12:00) - 4 tasks")
        print(f"   4. Closing Checks (17:00-23:59) - 4 tasks")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_food_safety_split()
