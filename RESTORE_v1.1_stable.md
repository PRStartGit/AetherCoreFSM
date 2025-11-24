# Database Restoration Guide - v1.1 Stable

## Backup Information
- **Version**: v1.1-stable
- **Date**: 2025-11-24
- **File**: database_backup_v1.1_stable_20251124_173549.sql.gz
- **Size**: 19KB (compressed), 119KB (uncompressed)
- **Git Branch**: v1.1-stable-dynamic-forms-working
- **Git Tag**: v1.1-stable

## What's Included
- 26 categories (Scotland Food Hygiene Regulations compliant)
- 68 tasks with dynamic forms
- 213 task fields (all types: yes_no, text, number, temperature, photo, dropdown, repeating_group)
- All repeating group fields correctly linked to count fields
- Field types normalized (lowercase with underscores)
- Allocated departments arrays fixed
- 2 sites configured
- 52 active checklists

## How to Restore

### 1. Stop all services
```bash
cd /root/AetherCoreFSM
docker compose down
```

### 2. Uncompress the backup
```bash
gunzip database_backup_v1.1_stable_20251124_173549.sql.gz
```

### 3. Start only the database
```bash
docker compose up -d database
sleep 5  # Wait for database to be ready
```

### 4. Drop and recreate the database
```bash
docker compose exec database psql -U postgres -c "DROP DATABASE IF EXISTS zynthio;"
docker compose exec database psql -U postgres -c "CREATE DATABASE zynthio;"
```

### 5. Restore from backup
```bash
cat database_backup_v1.1_stable_20251124_173549.sql | docker compose exec -T database psql -U postgres zynthio
```

### 6. Start all services
```bash
docker compose up -d
```

### 7. Verify restoration
```bash
docker compose exec backend python3 -c "
from app.core.database import SessionLocal
from app.models.task import Task
from app.models.task_field import TaskField

db = SessionLocal()
tasks = db.query(Task).filter(Task.has_dynamic_form == True).count()
fields = db.query(TaskField).count()
print(f'Tasks with dynamic forms: {tasks}')
print(f'Total task fields: {fields}')
db.close()
"
```

Expected output:
- Tasks with dynamic forms: 68
- Total task fields: 213

## Git Checkout
To get the code matching this database:
```bash
git fetch origin
git checkout v1.1-stable-dynamic-forms-working
# or
git checkout v1.1-stable
```

## Key Features Working
- ✅ Dynamic form rendering (all field types)
- ✅ Repeating group expansion (linked to count fields)
- ✅ Locked missed checklists (past due date)
- ✅ Form submission scroll position fix
- ✅ Photo upload for task fields
- ✅ Temperature validation with auto-defect creation
- ✅ Conditional field display (show_if logic)
