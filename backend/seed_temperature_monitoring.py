"""
Seed script for temperature monitoring with AM/PM checks.

Creates:
- AM Temperature Checks (opens 00:00, closes 12:00)
  - AM Fridge Temperature Checks (with dynamic repeating fields)
  - AM Freezer Temperature Checks (with dynamic repeating fields)
- PM Temperature Checks (opens 17:00, closes 23:59)
  - PM Fridge Temperature Checks (with dynamic repeating fields)
  - PM Freezer Temperature Checks (with dynamic repeating fields)

Run with: python seed_temperature_monitoring.py
"""
import sys
import os
from datetime import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.category import Category, ChecklistFrequency
from app.models.task import Task
from app.models.task_field import TaskField

Base.metadata.create_all(bind=engine)


def seed_temperature_monitoring():
    """Set up AM and PM temperature monitoring with dynamic fields."""
    db = SessionLocal()

    try:
        print("🌡️  Setting up Temperature Monitoring System...")
        print("=" * 70)

        # ===================================================================
        # 1. Create/Update AM Temperature Checks Category
        # ===================================================================
        am_temp_category = db.query(Category).filter(
            Category.name == "AM Temperature Checks"
        ).first()

        if not am_temp_category:
            am_temp_category = Category(
                name="AM Temperature Checks",
                description="Morning temperature monitoring (fridge & freezer)",
                icon="🌡️",
                is_global=True,
                frequency=ChecklistFrequency.DAILY,
                opens_at=time(0, 0),    # Opens at midnight
                closes_at=time(12, 0)   # Must complete by 12:00 noon
            )
            db.add(am_temp_category)
            db.flush()
            print(f"✅ Created category: {am_temp_category.name}")
        else:
            am_temp_category.opens_at = time(0, 0)
            am_temp_category.closes_at = time(12, 0)
            db.flush()
            print(f"✅ Updated category: {am_temp_category.name}")

        # ===================================================================
        # 2. Create/Update PM Temperature Checks Category
        # ===================================================================
        pm_temp_category = db.query(Category).filter(
            Category.name == "PM Temperature Checks"
        ).first()

        if not pm_temp_category:
            pm_temp_category = Category(
                name="PM Temperature Checks",
                description="Evening temperature monitoring (fridge & freezer)",
                icon="🌡️",
                is_global=True,
                frequency=ChecklistFrequency.DAILY,
                opens_at=time(17, 0),   # Opens at 5pm
                closes_at=time(23, 59)  # Must complete by end of day
            )
            db.add(pm_temp_category)
            db.flush()
            print(f"✅ Created category: {pm_temp_category.name}")
        else:
            pm_temp_category.opens_at = time(17, 0)
            pm_temp_category.closes_at = time(23, 59)
            db.flush()
            print(f"✅ Updated category: {pm_temp_category.name}")

        # ===================================================================
        # 3. Update Closing Checks Category
        # ===================================================================
        closing_category = db.query(Category).filter(
            Category.name == "Closing Checks"
        ).first()

        if closing_category:
            closing_category.opens_at = time(18, 0)   # Opens at 6pm
            closing_category.closes_at = time(23, 59) # Must complete by end of day
            db.flush()
            print(f"✅ Updated category: {closing_category.name}")

        print()
        print("=" * 70)
        print("🔧 Setting up AM Temperature Monitoring Tasks...")
        print("=" * 70)

        # ===================================================================
        # 4. AM Fridge Temperature Checks Task
        # ===================================================================
        am_fridge_task = db.query(Task).filter(
            Task.category_id == am_temp_category.id,
            Task.name == "AM Fridge Temperature Checks"
        ).first()

        if not am_fridge_task:
            am_fridge_task = Task(
                category_id=am_temp_category.id,
                name="AM Fridge Temperature Checks",
                description="Record morning fridge temperatures",
                has_dynamic_form=True,
                is_active=True,
                order_index=1
            )
            db.add(am_fridge_task)
            db.flush()
            print(f"✅ Created task: {am_fridge_task.name}")
        else:
            print(f"✅ Found existing task: {am_fridge_task.name}")

        # Clear existing fields for AM Fridge task
        db.query(TaskField).filter(TaskField.task_id == am_fridge_task.id).delete()

        # Field 1: Number of Fridges
        field_fridge_count = TaskField(
            task_id=am_fridge_task.id,
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
            task_id=am_fridge_task.id,
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
                        "min": -5,
                        "max": 10,
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
        print(f"  ✅ Configured dynamic fields for AM Fridge checks")

        # ===================================================================
        # 5. AM Freezer Temperature Checks Task
        # ===================================================================
        am_freezer_task = db.query(Task).filter(
            Task.category_id == am_temp_category.id,
            Task.name == "AM Freezer Temperature Checks"
        ).first()

        if not am_freezer_task:
            am_freezer_task = Task(
                category_id=am_temp_category.id,
                name="AM Freezer Temperature Checks",
                description="Record morning freezer temperatures",
                has_dynamic_form=True,
                is_active=True,
                order_index=2
            )
            db.add(am_freezer_task)
            db.flush()
            print(f"✅ Created task: {am_freezer_task.name}")
        else:
            print(f"✅ Found existing task: {am_freezer_task.name}")

        # Clear existing fields for AM Freezer task
        db.query(TaskField).filter(TaskField.task_id == am_freezer_task.id).delete()

        # Field 1: Number of Freezers
        field_freezer_count = TaskField(
            task_id=am_freezer_task.id,
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
            task_id=am_freezer_task.id,
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
                        "max": -15,
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
        print(f"  ✅ Configured dynamic fields for AM Freezer checks")

        print()
        print("=" * 70)
        print("🔧 Setting up PM Temperature Monitoring Tasks...")
        print("=" * 70)

        # ===================================================================
        # 6. PM Fridge Temperature Checks Task
        # ===================================================================
        pm_fridge_task = db.query(Task).filter(
            Task.category_id == pm_temp_category.id,
            Task.name == "PM Fridge Temperature Checks"
        ).first()

        if not pm_fridge_task:
            pm_fridge_task = Task(
                category_id=pm_temp_category.id,
                name="PM Fridge Temperature Checks",
                description="Record evening fridge temperatures",
                has_dynamic_form=True,
                is_active=True,
                order_index=1
            )
            db.add(pm_fridge_task)
            db.flush()
            print(f"✅ Created task: {pm_fridge_task.name}")
        else:
            print(f"✅ Found existing task: {pm_fridge_task.name}")

        # Clear existing fields for PM Fridge task
        db.query(TaskField).filter(TaskField.task_id == pm_fridge_task.id).delete()

        # Field 1: Number of Fridges
        field_pm_fridge_count = TaskField(
            task_id=pm_fridge_task.id,
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
            task_id=pm_fridge_task.id,
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
                        "min": -5,
                        "max": 10,
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
        print(f"  ✅ Configured dynamic fields for PM Fridge checks")

        # ===================================================================
        # 7. PM Freezer Temperature Checks Task
        # ===================================================================
        pm_freezer_task = db.query(Task).filter(
            Task.category_id == pm_temp_category.id,
            Task.name == "PM Freezer Temperature Checks"
        ).first()

        if not pm_freezer_task:
            pm_freezer_task = Task(
                category_id=pm_temp_category.id,
                name="PM Freezer Temperature Checks",
                description="Record evening freezer temperatures",
                has_dynamic_form=True,
                is_active=True,
                order_index=2
            )
            db.add(pm_freezer_task)
            db.flush()
            print(f"✅ Created task: {pm_freezer_task.name}")
        else:
            print(f"✅ Found existing task: {pm_freezer_task.name}")

        # Clear existing fields for PM Freezer task
        db.query(TaskField).filter(TaskField.task_id == pm_freezer_task.id).delete()

        # Field 1: Number of Freezers
        field_pm_freezer_count = TaskField(
            task_id=pm_freezer_task.id,
            field_type="number",
            field_label="How many freezers need checking?",
            field_order=1,
            is_required=True,
            validation_rules={"min": 1, "max": 20}
        )
        db.add(field_pm_freezer_count)
        db.flush()

        # Field 2: Repeating Group for Freezers
        field_pm_freezer_repeating = TaskField(
            task_id=pm_freezer_task.id,
            field_type="repeating_group",
            field_label="Freezer Temperature Records",
            field_order=2,
            is_required=True,
            validation_rules={
                "repeat_count_field_id": field_pm_freezer_count.id,
                "repeat_label": "Freezer",
                "repeat_template": [
                    {
                        "type": "temperature",
                        "label": "Temperature (°C)",
                        "min": -25,
                        "max": -15,
                        "create_defect_if": "out_of_range"
                    },
                    {
                        "type": "photo",
                        "label": "Freezer Photo"
                    }
                ]
            }
        )
        db.add(field_pm_freezer_repeating)
        print(f"  ✅ Configured dynamic fields for PM Freezer checks")

        # Commit all changes
        db.commit()

        print()
        print("=" * 70)
        print("✅ Temperature Monitoring System configured successfully!")
        print("=" * 70)
        print()
        print("📋 Summary:")
        print(f"  • AM Temperature Checks (00:00 - 12:00)")
        print(f"    - AM Fridge Temperature Checks (dynamic, 1-20 fridges)")
        print(f"    - AM Freezer Temperature Checks (dynamic, 1-20 freezers)")
        print(f"  • PM Temperature Checks (17:00 - 23:59)")
        print(f"    - PM Fridge Temperature Checks (dynamic, 1-20 fridges)")
        print(f"    - PM Freezer Temperature Checks (dynamic, 1-20 freezers)")
        print()
        print("🎉 Site users can now record temperature + photo for each unit!")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_temperature_monitoring()
