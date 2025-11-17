"""
Seed UK Food Safety Categories and Tasks
Based on SFBB (Safer Food Better Business) and Food Hygiene Regulations 2006

This script populates global categories and tasks that are accessible to all organizations.
Organizations can then customize these by adding/removing tasks as needed.

Run with: python seed_food_safety_data.py
"""

import sys
import os
from datetime import time

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.category import Category, ChecklistFrequency
from app.models.task import Task

# Create tables if they don't exist
from app.core.database import Base
Base.metadata.create_all(bind=engine)


def seed_food_safety_data():
    """Seed all UK food safety categories and tasks."""
    db = SessionLocal()

    try:
        print("🌍 Starting UK Food Safety Data Seeding...")
        print("=" * 60)

        # Check if data already exists
        existing_categories = db.query(Category).filter(Category.is_global == True).count()
        if existing_categories > 0:
            print(f"⚠️  Found {existing_categories} existing global categories.")
            response = input("Do you want to clear and reseed? (yes/no): ")
            if response.lower() != 'yes':
                print("❌ Seeding cancelled.")
                return

            # Delete existing global data
            print("🗑️  Clearing existing global data...")
            db.query(Task).filter(Task.category.has(is_global=True)).delete(synchronize_session=False)
            db.query(Category).filter(Category.is_global == True).delete(synchronize_session=False)
            db.commit()
            print("✅ Existing data cleared.")

        # ==================================================================
        # CATEGORY 1: TEMPERATURE MONITORING
        # ==================================================================
        cat1 = Category(
            name="Temperature Monitoring",
            description="Daily monitoring of fridge, freezer, and hot holding temperatures",
            icon="🌡️",
            frequency=ChecklistFrequency.DAILY,
            closes_at=time(23, 59),
            is_global=True,
            is_active=True
        )
        db.add(cat1)
        db.flush()

        # Task 1.1: Opening Fridge Temperature Checks
        task1_1 = Task(
            name="Opening Fridge Temperature Checks",
            description="Check all fridge temperatures at opening. Legal range: 0°C to 5°C. Temperature outside range creates HIGH defect automatically.",
            priority="high",
            category_id=cat1.id,
            order_index=1,
            has_dynamic_form=True,
            is_active=True
        )
        db.add(task1_1)

        # Task 1.2: Closing Fridge Temperature Checks
        task1_2 = Task(
            name="Closing Fridge Temperature Checks",
            description="Check all fridge temperatures at closing. Legal range: 0°C to 5°C.",
            priority="high",
            category_id=cat1.id,
            order_index=2,
            has_dynamic_form=True,
            is_active=True
        )
        db.add(task1_2)

        # Task 1.3: Freezer Temperature Checks
        task1_3 = Task(
            name="Freezer Temperature Checks",
            description="Daily freezer temperature monitoring. Legal range: -18°C to -25°C.",
            priority="high",
            category_id=cat1.id,
            order_index=3,
            has_dynamic_form=True,
            is_active=True
        )
        db.add(task1_3)

        print(f"✅ Category 1: {cat1.name} ({cat1.icon}) - 3 tasks")

        # ==================================================================
        # CATEGORY 2: OPENING CHECKS
        # ==================================================================
        cat2 = Category(
            name="Opening Checks",
            description="Daily opening procedures and safety checks",
            icon="🔓",
            frequency=ChecklistFrequency.DAILY,
            closes_at=time(9, 0),
            is_global=True,
            is_active=True
        )
        db.add(cat2)
        db.flush()

        task2_1 = Task(
            name="Daily Opening Checklist",
            description="Complete opening safety and hygiene checks including premises security, hand wash stations, fire exits, and pest activity.",
            priority="high",
            category_id=cat2.id,
            order_index=1,
            has_dynamic_form=True,
            is_active=True
        )
        db.add(task2_1)

        task2_2 = Task(
            name="Equipment Check",
            description="Verify all equipment is operational and gas/electrical safety checks.",
            priority="medium",
            category_id=cat2.id,
            order_index=2,
            has_dynamic_form=True,
            is_active=True
        )
        db.add(task2_2)

        print(f"✅ Category 2: {cat2.name} ({cat2.icon}) - 2 tasks")

        # ==================================================================
        # CATEGORY 3: CLOSING CHECKS
        # ==================================================================
        cat3 = Category(
            name="Closing Checks",
            description="End of day procedures and security",
            icon="🔒",
            frequency=ChecklistFrequency.DAILY,
            closes_at=time(23, 59),
            is_global=True,
            is_active=True
        )
        db.add(cat3)
        db.flush()

        task3_1 = Task(
            name="Daily Closing Checklist",
            description="End of day checklist including food storage, cleaning, equipment shutdown, and security.",
            priority="high",
            category_id=cat3.id,
            order_index=1,
            has_dynamic_form=True,
            is_active=True
        )
        db.add(task3_1)

        print(f"✅ Category 3: {cat3.name} ({cat3.icon}) - 1 task")

        # ==================================================================
        # CATEGORY 4: CLEANING & HYGIENE
        # ==================================================================
        cat4 = Category(
            name="Cleaning & Hygiene",
            description="Cleaning schedules and hygiene monitoring",
            icon="🧼",
            frequency=ChecklistFrequency.DAILY,
            closes_at=time(23, 59),
            is_global=True,
            is_active=True
        )
        db.add(cat4)
        db.flush()

        task4_1 = Task(
            name="Daily Kitchen Deep Clean",
            description="Complete kitchen cleaning including surfaces, sinks, equipment, floors, walls, and drains.",
            priority="high",
            category_id=cat4.id,
            order_index=1,
            has_dynamic_form=True,
            is_active=True
        )
        db.add(task4_1)

        task4_2 = Task(
            name="Weekly Deep Clean Schedule",
            description="Weekly deep cleaning of areas behind equipment, ventilation filters, light fixtures, storage areas.",
            priority="medium",
            category_id=cat4.id,
            order_index=2,
            has_dynamic_form=True,
            is_active=True
        )
        db.add(task4_2)

        print(f"✅ Category 4: {cat4.name} ({cat4.icon}) - 2 tasks")

        # ==================================================================
        # CATEGORY 5: DELIVERIES & STOCK CHECKS
        # ==================================================================
        cat5 = Category(
            name="Deliveries & Stock Checks",
            description="Supplier checks and stock rotation",
            icon="📦",
            frequency=ChecklistFrequency.DAILY,
            closes_at=time(23, 59),
            is_global=True,
            is_active=True
        )
        db.add(cat5)
        db.flush()

        task5_1 = Task(
            name="Delivery Inspection",
            description="Inspect all deliveries including vehicle cleanliness, temperatures, packaging, and dates.",
            priority="high",
            category_id=cat5.id,
            order_index=1,
            has_dynamic_form=True,
            is_active=True
        )
        db.add(task5_1)

        task5_2 = Task(
            name="Daily Use-By Date Check",
            description="Check all items for expiry dates and ensure FIFO stock rotation.",
            priority="high",
            category_id=cat5.id,
            order_index=2,
            has_dynamic_form=True,
            is_active=True
        )
        db.add(task5_2)

        print(f"✅ Category 5: {cat5.name} ({cat5.icon}) - 2 tasks")

        # ==================================================================
        # CATEGORY 6: PEST CONTROL
        # ==================================================================
        cat6 = Category(
            name="Pest Control",
            description="Pest monitoring and prevention",
            icon="🐀",
            frequency=ChecklistFrequency.DAILY,
            closes_at=time(9, 0),
            is_global=True,
            is_active=True
        )
        db.add(cat6)
        db.flush()

        task6_1 = Task(
            name="Daily Pest Activity Check",
            description="Check for any signs of pest activity. Any evidence creates HIGH defect.",
            priority="high",
            category_id=cat6.id,
            order_index=1,
            has_dynamic_form=True,
            is_active=True
        )
        db.add(task6_1)

        task6_2 = Task(
            name="Monthly Pest Control Inspection",
            description="Monthly professional pest control inspection and treatment record.",
            priority="medium",
            category_id=cat6.id,
            order_index=2,
            has_dynamic_form=True,
            is_active=True
        )
        db.add(task6_2)

        print(f"✅ Category 6: {cat6.name} ({cat6.icon}) - 2 tasks")

        # ==================================================================
        # CATEGORY 7: STAFF HYGIENE & TRAINING
        # ==================================================================
        cat7 = Category(
            name="Staff Hygiene & Training",
            description="Staff hygiene monitoring and training records",
            icon="👨‍🍳",
            frequency=ChecklistFrequency.DAILY,
            closes_at=time(9, 0),
            is_global=True,
            is_active=True
        )
        db.add(cat7)
        db.flush()

        task7_1 = Task(
            name="Daily Staff Hygiene Check",
            description="Check staff uniforms, wound coverings, and illness reporting.",
            priority="medium",
            category_id=cat7.id,
            order_index=1,
            has_dynamic_form=True,
            is_active=True
        )
        db.add(task7_1)

        task7_2 = Task(
            name="Weekly Hand Washing Observation",
            description="Observe and record proper hand washing technique and station supplies.",
            priority="low",
            category_id=cat7.id,
            order_index=2,
            has_dynamic_form=True,
            is_active=True
        )
        db.add(task7_2)

        print(f"✅ Category 7: {cat7.name} ({cat7.icon}) - 2 tasks")

        # ==================================================================
        # CATEGORY 8: COOKING & PREPARATION
        # ==================================================================
        cat8 = Category(
            name="Cooking & Preparation",
            description="Food preparation and cooking controls",
            icon="🍳",
            frequency=ChecklistFrequency.DAILY,
            closes_at=time(23, 59),
            is_global=True,
            is_active=True
        )
        db.add(cat8)
        db.flush()

        task8_1 = Task(
            name="Cooking Temperature Verification",
            description="Verify core cooking temperatures (minimum 75°C for meat).",
            priority="high",
            category_id=cat8.id,
            order_index=1,
            has_dynamic_form=True,
            is_active=True
        )
        db.add(task8_1)

        task8_2 = Task(
            name="Reheating Temperature Check",
            description="Ensure reheated food reaches minimum 75°C core temperature.",
            priority="high",
            category_id=cat8.id,
            order_index=2,
            has_dynamic_form=True,
            is_active=True
        )
        db.add(task8_2)

        print(f"✅ Category 8: {cat8.name} ({cat8.icon}) - 2 tasks")

        # ==================================================================
        # CATEGORY 9: EQUIPMENT MAINTENANCE
        # ==================================================================
        cat9 = Category(
            name="Equipment Maintenance",
            description="Equipment checks and servicing",
            icon="🔧",
            frequency=ChecklistFrequency.WEEKLY,
            closes_at=time(17, 0),
            is_global=True,
            is_active=True
        )
        db.add(cat9)
        db.flush()

        task9_1 = Task(
            name="Weekly Equipment Inspection",
            description="Check all kitchen equipment for proper operation and safety.",
            priority="medium",
            category_id=cat9.id,
            order_index=1,
            has_dynamic_form=True,
            is_active=True
        )
        db.add(task9_1)

        task9_2 = Task(
            name="Monthly Gas Safety Check",
            description="Monthly gas equipment safety inspection.",
            priority="high",
            category_id=cat9.id,
            order_index=2,
            has_dynamic_form=True,
            is_active=True
        )
        db.add(task9_2)

        print(f"✅ Category 9: {cat9.name} ({cat9.icon}) - 2 tasks")

        # ==================================================================
        # CATEGORY 10: LICENSING & COMPLIANCE
        # ==================================================================
        cat10 = Category(
            name="Licensing & Compliance",
            description="License checks and legal compliance",
            icon="📜",
            frequency=ChecklistFrequency.MONTHLY,
            closes_at=time(17, 0),
            is_global=True,
            is_active=True
        )
        db.add(cat10)
        db.flush()

        task10_1 = Task(
            name="Monthly License Display Check",
            description="Verify premises license and personal license are displayed correctly.",
            priority="medium",
            category_id=cat10.id,
            order_index=1,
            has_dynamic_form=True,
            is_active=True
        )
        db.add(task10_1)

        task10_2 = Task(
            name="Quarterly Insurance Check",
            description="Verify public liability and employer's liability insurance is valid.",
            priority="medium",
            category_id=cat10.id,
            order_index=2,
            has_dynamic_form=True,
            is_active=True
        )
        db.add(task10_2)

        print(f"✅ Category 10: {cat10.name} ({cat10.icon}) - 2 tasks")

        # ==================================================================
        # CATEGORY 11: ALLERGEN MANAGEMENT
        # ==================================================================
        cat11 = Category(
            name="Allergen Management",
            description="Allergen controls and documentation",
            icon="⚠️",
            frequency=ChecklistFrequency.DAILY,
            closes_at=time(10, 0),
            is_global=True,
            is_active=True
        )
        db.add(cat11)
        db.flush()

        task11_1 = Task(
            name="Daily Allergen Check",
            description="Verify allergen information is up to date and staff are briefed.",
            priority="high",
            category_id=cat11.id,
            order_index=1,
            has_dynamic_form=True,
            is_active=True
        )
        db.add(task11_1)

        task11_2 = Task(
            name="Weekly Allergen Training Check",
            description="Verify staff knowledge of 14 allergens and cross-contamination procedures.",
            priority="medium",
            category_id=cat11.id,
            order_index=2,
            has_dynamic_form=True,
            is_active=True
        )
        db.add(task11_2)

        print(f"✅ Category 11: {cat11.name} ({cat11.icon}) - 2 tasks")

        # ==================================================================
        # CATEGORY 12: WASTE MANAGEMENT
        # ==================================================================
        cat12 = Category(
            name="Waste Management",
            description="Waste disposal and recycling",
            icon="🗑️",
            frequency=ChecklistFrequency.DAILY,
            closes_at=time(23, 59),
            is_global=True,
            is_active=True
        )
        db.add(cat12)
        db.flush()

        task12_1 = Task(
            name="Daily Waste Disposal",
            description="Ensure bins are emptied, sanitized, and waste area is clean.",
            priority="medium",
            category_id=cat12.id,
            order_index=1,
            has_dynamic_form=True,
            is_active=True
        )
        db.add(task12_1)

        task12_2 = Task(
            name="Weekly Grease Trap Check",
            description="Clean and inspect grease trap, check drainage.",
            priority="medium",
            category_id=cat12.id,
            order_index=2,
            has_dynamic_form=True,
            is_active=True
        )
        db.add(task12_2)

        print(f"✅ Category 12: {cat12.name} ({cat12.icon}) - 2 tasks")

        # ==================================================================
        # CATEGORY 13: FIRE SAFETY
        # ==================================================================
        cat13 = Category(
            name="Fire Safety",
            description="Fire prevention and safety checks",
            icon="🔥",
            frequency=ChecklistFrequency.DAILY,
            closes_at=time(9, 0),
            is_global=True,
            is_active=True
        )
        db.add(cat13)
        db.flush()

        task13_1 = Task(
            name="Daily Fire Safety Check",
            description="Check fire exits, signs, doors, and alarm panel.",
            priority="high",
            category_id=cat13.id,
            order_index=1,
            has_dynamic_form=True,
            is_active=True
        )
        db.add(task13_1)

        task13_2 = Task(
            name="Weekly Fire Extinguisher Check",
            description="Check all fire extinguishers and fire blanket.",
            priority="high",
            category_id=cat13.id,
            order_index=2,
            has_dynamic_form=True,
            is_active=True
        )
        db.add(task13_2)

        task13_3 = Task(
            name="Monthly Fire Alarm Test",
            description="Test fire alarm system and record evacuation time.",
            priority="high",
            category_id=cat13.id,
            order_index=3,
            has_dynamic_form=True,
            is_active=True
        )
        db.add(task13_3)

        print(f"✅ Category 13: {cat13.name} ({cat13.icon}) - 3 tasks")

        # ==================================================================
        # CATEGORY 14: WATER SAFETY
        # ==================================================================
        cat14 = Category(
            name="Water Safety",
            description="Water temperature and legionella control",
            icon="💧",
            frequency=ChecklistFrequency.WEEKLY,
            closes_at=time(17, 0),
            is_global=True,
            is_active=True
        )
        db.add(cat14)
        db.flush()

        task14_1 = Task(
            name="Weekly Hot Water Temperature Check",
            description="Check hot water outlet temperature (≥50°C) and cold water (<20°C).",
            priority="medium",
            category_id=cat14.id,
            order_index=1,
            has_dynamic_form=True,
            is_active=True
        )
        db.add(task14_1)

        task14_2 = Task(
            name="Monthly Tap Flush (Unused Outlets)",
            description="Flush all unused taps to prevent legionella.",
            priority="low",
            category_id=cat14.id,
            order_index=2,
            has_dynamic_form=True,
            is_active=True
        )
        db.add(task14_2)

        print(f"✅ Category 14: {cat14.name} ({cat14.icon}) - 2 tasks")

        # Commit all changes
        db.commit()

        print("=" * 60)
        print("🎉 UK Food Safety Data Seeding Complete!")
        print(f"📊 Total: 14 categories with 31 tasks created")
        print()
        print("✅ All categories are marked as GLOBAL (is_global=True)")
        print("✅ Organizations can now access these as templates")
        print("✅ Organizations can customize by adding/removing tasks")
        print()
        print("📝 Note: Task fields can be configured through the admin interface")
        print("    or by extending this script with TaskField entries.")

    except Exception as e:
        print(f"❌ Error during seeding: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_food_safety_data()
