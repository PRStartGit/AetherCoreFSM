"""
Seed script for EHO-compliant food safety categories and tasks
Based on Food Hygiene (Scotland) Regulations 2006
"""
import sys
sys.path.insert(0, "/root/AetherCoreFSM/backend")

from datetime import datetime
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.category import Category, ChecklistFrequency
from app.models.task import Task
from app.models.task_field import TaskField, TaskFieldType

def create_eho_categories(db: Session, organization_id: int = None):
    """Create all EHO-compliant categories"""

    categories_data = [
        {
            "name": "Food Safety Management System (HACCP)",
            "description": "HACCP-based food safety management procedures and documentation",
            "frequency": ChecklistFrequency.MONTHLY,
            "opens_at": "00:00",
            "closes_at": "23:59",
            "is_global": True if not organization_id else False,
            "organization_id": organization_id
        },
        {
            "name": "Temperature Control (AM)",
            "description": "Morning temperature checks for all refrigeration, freezer, and cooking equipment",
            "frequency": ChecklistFrequency.DAILY,
            "opens_at": "08:00",
            "closes_at": "12:00",
            "is_global": True if not organization_id else False,
            "organization_id": organization_id
        },
        {
            "name": "Temperature Control (PM)",
            "description": "Afternoon temperature checks for refrigeration and freezer equipment",
            "frequency": ChecklistFrequency.DAILY,
            "opens_at": "12:00",
            "closes_at": "23:59",
            "is_global": True if not organization_id else False,
            "organization_id": organization_id
        },
        {
            "name": "Personal Hygiene",
            "description": "Staff hygiene compliance and hand washing procedures",
            "frequency": ChecklistFrequency.DAILY,
            "opens_at": "09:00",
            "closes_at": "23:59",
            "is_global": True if not organization_id else False,
            "organization_id": organization_id
        },
        {
            "name": "Cleaning and Disinfection",
            "description": "Kitchen cleaning schedules and sanitization procedures",
            "frequency": ChecklistFrequency.DAILY,
            "opens_at": "09:00",
            "closes_at": "23:59",
            "is_global": True if not organization_id else False,
            "organization_id": organization_id
        },
        {
            "name": "Pest Control",
            "description": "Pest monitoring and prevention procedures",
            "frequency": ChecklistFrequency.WEEKLY,
            "opens_at": "00:00",
            "closes_at": "23:59",
            "is_global": True if not organization_id else False,
            "organization_id": organization_id
        },
        {
            "name": "Food Storage and Handling",
            "description": "Stock rotation, storage separation, and date checking",
            "frequency": ChecklistFrequency.DAILY,
            "opens_at": "09:00",
            "closes_at": "23:59",
            "is_global": True if not organization_id else False,
            "organization_id": organization_id
        },
        {
            "name": "Cross-Contamination Prevention",
            "description": "Procedures to prevent cross-contamination between raw and ready-to-eat foods",
            "frequency": ChecklistFrequency.DAILY,
            "opens_at": "09:00",
            "closes_at": "23:59",
            "is_global": True if not organization_id else False,
            "organization_id": organization_id
        },
        {
            "name": "Allergen Management",
            "description": "Allergen information and communication procedures",
            "frequency": ChecklistFrequency.WEEKLY,
            "opens_at": "00:00",
            "closes_at": "23:59",
            "is_global": True if not organization_id else False,
            "organization_id": organization_id
        },
        {
            "name": "Training Records",
            "description": "Staff training documentation and verification",
            "frequency": ChecklistFrequency.MONTHLY,
            "opens_at": "00:00",
            "closes_at": "23:59",
            "is_global": True if not organization_id else False,
            "organization_id": organization_id
        },
        {
            "name": "Equipment Maintenance",
            "description": "Equipment inspection and maintenance procedures",
            "frequency": ChecklistFrequency.WEEKLY,
            "opens_at": "00:00",
            "closes_at": "23:59",
            "is_global": True if not organization_id else False,
            "organization_id": organization_id
        },
        {
            "name": "Waste Management",
            "description": "Waste handling and disposal procedures",
            "frequency": ChecklistFrequency.DAILY,
            "opens_at": "09:00",
            "closes_at": "23:59",
            "is_global": True if not organization_id else False,
            "organization_id": organization_id
        },
        {
            "name": "Water Supply and Drainage",
            "description": "Water temperature and drainage system checks",
            "frequency": ChecklistFrequency.DAILY,
            "opens_at": "09:00",
            "closes_at": "23:59",
            "is_global": True if not organization_id else False,
            "organization_id": organization_id
        },
        {
            "name": "Structure and Facilities",
            "description": "Premises condition and facility integrity checks",
            "frequency": ChecklistFrequency.MONTHLY,
            "opens_at": "00:00",
            "closes_at": "23:59",
            "is_global": True if not organization_id else False,
            "organization_id": organization_id
        },
        {
            "name": "Supplier and Traceability",
            "description": "Supplier approval and traceability procedures",
            "frequency": ChecklistFrequency.QUARTERLY,
            "opens_at": "00:00",
            "closes_at": "23:59",
            "is_global": True if not organization_id else False,
            "organization_id": organization_id
        },
        {
            "name": "Documentation and Record Keeping",
            "description": "Record completion and storage procedures",
            "frequency": ChecklistFrequency.WEEKLY,
            "opens_at": "00:00",
            "closes_at": "23:59",
            "is_global": True if not organization_id else False,
            "organization_id": organization_id
        }
    ]

    categories = []
    for cat_data in categories_data:
        category = Category(**cat_data)
        db.add(category)
        db.flush()
        categories.append(category)
        print(f"Created category: {category.name} (ID: {category.id})")

    return categories


