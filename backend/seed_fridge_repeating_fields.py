"""
Add repeating group fields to Fridge Temperature Check tasks.

This script configures the "Opening Fridge Temperature Checks" task
with a repeating group that asks "How many fridges?" and then generates
temperature + photo fields for each fridge.

Run with: python seed_fridge_repeating_fields.py
"""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.task import Task
from app.models.task_field import TaskField

# Create tables if they don't exist
from app.core.database import Base
Base.metadata.create_all(bind=engine)


def seed_fridge_repeating_fields():
    """Add repeating field configuration to fridge check tasks."""
    db = SessionLocal()

    try:
        print("🌡️  Configuring Fridge Temperature Check Fields...")
        print("=" * 60)

        # Find the Opening Fridge Temperature Checks task
        opening_fridge_task = db.query(Task).filter(
            Task.name == "Opening Fridge Temperature Checks"
        ).first()

        if not opening_fridge_task:
            print("❌ Task 'Opening Fridge Temperature Checks' not found.")
            print("   Please run seed_food_safety_data.py first.")
            return

        # Clear existing fields for this task (if any)
        existing_fields_count = db.query(TaskField).filter(
            TaskField.task_id == opening_fridge_task.id
        ).count()

        if existing_fields_count > 0:
            print(f"⚠️  Found {existing_fields_count} existing fields for this task.")
            response = input("Do you want to clear and reseed fields? (yes/no): ")
            if response.lower() != 'yes':
                print("❌ Seeding cancelled.")
                return

            db.query(TaskField).filter(
                TaskField.task_id == opening_fridge_task.id
            ).delete(synchronize_session=False)
            db.commit()
            print("✅ Existing fields cleared.")

        # ===============================================================
        # FIELD 1: Number of Fridges (NUMBER field)
        # ===============================================================
        field_count = TaskField(
            task_id=opening_fridge_task.id,
            field_type="number",
            field_label="How many fridges need checking?",
            field_order=1,
            is_required=True,
            validation_rules={
                "min": 1,
                "max": 20
            }
        )
        db.add(field_count)
        db.flush()  # Get the ID for field_count

        print(f"✅ Created field: {field_count.field_label} (ID: {field_count.id})")

        # ===============================================================
        # FIELD 2: Repeating Group for Fridge Temperatures
        # ===============================================================
        field_repeating = TaskField(
            task_id=opening_fridge_task.id,
            field_type="repeating_group",
            field_label="Fridge Temperature Records",
            field_order=2,
            is_required=True,
            validation_rules={
                "repeat_count_field_id": field_count.id,  # Links to field 1
                "repeat_label": "Fridge",  # Will show as "Fridge 1", "Fridge 2", etc.
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
        db.add(field_repeating)

        print(f"✅ Created field: {field_repeating.field_label}")

        # Commit all changes
        db.commit()
        print("=" * 60)
        print("✅ Fridge temperature check fields configured successfully!")
        print(f"\nTask: {opening_fridge_task.name}")
        print(f"  - Field 1: {field_count.field_label}")
        print(f"  - Field 2: {field_repeating.field_label}")
        print("\n🎉 Site users can now enter the number of fridges and record")
        print("   temperature + photo for each fridge dynamically!")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_fridge_repeating_fields()
