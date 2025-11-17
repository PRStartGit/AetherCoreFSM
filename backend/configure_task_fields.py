"""
Configure dynamic task fields for all tasks based on their type and name.
This script adds proper field configurations (yes/no, photo, temperature, etc.)
to tasks that are marked as having dynamic forms but don't have fields configured.
"""
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.task import Task
from app.models.task_field import TaskField


def configure_task_fields():
    """Configure dynamic fields for all tasks based on their names and categories."""
    db = SessionLocal()

    try:
        # Get all tasks that have dynamic forms but no fields
        tasks = db.query(Task).filter(Task.has_dynamic_form == True).all()

        print(f"Found {len(tasks)} tasks with dynamic forms enabled")
        print("=" * 80)

        configured_count = 0
        skipped_count = 0

        for task in tasks:
            # Check if task already has fields
            existing_fields = db.query(TaskField).filter(TaskField.task_id == task.id).count()
            if existing_fields > 0:
                print(f"✓ Skipping '{task.name}' - already has {existing_fields} fields")
                skipped_count += 1
                continue

            # Configure fields based on task name/type
            fields_config = get_field_config_for_task(task)

            if not fields_config:
                print(f"⚠ Skipping '{task.name}' - no field configuration found")
                skipped_count += 1
                continue

            # Create fields
            for field_data in fields_config:
                field = TaskField(
                    task_id=task.id,
                    field_type=field_data['field_type'],
                    field_label=field_data['field_label'],
                    field_order=field_data['field_order'],
                    is_required=field_data.get('is_required', True),
                    validation_rules=field_data.get('validation_rules'),
                    options=field_data.get('options')
                )
                db.add(field)

            db.commit()
            configured_count += 1
            print(f"✓ Configured {len(fields_config)} fields for '{task.name}'")

        print("=" * 80)
        print(f"\nSummary:")
        print(f"  - Tasks configured: {configured_count}")
        print(f"  - Tasks skipped: {skipped_count}")
        print(f"  - Total tasks: {len(tasks)}")

    except Exception as e:
        db.rollback()
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