def create_tasks_and_fields(db: Session, categories: list):
    """Create all tasks and their dynamic fields for each category"""

    tasks = []

    # Category 1: HACCP
    haccp_cat = categories[0]
    tasks.extend([
        {
            "name": "HACCP Plan Review",
            "description": "Review all critical control points, verify procedures are current, and update documentation as needed",
            "category_id": haccp_cat.id,
            "order_index": 1,
            "has_dynamic_form": True,
            "fields": [
                {"field_type": TaskFieldType.YES_NO, "field_label": "HACCP Plan Reviewed?", "field_order": 1, "is_required": True},
                {"field_type": TaskFieldType.TEXT, "field_label": "Updates Made (if any)", "field_order": 2, "is_required": False}
            ]
        },
        {
            "name": "HACCP Records Verification",
            "description": "Check monitoring sheets, corrective actions, and verification records",
            "category_id": haccp_cat.id,
            "order_index": 2,
            "has_dynamic_form": True,
            "fields": [
                {"field_type": TaskFieldType.YES_NO, "field_label": "All Records Complete?", "field_order": 1, "is_required": True},
                {"field_type": TaskFieldType.TEXT, "field_label": "Issues Found (if any)", "field_order": 2, "is_required": False}
            ]
        }
    ])

    # Category 2: Temperature Control (AM)
    temp_am_cat = categories[1]
    tasks.extend([
        {
            "name": "AM Fridge Temperature Checks",
            "description": "Check and record temperatures of all refrigeration units (must be ≤5°C)",
            "category_id": temp_am_cat.id,
            "order_index": 1,
            "has_dynamic_form": True,
            "fields": [
                {
                    "field_type": TaskFieldType.NUMBER,
                    "field_label": "Number of Fridges",
                    "field_order": 1,
                    "is_required": True,
                    "validation_rules": {"min": 0, "max": 50}
                },
                {
                    "field_type": TaskFieldType.REPEATING_GROUP,
                    "field_label": "Fridge Temperature Readings",
                    "field_order": 2,
                    "is_required": True,
                    "validation_rules": {
                        "repeat_count_field_id": "will_be_set",
                        "repeat_label": "Fridge",
                        "repeat_template": [
                            {"type": "temperature", "label": "Temperature (°C)", "min": -10, "max": 15, "auto_defect_threshold": 5, "auto_defect_operator": ">"},
                            {"type": "photo", "label": "Photo Evidence (optional)"}
                        ]
                    }
                }
            ]
        },
        {
            "name": "AM Freezer Temperature Checks",
            "description": "Check and record temperatures of all freezers (must be ≤-18°C)",
            "category_id": temp_am_cat.id,
            "order_index": 2,
            "has_dynamic_form": True,
            "fields": [
                {
                    "field_type": TaskFieldType.NUMBER,
                    "field_label": "Number of Freezers",
                    "field_order": 1,
                    "is_required": True,
                    "validation_rules": {"min": 0, "max": 50}
                },
                {
                    "field_type": TaskFieldType.REPEATING_GROUP,
                    "field_label": "Freezer Temperature Readings",
                    "field_order": 2,
                    "is_required": True,
                    "validation_rules": {
                        "repeat_count_field_id": "will_be_set",
                        "repeat_label": "Freezer",
                        "repeat_template": [
                            {"type": "temperature", "label": "Temperature (°C)", "min": -30, "max": 0, "auto_defect_threshold": -18, "auto_defect_operator": ">"},
                            {"type": "photo", "label": "Photo Evidence (optional)"}
                        ]
                    }
                }
            ]
        },
        {
            "name": "Delivery Temperature Check",
            "description": "Record temperatures and reject if outside safe limits",
            "category_id": temp_am_cat.id,
            "order_index": 3,
            "has_dynamic_form": True,
            "fields": [
                {
                    "field_type": TaskFieldType.YES_NO,
                    "field_label": "Did you receive any deliveries?",
                    "field_order": 1,
                    "is_required": True
                },
                {
                    "field_type": TaskFieldType.NUMBER,
                    "field_label": "Number of Suppliers",
                    "field_order": 2,
                    "is_required": False,
                    "show_if": {"field_order": 1, "equals": True}
                },
                {
                    "field_type": TaskFieldType.REPEATING_GROUP,
                    "field_label": "Delivery Details",
                    "field_order": 3,
                    "is_required": False,
                    "validation_rules": {
                        "repeat_count_field_id": "will_be_set",
                        "repeat_label": "Delivery",
                        "repeat_template": [
                            {"type": "text", "label": "Supplier Name"},
                            {"type": "text", "label": "Item Description"},
                            {"type": "temperature", "label": "Temperature (°C)", "min": -30, "max": 10},
                            {"type": "photo", "label": "Photo Evidence (optional)"}
                        ]
                    },
                    "show_if": {"field_order": 1, "equals": True}
                }
            ]
        }
    ])

    # Category 3: Temperature Control (PM)
    temp_pm_cat = categories[2]
    tasks.extend([
        {
            "name": "PM Fridge Temperature Checks",
            "description": "Check and record temperatures of all refrigeration units (must be ≤5°C)",
            "category_id": temp_pm_cat.id,
            "order_index": 1,
            "has_dynamic_form": True,
            "fields": [
                {
                    "field_type": TaskFieldType.NUMBER,
                    "field_label": "Number of Fridges",
                    "field_order": 1,
                    "is_required": True,
                    "validation_rules": {"min": 0, "max": 50}
                },
                {
                    "field_type": TaskFieldType.REPEATING_GROUP,
                    "field_label": "Fridge Temperature Readings",
                    "field_order": 2,
                    "is_required": True,
                    "validation_rules": {
                        "repeat_count_field_id": "will_be_set",
                        "repeat_label": "Fridge",
                        "repeat_template": [
                            {"type": "temperature", "label": "Temperature (°C)", "min": -10, "max": 15, "auto_defect_threshold": 5, "auto_defect_operator": ">"},
                            {"type": "photo", "label": "Photo Evidence (optional)"}
                        ]
                    }
                }
            ]
        },
        {
            "name": "PM Freezer Temperature Checks",
            "description": "Check and record temperatures of all freezers (must be ≤-18°C)",
            "category_id": temp_pm_cat.id,
            "order_index": 2,
            "has_dynamic_form": True,
            "fields": [
                {
                    "field_type": TaskFieldType.NUMBER,
                    "field_label": "Number of Freezers",
                    "field_order": 1,
                    "is_required": True,
                    "validation_rules": {"min": 0, "max": 50}
                },
                {
                    "field_type": TaskFieldType.REPEATING_GROUP,
                    "field_label": "Freezer Temperature Readings",
                    "field_order": 2,
                    "is_required": True,
                    "validation_rules": {
                        "repeat_count_field_id": "will_be_set",
                        "repeat_label": "Freezer",
                        "repeat_template": [
                            {"type": "temperature", "label": "Temperature (°C)", "min": -30, "max": 0, "auto_defect_threshold": -18, "auto_defect_operator": ">"},
                            {"type": "photo", "label": "Photo Evidence (optional)"}
                        ]
                    }
                }
            ]
        }
    ])

    # Category 4: Personal Hygiene
    hygiene_cat = categories[3]
    tasks.extend([
        {
            "name": "Hand Washing Compliance Check",
            "description": "Ensure staff wash hands before handling food, after breaks, after touching raw food",
            "category_id": hygiene_cat.id,
            "order_index": 1,
            "has_dynamic_form": True,
            "fields": [
                {"field_type": TaskFieldType.YES_NO, "field_label": "Hand Washing Procedures Followed?", "field_order": 1, "is_required": True},
                {"field_type": TaskFieldType.TEXT, "field_label": "Issues Observed (if any)", "field_order": 2, "is_required": False}
            ]
        },
        {
            "name": "Personal Hygiene Inspection",
            "description": "Verify clean uniform, hair net/hat, no jewelry, clean hands, covered wounds",
            "category_id": hygiene_cat.id,
            "order_index": 2,
            "has_dynamic_form": True,
            "fields": [
                {"field_type": TaskFieldType.YES_NO, "field_label": "All Staff in Proper Attire?", "field_order": 1, "is_required": True},
                {"field_type": TaskFieldType.TEXT, "field_label": "Issues Found (if any)", "field_order": 2, "is_required": False}
            ]
        },
        {
            "name": "Staff Illness Reporting Check",
            "description": "Ensure no staff with vomiting, diarrhea, or infections are handling food",
            "category_id": hygiene_cat.id,
            "order_index": 3,
            "has_dynamic_form": True,
            "fields": [
                {"field_type": TaskFieldType.YES_NO, "field_label": "Any Staff Reported Illness?", "field_order": 1, "is_required": True},
                {"field_type": TaskFieldType.TEXT, "field_label": "Details and Action Taken", "field_order": 2, "is_required": False, "show_if": {"field_order": 1, "equals": True}}
            ]
        }
    ])

    # Category 5: Cleaning and Disinfection
    cleaning_cat = categories[4]
    tasks.extend([
        {
            "name": "Daily Kitchen Cleaning Check",
            "description": "Clean all surfaces, equipment, floors following cleaning schedule",
            "category_id": cleaning_cat.id,
            "order_index": 1,
            "has_dynamic_form": True,
            "fields": [
                {"field_type": TaskFieldType.YES_NO, "field_label": "Daily Cleaning Completed?", "field_order": 1, "is_required": True},
                {"field_type": TaskFieldType.TEXT, "field_label": "Areas Needing Attention", "field_order": 2, "is_required": False}
            ]
        },
        {
            "name": "Food Contact Surfaces Sanitization",
            "description": "Clean with detergent, rinse, and apply sanitizer",
            "category_id": cleaning_cat.id,
            "order_index": 2,
            "has_dynamic_form": True,
            "fields": [
                {"field_type": TaskFieldType.YES_NO, "field_label": "All Surfaces Sanitized?", "field_order": 1, "is_required": True}
            ]
        }
    ])

    # Category 6: Pest Control
    pest_cat = categories[5]
    tasks.extend([
        {
            "name": "Pest Control Device Check",
            "description": "Check devices are functional, clean fly killers, note any pest activity",
            "category_id": pest_cat.id,
            "order_index": 1,
            "has_dynamic_form": True,
            "fields": [
                {"field_type": TaskFieldType.YES_NO, "field_label": "All Devices Functional?", "field_order": 1, "is_required": True},
                {"field_type": TaskFieldType.YES_NO, "field_label": "Any Pest Activity Observed?", "field_order": 2, "is_required": True},
                {"field_type": TaskFieldType.TEXT, "field_label": "Details of Pest Activity", "field_order": 3, "is_required": False, "show_if": {"field_order": 2, "equals": True}},
                {"field_type": TaskFieldType.PHOTO, "field_label": "Photo Evidence", "field_order": 4, "is_required": False}
            ]
        }
    ])

    # Category 7: Food Storage and Handling
    storage_cat = categories[6]
    tasks.extend([
        {
            "name": "Stock Rotation Check (FIFO)",
            "description": "Check date labels, rotate stock, remove expired items",
            "category_id": storage_cat.id,
            "order_index": 1,
            "has_dynamic_form": True,
            "fields": [
                {"field_type": TaskFieldType.YES_NO, "field_label": "FIFO System Working Properly?", "field_order": 1, "is_required": True},
                {"field_type": TaskFieldType.YES_NO, "field_label": "Any Expired Items Found?", "field_order": 2, "is_required": True},
                {"field_type": TaskFieldType.TEXT, "field_label": "Expired Items Removed", "field_order": 3, "is_required": False, "show_if": {"field_order": 2, "equals": True}}
            ]
        },
        {
            "name": "Food Storage Separation Audit",
            "description": "Check storage areas maintain separation (raw below cooked, covered items)",
            "category_id": storage_cat.id,
            "order_index": 2,
            "has_dynamic_form": True,
            "fields": [
                {"field_type": TaskFieldType.YES_NO, "field_label": "Proper Separation Maintained?", "field_order": 1, "is_required": True},
                {"field_type": TaskFieldType.TEXT, "field_label": "Issues Found (if any)", "field_order": 2, "is_required": False}
            ]
        }
    ])

    # Category 8: Cross-Contamination Prevention
    cross_cat = categories[7]
    tasks.extend([
        {
            "name": "Color-Coded Equipment Check",
            "description": "Check boards, knives, and cloths are color-coded and used for designated purposes",
            "category_id": cross_cat.id,
            "order_index": 1,
            "has_dynamic_form": True,
            "fields": [
                {"field_type": TaskFieldType.YES_NO, "field_label": "Color-Coding Used Correctly?", "field_order": 1, "is_required": True}
            ]
        },
        {
            "name": "Separate Preparation Area Audit",
            "description": "Check physical separation or time separation is maintained",
            "category_id": cross_cat.id,
            "order_index": 2,
            "has_dynamic_form": True,
            "fields": [
                {"field_type": TaskFieldType.YES_NO, "field_label": "Separation Maintained?", "field_order": 1, "is_required": True}
            ]
        }
    ])

    # Category 9: Allergen Management
    allergen_cat = categories[8]
    tasks.extend([
        {
            "name": "Allergen Information Update",
            "description": "Verify allergen matrix is current and accurate for all 14 allergens",
            "category_id": allergen_cat.id,
            "order_index": 1,
            "has_dynamic_form": True,
            "fields": [
                {"field_type": TaskFieldType.YES_NO, "field_label": "Allergen Information Up-to-Date?", "field_order": 1, "is_required": True},
                {"field_type": TaskFieldType.TEXT, "field_label": "Menu Changes (if any)", "field_order": 2, "is_required": False}
            ]
        }
    ])

    # Category 10: Training Records
    training_cat = categories[9]
    tasks.extend([
        {
            "name": "Food Hygiene Training Verification",
            "description": "Check certificates are current and new staff are enrolled in training",
            "category_id": training_cat.id,
            "order_index": 1,
            "has_dynamic_form": True,
            "fields": [
                {"field_type": TaskFieldType.YES_NO, "field_label": "All Staff Certified?", "field_order": 1, "is_required": True},
                {"field_type": TaskFieldType.TEXT, "field_label": "Staff Names and Certificate Expiry", "field_order": 2, "is_required": False}
            ]
        }
    ])

    # Category 11: Equipment Maintenance
    equipment_cat = categories[10]
    tasks.extend([
        {
            "name": "Refrigeration Equipment Check",
            "description": "Check door seals, cleanliness, defrost cycles, and unusual noises",
            "category_id": equipment_cat.id,
            "order_index": 1,
            "has_dynamic_form": True,
            "fields": [
                {"field_type": TaskFieldType.YES_NO, "field_label": "All Equipment Operating Properly?", "field_order": 1, "is_required": True},
                {"field_type": TaskFieldType.TEXT, "field_label": "Issues Found (if any)", "field_order": 2, "is_required": False}
            ]
        }
    ])

    # Category 12: Waste Management
    waste_cat = categories[11]
    tasks.extend([
        {
            "name": "Waste Bin Cleaning",
            "description": "Empty, clean, and sanitize internal and external bins",
            "category_id": waste_cat.id,
            "order_index": 1,
            "has_dynamic_form": True,
            "fields": [
                {"field_type": TaskFieldType.YES_NO, "field_label": "All Bins Cleaned?", "field_order": 1, "is_required": True}
            ]
        },
        {
            "name": "Waste Storage Area Inspection",
            "description": "Verify area is clean, bins are lidded, no pest attraction, no overflow",
            "category_id": waste_cat.id,
            "order_index": 2,
            "has_dynamic_form": True,
            "fields": [
                {"field_type": TaskFieldType.YES_NO, "field_label": "Storage Area Acceptable?", "field_order": 1, "is_required": True}
            ]
        }
    ])

    # Category 13: Water Supply and Drainage
    water_cat = categories[12]
    tasks.extend([
        {
            "name": "Water Temperature Check",
            "description": "Check hot water reaches adequate temperature for effective hand washing",
            "category_id": water_cat.id,
            "order_index": 1,
            "has_dynamic_form": True,
            "fields": [
                {"field_type": TaskFieldType.YES_NO, "field_label": "Hot Water Adequate?", "field_order": 1, "is_required": True},
                {"field_type": TaskFieldType.TEMPERATURE, "field_label": "Temperature (°C)", "field_order": 2, "is_required": False, "validation_rules": {"min": 0, "max": 100}}
            ]
        }
    ])

    # Category 14: Structure and Facilities
    structure_cat = categories[13]
    tasks.extend([
        {
            "name": "Premises Condition Inspection",
            "description": "Check for cracks, holes, peeling paint, water damage that could harbor pests",
            "category_id": structure_cat.id,
            "order_index": 1,
            "has_dynamic_form": True,
            "fields": [
                {"field_type": TaskFieldType.YES_NO, "field_label": "Premises in Good Condition?", "field_order": 1, "is_required": True},
                {"field_type": TaskFieldType.TEXT, "field_label": "Repairs Needed (if any)", "field_order": 2, "is_required": False},
                {"field_type": TaskFieldType.PHOTO, "field_label": "Photo Evidence", "field_order": 3, "is_required": False}
            ]
        }
    ])

    # Category 15: Supplier and Traceability
    supplier_cat = categories[14]
    tasks.extend([
        {
            "name": "Supplier Approval Review",
            "description": "Verify all suppliers are approved, have adequate food safety credentials",
            "category_id": supplier_cat.id,
            "order_index": 1,
            "has_dynamic_form": True,
            "fields": [
                {"field_type": TaskFieldType.YES_NO, "field_label": "All Suppliers Approved?", "field_order": 1, "is_required": True},
                {"field_type": TaskFieldType.TEXT, "field_label": "Supplier List Review Notes", "field_order": 2, "is_required": False}
            ]
        }
    ])

    # Category 16: Documentation and Record Keeping
    docs_cat = categories[15]
    tasks.extend([
        {
            "name": "Daily Records Completion Check",
            "description": "Check temperature logs, cleaning schedules, and delivery records are filled in",
            "category_id": docs_cat.id,
            "order_index": 1,
            "has_dynamic_form": True,
            "fields": [
                {"field_type": TaskFieldType.YES_NO, "field_label": "All Daily Records Complete?", "field_order": 1, "is_required": True},
                {"field_type": TaskFieldType.TEXT, "field_label": "Missing Records (if any)", "field_order": 2, "is_required": False}
            ]
        }
    ])

    # Create all tasks and fields
    for task_data in tasks:
        fields_data = task_data.pop("fields", [])
        task = Task(**task_data)
        db.add(task)
        db.flush()

        print(f"  Created task: {task.name} (ID: {task.id})")

        # Create fields for this task
        count_field_id = None
        for field_data in fields_data:
            # If this is a number field that might be referenced by a repeating group, save its ID
            if field_data["field_type"] == TaskFieldType.NUMBER and "Number of" in field_data["field_label"]:
                field = TaskField(task_id=task.id, **field_data)
                db.add(field)
                db.flush()
                count_field_id = field.id
                print(f"    Created field: {field.field_label} (ID: {field.id})")
            # If this is a repeating group, reference the count field
            elif field_data["field_type"] == TaskFieldType.REPEATING_GROUP:
                if count_field_id and field_data.get("validation_rules", {}).get("repeat_count_field_id") == "will_be_set":
                    field_data["validation_rules"]["repeat_count_field_id"] = count_field_id
                field = TaskField(task_id=task.id, **field_data)
                db.add(field)
                db.flush()
                print(f"    Created field: {field.field_label} (ID: {field.id}, references count field {count_field_id})")
            else:
                field = TaskField(task_id=task.id, **field_data)
                db.add(field)
                db.flush()
                print(f"    Created field: {field.field_label} (ID: {field.id})")


def main():
    db = SessionLocal()
    try:
        print("Starting EHO category and task seeding...")
        print("=" * 80)

        # Create categories as global (no organization_id)
        categories = create_eho_categories(db, organization_id=None)

        print("\n" + "=" * 80)
        print("Creating tasks and fields...")
        print("=" * 80 + "\n")

        # Create tasks and fields
        create_tasks_and_fields(db, categories)

        # Commit all changes
        db.commit()

        print("\n" + "=" * 80)
        print("✓ EHO categories, tasks, and fields created successfully!")
        print("=" * 80)
        print(f"\nCreated {len(categories)} categories")
        print("Created approximately 30+ tasks with dynamic fields")
        print("\nNext step: Regenerate today's checklists to include new categories")

    except Exception as e:
        db.rollback()
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
