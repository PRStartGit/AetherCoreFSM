"""
Comprehensive Food Safety Seed Script
Based on UK Food Safety Regulations & SFBB specifications

Creates:
- CATEGORY 1: Temperature Monitoring (with dynamic repeating fields)
- CATEGORY 2: Opening Checks (8:00 AM - 12:00 PM)
- CATEGORY 3: Closing Checks (5:00 PM - Midnight)

Run with: python seed_food_safety_core.py
"""
import sys
import os
from datetime import time, date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.category import Category, ChecklistFrequency
from app.models.task import Task
from app.models.task_field import TaskField
from app.models.checklist import Checklist

Base.metadata.create_all(bind=engine)


def purge_todays_checklists(db: Session):
    """Delete all checklists for today."""
    from app.models.checklist_item import ChecklistItem

    today = date.today()
    print(f"🗑️  Purging checklists for {today}...")

    # Get all today's checklists
    todays_checklists = db.query(Checklist).filter(
        Checklist.checklist_date == today
    ).all()

    checklist_ids = [c.id for c in todays_checklists]

    if checklist_ids:
        # First delete checklist items
        items_deleted = db.query(ChecklistItem).filter(
            ChecklistItem.checklist_id.in_(checklist_ids)
        ).delete(synchronize_session=False)

        print(f"  - Deleted {items_deleted} checklist items")

        # Then delete checklists
        checklists_deleted = db.query(Checklist).filter(
            Checklist.id.in_(checklist_ids)
        ).delete(synchronize_session=False)

        print(f"  - Deleted {checklists_deleted} checklists")
    else:
        print(f"  - No checklists to delete")

    db.commit()
    print(f"✅ Purge complete")
    print()


def deactivate_old_categories(db: Session):
    """Deactivate old temperature monitoring category."""
    print("🔄 Deactivating old categories...")

    old_temp = db.query(Category).filter(Category.name == "Temperature Monitoring").first()
    if old_temp:
        old_temp.is_active = False
        print(f"  ✅ Deactivated: {old_temp.name} (ID: {old_temp.id})")

    db.commit()
    print()