def get_field_config_for_task(task: Task) -> list:
    """
    Return field configuration based on task name and type.
    Each task gets appropriate field types (yes/no, photo, temperature, number, etc.)
    """
    name_lower = task.name.lower()

    # TEMPERATURE CHECKS
    if 'temperature' in name_lower:
        if 'fridge' in name_lower:
            return [
                {
                    'field_type': 'temperature',
                    'field_label': 'Fridge Temperature (°C)',
                    'field_order': 1,
                    'is_required': True,
                    'validation_rules': {
                        'min': -5,
                        'max': 8,
                        'create_defect_if': 'out_of_range'
                    }
                },
                {
                    'field_type': 'photo',
                    'field_label': 'Photo of Temperature Display',
                    'field_order': 2,
                    'is_required': False
                },
                {
                    'field_type': 'text',
                    'field_label': 'Notes',
                    'field_order': 3,
                    'is_required': False
                }
            ]
        elif 'freezer' in name_lower:
            return [
                {
                    'field_type': 'temperature',
                    'field_label': 'Freezer Temperature (°C)',
                    'field_order': 1,
                    'is_required': True,
                    'validation_rules': {
                        'min': -25,
                        'max': -18,
                        'create_defect_if': 'out_of_range'
                    }
                },
                {
                    'field_type': 'photo',
                    'field_label': 'Photo of Temperature Display',
                    'field_order': 2,
                    'is_required': False
                },
                {
                    'field_type': 'text',
                    'field_label': 'Notes',
                    'field_order': 3,
                    'is_required': False
                }
            ]
        else:
            # Generic temperature check
            return [
                {
                    'field_type': 'temperature',
                    'field_label': 'Temperature (°C)',
                    'field_order': 1,
                    'is_required': True,
                    'validation_rules': {
                        'min': -30,
                        'max': 90
                    }
                },
                {
                    'field_type': 'photo',
                    'field_label': 'Photo Evidence',
                    'field_order': 2,
                    'is_required': False
                }
            ]

    # CLEANING TASKS
    elif 'clean' in name_lower or 'sanitize' in name_lower or 'disinfect' in name_lower:
        return [
            {
                'field_type': 'yes_no',
                'field_label': 'Area Cleaned?',
                'field_order': 1,
                'is_required': True
            },
            {
                'field_type': 'yes_no',
                'field_label': 'Cleaning Products Used?',
                'field_order': 2,
                'is_required': True
            },
            {
                'field_type': 'photo',
                'field_label': 'Photo of Cleaned Area',
                'field_order': 3,
                'is_required': False
            },
            {
                'field_type': 'text',
                'field_label': 'Notes',
                'field_order': 4,
                'is_required': False
            }
        ]

    # EQUIPMENT CHECKS
    elif 'equipment' in name_lower or 'machinery' in name_lower:
        return [
            {
                'field_type': 'yes_no',
                'field_label': 'Equipment in Good Working Order?',
                'field_order': 1,
                'is_required': True
            },
            {
                'field_type': 'yes_no',
                'field_label': 'Any Damage Visible?',
                'field_order': 2,
                'is_required': True
            },
            {
                'field_type': 'photo',
                'field_label': 'Photo of Equipment',
                'field_order': 3,
                'is_required': False
            },
            {
                'field_type': 'text',
                'field_label': 'Issues Found',
                'field_order': 4,
                'is_required': False
            }
        ]

    # OPENING CHECKLIST
    elif 'opening' in name_lower:
        return [
            {
                'field_type': 'yes_no',
                'field_label': 'Lights Working?',
                'field_order': 1,
                'is_required': True
            },
            {
                'field_type': 'yes_no',
                'field_label': 'Premises Secure?',
                'field_order': 2,
                'is_required': True
            },
            {
                'field_type': 'yes_no',
                'field_label': 'No Pest Evidence?',
                'field_order': 3,
                'is_required': True
            },
            {
                'field_type': 'text',
                'field_label': 'Additional Notes',
                'field_order': 4,
                'is_required': False
            }
        ]

    # CLOSING CHECKLIST
    elif 'closing' in name_lower:
        return [
            {
                'field_type': 'yes_no',
                'field_label': 'All Equipment Turned Off?',
                'field_order': 1,
                'is_required': True
            },
            {
                'field_type': 'yes_no',
                'field_label': 'All Doors Locked?',
                'field_order': 2,
                'is_required': True
            },
            {
                'field_type': 'yes_no',
                'field_label': 'Alarm Set?',
                'field_order': 3,
                'is_required': True
            },
            {
                'field_type': 'text',
                'field_label': 'Additional Notes',
                'field_order': 4,
                'is_required': False
            }
        ]

    # PEST CONTROL
    elif 'pest' in name_lower:
        return [
            {
                'field_type': 'yes_no',
                'field_label': 'Evidence of Pest Activity?',
                'field_order': 1,
                'is_required': True
            },
            {
                'field_type': 'dropdown',
                'field_label': 'Type of Pest (if any)',
                'field_order': 2,
                'is_required': False,
                'options': ['None', 'Rodents', 'Insects', 'Birds', 'Other']
            },
            {
                'field_type': 'photo',
                'field_label': 'Photo Evidence',
                'field_order': 3,
                'is_required': False
            },
            {
                'field_type': 'text',
                'field_label': 'Action Taken',
                'field_order': 4,
                'is_required': False
            }
        ]

    # WASTE MANAGEMENT
    elif 'waste' in name_lower or 'bin' in name_lower or 'garbage' in name_lower:
        return [
            {
                'field_type': 'yes_no',
                'field_label': 'Waste Bins Emptied?',
                'field_order': 1,
                'is_required': True
            },
            {
                'field_type': 'yes_no',
                'field_label': 'Recycling Separated Correctly?',
                'field_order': 2,
                'is_required': True
            },
            {
                'field_type': 'yes_no',
                'field_label': 'Bin Area Clean?',
                'field_order': 3,
                'is_required': True
            },
            {
                'field_type': 'text',
                'field_label': 'Notes',
                'field_order': 4,
                'is_required': False
            }
        ]

    # FOOD SAFETY CHECKS
    elif 'food' in name_lower or 'hygiene' in name_lower:
        return [
            {
                'field_type': 'yes_no',
                'field_label': 'Food Storage Correct?',
                'field_order': 1,
                'is_required': True
            },
            {
                'field_type': 'yes_no',
                'field_label': 'Date Labels Present?',
                'field_order': 2,
                'is_required': True
            },
            {
                'field_type': 'yes_no',
                'field_label': 'No Cross-Contamination Risk?',
                'field_order': 3,
                'is_required': True
            },
            {
                'field_type': 'photo',
                'field_label': 'Photo Evidence',
                'field_order': 4,
                'is_required': False
            },
            {
                'field_type': 'text',
                'field_label': 'Issues Found',
                'field_order': 5,
                'is_required': False
            }
        ]

    # DELIVERY CHECKS
    elif 'delivery' in name_lower or 'receiving' in name_lower:
        return [
            {
                'field_type': 'text',
                'field_label': 'Supplier Name',
                'field_order': 1,
                'is_required': True
            },
            {
                'field_type': 'temperature',
                'field_label': 'Delivery Temperature (if applicable)',
                'field_order': 2,
                'is_required': False,
                'validation_rules': {
                    'min': -5,
                    'max': 8
                }
            },
            {
                'field_type': 'yes_no',
                'field_label': 'Packaging Intact?',
                'field_order': 3,
                'is_required': True
            },
            {
                'field_type': 'yes_no',
                'field_label': 'Quality Acceptable?',
                'field_order': 4,
                'is_required': True
            },
            {
                'field_type': 'photo',
                'field_label': 'Photo of Delivery',
                'field_order': 5,
                'is_required': False
            }
        ]

    # STAFF CHECKS
    elif 'staff' in name_lower or 'uniform' in name_lower or 'personal' in name_lower:
        return [
            {
                'field_type': 'yes_no',
                'field_label': 'Staff in Clean Uniforms?',
                'field_order': 1,
                'is_required': True
            },
            {
                'field_type': 'yes_no',
                'field_label': 'Hair Nets/Hats Worn?',
                'field_order': 2,
                'is_required': True
            },
            {
                'field_type': 'yes_no',
                'field_label': 'No Jewelry Worn?',
                'field_order': 3,
                'is_required': True
            },
            {
                'field_type': 'text',
                'field_label': 'Notes',
                'field_order': 4,
                'is_required': False
            }
        ]

    # FIRE SAFETY
    elif 'fire' in name_lower or 'extinguisher' in name_lower or 'alarm' in name_lower:
        return [
            {
                'field_type': 'yes_no',
                'field_label': 'Equipment Present?',
                'field_order': 1,
                'is_required': True
            },
            {
                'field_type': 'yes_no',
                'field_label': 'In Good Condition?',
                'field_order': 2,
                'is_required': True
            },
            {
                'field_type': 'yes_no',
                'field_label': 'Inspection Date Current?',
                'field_order': 3,
                'is_required': True
            },
            {
                'field_type': 'photo',
                'field_label': 'Photo of Inspection Tag',
                'field_order': 4,
                'is_required': False
            },
            {
                'field_type': 'text',
                'field_label': 'Notes',
                'field_order': 5,
                'is_required': False
            }
        ]

    # GENERIC CHECK (DEFAULT)
    else:
        return [
            {
                'field_type': 'yes_no',
                'field_label': 'Task Completed Successfully?',
                'field_order': 1,
                'is_required': True
            },
            {
                'field_type': 'photo',
                'field_label': 'Photo Evidence',
                'field_order': 2,
                'is_required': False
            },
            {
                'field_type': 'text',
                'field_label': 'Notes',
                'field_order': 3,
                'is_required': False
            }
        ]


if __name__ == '__main__':
    print("=" * 80)
    print("Configuring Dynamic Task Fields")
    print("=" * 80)
    configure_task_fields()
    print("\n✅ Configuration complete!")
