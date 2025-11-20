import sys
sys.path.insert(0, "/app")

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.checklist import Checklist, ChecklistItem
from app.models.task import Task

db = SessionLocal()

try:
    # Get all checklists that have no items
    checklists = db.query(Checklist).all()
    
    created_count = 0
    
    for checklist in checklists:
        # Check if this checklist already has items
        existing_items = db.query(ChecklistItem).filter(
            ChecklistItem.checklist_id == checklist.id
        ).count()
        
        if existing_items > 0:
            continue  # Skip checklists that already have items
        
        # Get tasks for this category
        tasks = db.query(Task).filter(
            Task.category_id == checklist.category_id,
            Task.is_active == True
        ).order_by(Task.order_index).all()
        
        # Create checklist items for each task
        for task in tasks:
            item = ChecklistItem(
                checklist_id=checklist.id,
                task_id=task.id,
                item_name=task.name,
                form_data=None,
                is_completed=False,
                completed_at=None,
                completed_by=None
            )
            db.add(item)
            created_count += 1
        
        print(f"Created {len(tasks)} items for checklist {checklist.id}")
    
    db.commit()
    print(f"\n✅ Successfully created {created_count} checklist items")
    
except Exception as e:
    db.rollback()
    print(f"❌ Error: {str(e)}")
    raise
finally:
    db.close()
