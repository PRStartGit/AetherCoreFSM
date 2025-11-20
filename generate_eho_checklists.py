import sys
sys.path.insert(0, "/app")

from datetime import datetime, timedelta, date
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.site import Site
from app.models.category import Category, ChecklistFrequency
from app.models.checklist import Checklist, ChecklistStatus
from app.models.task import Task

db = SessionLocal()

try:
    # Get all active sites
    sites = db.query(Site).filter(Site.is_active == True).all()
    print(f"Found {len(sites)} active sites")
    
    # Get all new EHO categories
    eho_categories = db.query(Category).filter(
        Category.id >= 126,  # New EHO categories start at ID 126
        Category.is_active == True
    ).all()
    
    print(f"Found {len(eho_categories)} EHO categories")
    
    today = date.today()
    created_count = 0
    
    for site in sites:
        print(f"\nProcessing site: {site.name} (ID: {site.id})")
        
        for category in eho_categories:
            # Determine checklist dates based on frequency
            checklist_dates = []
            
            if category.frequency == ChecklistFrequency.DAILY:
                # Create for today
                checklist_dates.append(today)
            elif category.frequency == ChecklistFrequency.WEEKLY:
                # Create for this week (Monday)
                checklist_dates.append(today)
            elif category.frequency == ChecklistFrequency.MONTHLY:
                # Create for this month (1st of month)
                checklist_dates.append(today.replace(day=1))
            elif category.frequency == ChecklistFrequency.QUARTERLY:
                # Create for this quarter and next quarter
                # Q1: Jan 1, Q2: Apr 1, Q3: Jul 1, Q4: Oct 1
                current_month = today.month
                if current_month <= 3:
                    quarter_start = date(today.year, 1, 1)
                    next_quarter = date(today.year, 4, 1)
                elif current_month <= 6:
                    quarter_start = date(today.year, 4, 1)
                    next_quarter = date(today.year, 7, 1)
                elif current_month <= 9:
                    quarter_start = date(today.year, 7, 1)
                    next_quarter = date(today.year, 10, 1)
                else:
                    quarter_start = date(today.year, 10, 1)
                    next_quarter = date(today.year + 1, 1, 1)
                
                checklist_dates.append(quarter_start)
                checklist_dates.append(next_quarter)
            
            # Create checklists
            for checklist_date in checklist_dates:
                # Check if checklist already exists
                existing = db.query(Checklist).filter(
                    Checklist.site_id == site.id,
                    Checklist.category_id == category.id,
                    Checklist.checklist_date == checklist_date
                ).first()
                
                if not existing:
                    # Get tasks for this category
                    tasks = db.query(Task).filter(
                        Task.category_id == category.id,
                        Task.is_active == True
                    ).all()
                    
                    checklist = Checklist(
                        site_id=site.id,
                        category_id=category.id,
                        checklist_date=checklist_date,
                        status=ChecklistStatus.PENDING,
                        total_items=len(tasks),
                        completed_items=0,
                        completion_percentage=0.0
                    )
                    db.add(checklist)
                    created_count += 1
                    print(f"  Created {category.name} checklist for {checklist_date}")
    
    db.commit()
    print(f"\n✅ Successfully created {created_count} checklists")
    
except Exception as e:
    db.rollback()
    print(f"❌ Error: {str(e)}")
    raise
finally:
    db.close()