def seed_temperature_monitoring(db: Session):
    """Create comprehensive temperature monitoring system."""
    print("🌡️  Setting up CATEGORY 1: TEMPERATURE MONITORING")
    print("=" * 70)

    # ===================================================================
    # 1. Create/Update Temperature Monitoring Category
    # ===================================================================
    temp_category = db.query(Category).filter(
        Category.name == "Temperature Monitoring",
        Category.is_active == True
    ).first()

    if not temp_category:
        temp_category = Category(
            name="Temperature Monitoring",
            description="Daily monitoring of fridge, freezer, and hot holding temperatures",
            icon="🌡️",
            is_global=True,
            frequency=ChecklistFrequency.DAILY,
            opens_at=None,  # Individual tasks have their own times
            closes_at=None
        )
        db.add(temp_category)
        db.flush()
        print(f"✅ Created category: {temp_category.name}")
    else:
        print(f"✅ Found existing category: {temp_category.name}")

    print()

    # ===================================================================
    # TASK 1.1: Opening Fridge Temperature Checks
    # Schedule: Daily, 8:00 AM, Due by: 12:00 PM
    # ===================================================================
    print("Creating TASK 1.1: Opening Fridge Temperature Checks...")

    opening_fridge_task = db.query(Task).filter(
        Task.category_id == temp_category.id,
        Task.name == "Opening Fridge Temperature Checks"
    ).first()

    if not opening_fridge_task:
        opening_fridge_task = Task(
            category_id=temp_category.id,
            name="Opening Fridge Temperature Checks",
            description="Record morning fridge temperatures (Legal requirement: 0°C to 5°C)",
            has_dynamic_form=True,
            is_active=True,
            order_index=1
        )
        db.add(opening_fridge_task)
        db.flush()
        print(f"  ✅ Created task")
    else:
        print(f"  ✅ Found existing task")

    # Clear existing fields
    db.query(TaskField).filter(TaskField.task_id == opening_fridge_task.id).delete()

    # Field 1: Number of Fridges
    field_fridge_count = TaskField(
        task_id=opening_fridge_task.id,
        field_type="number",
        field_label="How many fridges need checking?",
        field_order=1,
        is_required=True,
        validation_rules={"min": 1, "max": 20}
    )
    db.add(field_fridge_count)
    db.flush()

    # Field 2: Repeating Group for Fridges
    field_fridge_repeating = TaskField(
        task_id=opening_fridge_task.id,
        field_type="repeating_group",
        field_label="Fridge Temperature Records",
        field_order=2,
        is_required=True,
        validation_rules={
            "repeat_count_field_id": field_fridge_count.id,
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
    db.add(field_fridge_repeating)

    # Field 3: Any issues?
    field_issues = TaskField(
        task_id=opening_fridge_task.id,
        field_type="yes_no",
        field_label="Any issues observed?",
        field_order=3,
        is_required=True
    )
    db.add(field_issues)

    # Field 4: Notes
    field_notes = TaskField(
        task_id=opening_fridge_task.id,
        field_type="text",
        field_label="Notes (optional)",
        field_order=4,
        is_required=False
    )
    db.add(field_notes)

    print(f"    ✅ Configured 4 dynamic fields for Opening Fridge checks")
    print()

    # ===================================================================
    # TASK 1.2: Closing Fridge Temperature Checks
    # Schedule: Daily, 5:00 PM, Due by: 11:59 PM
    # ===================================================================
    print("Creating TASK 1.2: Closing Fridge Temperature Checks...")

    closing_fridge_task = db.query(Task).filter(
        Task.category_id == temp_category.id,
        Task.name == "Closing Fridge Temperature Checks"
    ).first()

    if not closing_fridge_task:
        closing_fridge_task = Task(
            category_id=temp_category.id,
            name="Closing Fridge Temperature Checks",
            description="Record evening fridge temperatures (Legal requirement: 0°C to 5°C)",
            has_dynamic_form=True,
            is_active=True,
            order_index=2
        )
        db.add(closing_fridge_task)
        db.flush()
        print(f"  ✅ Created task")
    else:
        print(f"  ✅ Found existing task")

    # Clear existing fields
    db.query(TaskField).filter(TaskField.task_id == closing_fridge_task.id).delete()

    # Same fields as opening fridge checks
    field_closing_fridge_count = TaskField(
        task_id=closing_fridge_task.id,
        field_type="number",
        field_label="How many fridges need checking?",
        field_order=1,
        is_required=True,
        validation_rules={"min": 1, "max": 20}
    )
    db.add(field_closing_fridge_count)
    db.flush()

    field_closing_fridge_repeating = TaskField(
        task_id=closing_fridge_task.id,
        field_type="repeating_group",
        field_label="Fridge Temperature Records",
        field_order=2,
        is_required=True,
        validation_rules={
            "repeat_count_field_id": field_closing_fridge_count.id,
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
    db.add(field_closing_fridge_repeating)

    field_closing_issues = TaskField(
        task_id=closing_fridge_task.id,
        field_type="yes_no",
        field_label="Any issues observed?",
        field_order=3,
        is_required=True
    )
    db.add(field_closing_issues)

    field_closing_notes = TaskField(
        task_id=closing_fridge_task.id,
        field_type="text",
        field_label="Notes (optional)",
        field_order=4,
        is_required=False
    )
    db.add(field_closing_notes)

    print(f"    ✅ Configured 4 dynamic fields for Closing Fridge checks")
    print()

    # ===================================================================
    # TASK 1.3: Freezer Temperature Checks
    # Schedule: Daily, 8:00 AM, Due by: 12:00 PM
    # ===================================================================
    print("Creating TASK 1.3: Freezer Temperature Checks...")

    freezer_task = db.query(Task).filter(
        Task.category_id == temp_category.id,
        Task.name == "Freezer Temperature Checks"
    ).first()

    if not freezer_task:
        freezer_task = Task(
            category_id=temp_category.id,
            name="Freezer Temperature Checks",
            description="Record freezer temperatures (Legal requirement: -25°C to -18°C)",
            has_dynamic_form=True,
            is_active=True,
            order_index=3
        )
        db.add(freezer_task)
        db.flush()
        print(f"  ✅ Created task")
    else:
        print(f"  ✅ Found existing task")

    # Clear existing fields
    db.query(TaskField).filter(TaskField.task_id == freezer_task.id).delete()

    # Field 1: Number of Freezers
    field_freezer_count = TaskField(
        task_id=freezer_task.id,
        field_type="number",
        field_label="How many freezers need checking?",
        field_order=1,
        is_required=True,
        validation_rules={"min": 1, "max": 10}
    )
    db.add(field_freezer_count)
    db.flush()

    # Field 2: Repeating Group for Freezers
    field_freezer_repeating = TaskField(
        task_id=freezer_task.id,
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

    # Field 3: Any issues?
    field_freezer_issues = TaskField(
        task_id=freezer_task.id,
        field_type="yes_no",
        field_label="Any issues observed?",
        field_order=3,
        is_required=True
    )
    db.add(field_freezer_issues)

    # Field 4: Notes
    field_freezer_notes = TaskField(
        task_id=freezer_task.id,
        field_type="text",
        field_label="Notes (optional)",
        field_order=4,
        is_required=False
    )
    db.add(field_freezer_notes)

    print(f"    ✅ Configured 4 dynamic fields for Freezer checks")
    print()

    # ===================================================================
    # TASK 1.4: Hot Holding Temperature Check
    # Schedule: Daily, 12:00 PM, Due by: 2:00 PM
    # ===================================================================
    print("Creating TASK 1.4: Hot Holding Temperature Check...")

    hot_holding_task = db.query(Task).filter(
        Task.category_id == temp_category.id,
        Task.name == "Hot Holding Temperature Check"
    ).first()

    if not hot_holding_task:
        hot_holding_task = Task(
            category_id=temp_category.id,
            name="Hot Holding Temperature Check",
            description="Check hot holding units during lunch service (Legal minimum: 63°C)",
            has_dynamic_form=True,
            is_active=True,
            order_index=4
        )
        db.add(hot_holding_task)
        db.flush()
        print(f"  ✅ Created task")
    else:
        print(f"  ✅ Found existing task")

    # Clear existing fields
    db.query(TaskField).filter(TaskField.task_id == hot_holding_task.id).delete()

    # Field 1: Number of hot holding units
    field_hot_count = TaskField(
        task_id=hot_holding_task.id,
        field_type="number",
        field_label="How many hot holding units?",
        field_order=1,
        is_required=True,
        validation_rules={"min": 1, "max": 10}
    )
    db.add(field_hot_count)
    db.flush()

    # Field 2: Repeating Group for Units
    field_hot_repeating = TaskField(
        task_id=hot_holding_task.id,
        field_type="repeating_group",
        field_label="Hot Holding Unit Temperature Records",
        field_order=2,
        is_required=True,
        validation_rules={
            "repeat_count_field_id": field_hot_count.id,
            "repeat_label": "Unit",
            "repeat_template": [
                {
                    "type": "temperature",
                    "label": "Temperature (°C)",
                    "min": 63,
                    "max": 100,
                    "create_defect_if": "out_of_range"
                },
                {
                    "type": "photo",
                    "label": "Unit Photo"
                }
            ]
        }
    )
    db.add(field_hot_repeating)

    # Field 3: Notes
    field_hot_notes = TaskField(
        task_id=hot_holding_task.id,
        field_type="text",
        field_label="Notes (optional)",
        field_order=3,
        is_required=False
    )
    db.add(field_hot_notes)

    print(f"    ✅ Configured 3 dynamic fields for Hot Holding checks")
    print()


def seed_opening_checks(db: Session):
    """Create Opening Checks category and tasks."""
    print("🔓 Setting up CATEGORY 2: OPENING CHECKS")
    print("=" * 70)

    # ===================================================================
    # Create/Update Opening Checks Category
    # Opens: 8:00 AM, Closes: 12:00 PM (Noon)
    # ===================================================================
    opening_category = db.query(Category).filter(
        Category.name == "Opening Checks"
    ).first()

    if not opening_category:
        opening_category = Category(
            name="Opening Checks",
            description="Daily opening procedures and safety checks",
            icon="🔓",
            is_global=True,
            frequency=ChecklistFrequency.DAILY,
            opens_at=time(8, 0),    # Opens at 8:00 AM
            closes_at=time(12, 0)   # Must complete by 12:00 PM
        )
        db.add(opening_category)
        db.flush()
        print(f"✅ Created category: {opening_category.name} (08:00 - 12:00)")
    else:
        opening_category.opens_at = time(8, 0)
        opening_category.closes_at = time(12, 0)
        db.flush()
        print(f"✅ Updated category: {opening_category.name} (08:00 - 12:00)")

    print()

    # ===================================================================
    # TASK 2.1: Daily Opening Checklist
    # ===================================================================
    print("Creating TASK 2.1: Daily Opening Checklist...")

    opening_task = db.query(Task).filter(
        Task.category_id == opening_category.id,
        Task.name == "Daily Opening Checklist"
    ).first()

    if not opening_task:
        opening_task = Task(
            category_id=opening_category.id,
            name="Daily Opening Checklist",
            description="Complete all opening procedures and safety checks",
            has_dynamic_form=True,
            is_active=True,
            order_index=1
        )
        db.add(opening_task)
        db.flush()
        print(f"  ✅ Created task")
    else:
        print(f"  ✅ Found existing task")

    # Clear existing fields
    db.query(TaskField).filter(TaskField.task_id == opening_task.id).delete()

    # Field 1: Premises secure?
    db.add(TaskField(
        task_id=opening_task.id,
        field_type="yes_no",
        field_label="Premises secure on arrival?",
        field_order=1,
        is_required=True
    ))

    # Field 2: Kitchen clean?
    db.add(TaskField(
        task_id=opening_task.id,
        field_type="dropdown",
        field_label="Kitchen clean and ready?",
        field_order=2,
        is_required=True,
        options=["Excellent", "Good", "Fair", "Poor"]
    ))

    # Field 3: Hand wash stations stocked?
    db.add(TaskField(
        task_id=opening_task.id,
        field_type="yes_no",
        field_label="Hand wash stations stocked (soap & towels)?",
        field_order=3,
        is_required=True
    ))

    # Field 4: Fire exits clear?
    db.add(TaskField(
        task_id=opening_task.id,
        field_type="yes_no",
        field_label="Fire exits clear?",
        field_order=4,
        is_required=True
    ))

    # Field 5: Bins empty?
    db.add(TaskField(
        task_id=opening_task.id,
        field_type="yes_no",
        field_label="Bins empty and clean?",
        field_order=5,
        is_required=True
    ))

    # Field 6: Pest activity?
    db.add(TaskField(
        task_id=opening_task.id,
        field_type="yes_no",
        field_label="Any pest activity observed?",
        field_order=6,
        is_required=True
    ))

    # Field 7: Notes
    db.add(TaskField(
        task_id=opening_task.id,
        field_type="text",
        field_label="Notes (optional)",
        field_order=7,
        is_required=False
    ))

    print(f"    ✅ Configured 7 fields for Opening Checklist")
    print()


def seed_closing_checks(db: Session):
    """Create Closing Checks category and tasks."""
    print("🔒 Setting up CATEGORY 3: CLOSING CHECKS")
    print("=" * 70)

    # ===================================================================
    # Create/Update Closing Checks Category
    # Opens: 5:00 PM (17:00), Closes: Midnight (23:59)
    # ===================================================================
    closing_category = db.query(Category).filter(
        Category.name == "Closing Checks"
    ).first()

    if not closing_category:
        closing_category = Category(
            name="Closing Checks",
            description="End of day procedures and security",
            icon="🔒",
            is_global=True,
            frequency=ChecklistFrequency.DAILY,
            opens_at=time(17, 0),   # Opens at 5:00 PM
            closes_at=time(23, 59)  # Must complete by midnight
        )
        db.add(closing_category)
        db.flush()
        print(f"✅ Created category: {closing_category.name} (17:00 - 23:59)")
    else:
        closing_category.opens_at = time(17, 0)
        closing_category.closes_at = time(23, 59)
        db.flush()
        print(f"✅ Updated category: {closing_category.name} (17:00 - 23:59)")

    print()

    # ===================================================================
    # TASK 3.1: Daily Closing Checklist
    # ===================================================================
    print("Creating TASK 3.1: Daily Closing Checklist...")

    closing_task = db.query(Task).filter(
        Task.category_id == closing_category.id,
        Task.name == "Daily Closing Checklist"
    ).first()

    if not closing_task:
        closing_task = Task(
            category_id=closing_category.id,
            name="Daily Closing Checklist",
            description="Complete all end of day procedures",
            has_dynamic_form=True,
            is_active=True,
            order_index=1
        )
        db.add(closing_task)
        db.flush()
        print(f"  ✅ Created task")
    else:
        print(f"  ✅ Found existing task")

    # Clear existing fields
    db.query(TaskField).filter(TaskField.task_id == closing_task.id).delete()

    # Field 1: Food stored correctly?
    db.add(TaskField(
        task_id=closing_task.id,
        field_type="yes_no",
        field_label="All food stored correctly?",
        field_order=1,
        is_required=True
    ))

    # Field 2: Kitchen cleaned?
    db.add(TaskField(
        task_id=closing_task.id,
        field_type="dropdown",
        field_label="Kitchen cleaned and sanitized?",
        field_order=2,
        is_required=True,
        options=["Excellent", "Good", "Fair", "Poor"]
    ))

    # Field 3: Surfaces wiped?
    db.add(TaskField(
        task_id=closing_task.id,
        field_type="yes_no",
        field_label="All surfaces wiped down?",
        field_order=3,
        is_required=True
    ))

    # Field 4: Equipment off?
    db.add(TaskField(
        task_id=closing_task.id,
        field_type="yes_no",
        field_label="All equipment turned off?",
        field_order=4,
        is_required=True
    ))

    # Field 5: Fire sources extinguished?
    db.add(TaskField(
        task_id=closing_task.id,
        field_type="yes_no",
        field_label="All fire sources extinguished (gas off, candles out)?",
        field_order=5,
        is_required=True
    ))

    # Field 6: Doors locked?
    db.add(TaskField(
        task_id=closing_task.id,
        field_type="yes_no",
        field_label="Doors and windows locked?",
        field_order=6,
        is_required=True
    ))

    # Field 7: Alarm set?
    db.add(TaskField(
        task_id=closing_task.id,
        field_type="yes_no",
        field_label="Alarm set?",
        field_order=7,
        is_required=True
    ))

    # Field 8: Notes
    db.add(TaskField(
        task_id=closing_task.id,
        field_type="text",
        field_label="Notes (optional)",
        field_order=8,
        is_required=False
    ))

    print(f"    ✅ Configured 8 fields for Closing Checklist")
    print()


def main():
    """Main seed function."""
    db = SessionLocal()

    try:
        print("\n")
        print("═" * 70)
        print("   ZYNTHIO - FOOD SAFETY SYSTEM SETUP")
        print("   Based on UK Food Safety Regulations & SFBB")
        print("═" * 70)
        print("\n")

        # Step 1: Purge today's checklists
        purge_todays_checklists(db)

        # Step 2: Deactivate old categories
        deactivate_old_categories(db)

        # Step 3: Seed categories and tasks
        seed_temperature_monitoring(db)
        seed_opening_checks(db)
        seed_closing_checks(db)

        # Commit all changes
        db.commit()

        print()
        print("=" * 70)
        print("✅ FOOD SAFETY SYSTEM CONFIGURED SUCCESSFULLY!")
        print("=" * 70)
        print()
        print("📋 Summary:")
        print()
        print("  🌡️  TEMPERATURE MONITORING")
        print("      - Opening Fridge Temperature Checks (dynamic, 1-20 fridges)")
        print("      - Closing Fridge Temperature Checks (dynamic, 1-20 fridges)")
        print("      - Freezer Temperature Checks (dynamic, 1-10 freezers)")
        print("      - Hot Holding Temperature Check (dynamic, 1-10 units)")
        print()
        print("  🔓 OPENING CHECKS (08:00 - 12:00)")
        print("      - Daily Opening Checklist")
        print()
        print("  🔒 CLOSING CHECKS (17:00 - 23:59)")
        print("      - Daily Closing Checklist")
        print()
        print("🎉 All tasks use dynamic repeating fields for flexible data entry!")
        print()
        print("⚠️  Next step: Run checklist generation task to create today's checklists")
        print()

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
