import json
from datetime import time
from app.core.database import SessionLocal
from app.models.category import Category
from app.models.task import Task
from app.models.task_field import TaskField

def make_time(time_str):
    """Convert time string HH:MM:SS to time object"""
    if not time_str:
        return None
    h, m, s = map(int, time_str.split(':'))
    return time(h, m, s)

def import_config(config_data):
    """Import checklist configuration from JSON"""
    db = SessionLocal()
    
    try:
        print('='*80)
        print('IMPORTING CHECKLIST CONFIGURATION')
        print('='*80)
        print()
        
        categories_created = 0
        tasks_created = 0
        fields_created = 0
        
        for cat_data in config_data['categories']:
            # Create category
            category = Category(
                name=cat_data['name'],
                description=cat_data['description'],
                icon=cat_data.get('icon'),
                frequency=cat_data['frequency'],
                opens_at=make_time(cat_data.get('opens_at')),
                closes_at=make_time(cat_data.get('closes_at')),
                is_global=cat_data.get('is_global', True),
                is_active=cat_data.get('is_active', True)
            )
            db.add(category)
            db.flush()
            categories_created += 1
            
            print(f'✓ Created category: {category.name}')
            
            # Create tasks for this category
            for task_data in cat_data.get('tasks', []):
                task = Task(
                    category_id=category.id,
                    name=task_data['name'],
                    description=task_data.get('description'),
                    priority=task_data.get('priority', 'medium'),
                    order_index=task_data.get('order_index', 1),
                    is_active=task_data.get('is_active', True),
                    has_dynamic_form=task_data.get('has_dynamic_form', True),
                    allocated_departments=task_data.get('allocated_departments')
                )
                db.add(task)
                db.flush()
                tasks_created += 1
                
                # Create fields for this task
                for field_data in task_data.get('fields', []):
                    field = TaskField(
                        task_id=task.id,
                        field_type=field_data['field_type'],
                        field_label=field_data['field_label'],
                        field_order=field_data['field_order'],
                        is_required=field_data.get('is_required', False),
                        validation_rules=field_data.get('validation_rules'),
                        options=field_data.get('options'),
                        show_if=field_data.get('show_if')
                    )
                    db.add(field)
                    fields_created += 1
                
            print(f'  └─ {len(task_data.get("fields", []))} tasks created')
        
        db.commit()
        
        print()
        print('='*80)
        print('IMPORT COMPLETE')
        print(f'  Categories: {categories_created}')
        print(f'  Tasks: {tasks_created}')
        print(f'  Fields: {fields_created}')
        print('='*80)
        
        return categories_created, tasks_created, fields_created
        
    except Exception as e:
        db.rollback()
        print(f'ERROR: {str(e)}')
        raise
    finally:
        db.close()

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python import_checklists.py <config_file.json>')
        sys.exit(1)
    
    with open(sys.argv[1], 'r') as f:
        config = json.load(f)
    
    import_config(config)
