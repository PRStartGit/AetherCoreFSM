"""
Add opens_at column to categories table.

Run with: python add_opens_at_migration.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from app.core.database import SessionLocal, engine

def run_migration():
    """Add opens_at column to categories table."""
    db = SessionLocal()

    try:
        print("🔄 Adding 'opens_at' column to categories table...")

        # Check if column already exists
        result = db.execute(text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name='categories' AND column_name='opens_at'
        """))

        if result.fetchone():
            print("✅ Column 'opens_at' already exists. Skipping migration.")
            return

        # Add the column
        db.execute(text("""
            ALTER TABLE categories
            ADD COLUMN opens_at TIME
        """))

        db.commit()
        print("✅ Successfully added 'opens_at' column to categories table!")

    except Exception as e:
        print(f"❌ Error during migration: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    run_migration()
