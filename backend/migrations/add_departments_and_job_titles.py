"""
Database migration script to add departments and job titles.

This script adds:
1. Department enum and column to users table
2. Job title enum and column to users table
3. Allocated departments array to tasks table

Run this script to update your existing database.
"""

from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:changeme@localhost:5432/zynthio")

# If using Docker, update the host
if "localhost" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("localhost", "localhost")


def upgrade_database():
    """Apply the migration."""
    engine = create_engine(DATABASE_URL)

    with engine.connect() as conn:
        print("Starting migration...")

        # 1. Create Department ENUM type
        print("Creating Department enum...")
        conn.execute(text("""
            DO $$ BEGIN
                CREATE TYPE department AS ENUM ('management', 'boh', 'foh');
            EXCEPTION
                WHEN duplicate_object THEN null;
            END $$;
        """))
        conn.commit()

        # 2. Create JobTitle ENUM type
        print("Creating JobTitle enum...")
        conn.execute(text("""
            DO $$ BEGIN
                CREATE TYPE jobtitle AS ENUM (
                    'general_manager',
                    'assistant_manager',
                    'head_chef',
                    'sous_chef',
                    'supervisor',
                    'team_member'
                );
            EXCEPTION
                WHEN duplicate_object THEN null;
            END $$;
        """))
        conn.commit()

        # 3. Add department column to users table
        print("Adding department column to users...")
        conn.execute(text("""
            DO $$ BEGIN
                ALTER TABLE users ADD COLUMN department department NULL;
            EXCEPTION
                WHEN duplicate_column THEN null;
            END $$;
        """))
        conn.commit()

        # 4. Add job_title column to users table
        print("Adding job_title column to users...")
        conn.execute(text("""
            DO $$ BEGIN
                ALTER TABLE users ADD COLUMN job_title jobtitle NULL;
            EXCEPTION
                WHEN duplicate_column THEN null;
            END $$;
        """))
        conn.commit()

        # 5. Add allocated_departments column to tasks table
        print("Adding allocated_departments column to tasks...")
        conn.execute(text("""
            DO $$ BEGIN
                ALTER TABLE tasks ADD COLUMN allocated_departments VARCHAR[] NULL;
            EXCEPTION
                WHEN duplicate_column THEN null;
            END $$;
        """))
        conn.commit()

        print("Migration completed successfully!")


def downgrade_database():
    """Rollback the migration."""
    engine = create_engine(DATABASE_URL)

    with engine.connect() as conn:
        print("Rolling back migration...")

        # Remove columns
        print("Removing allocated_departments column from tasks...")
        conn.execute(text("ALTER TABLE tasks DROP COLUMN IF EXISTS allocated_departments"))
        conn.commit()

        print("Removing job_title column from users...")
        conn.execute(text("ALTER TABLE users DROP COLUMN IF EXISTS job_title"))
        conn.commit()

        print("Removing department column from users...")
        conn.execute(text("ALTER TABLE users DROP COLUMN IF EXISTS department"))
        conn.commit()

        # Drop enum types
        print("Dropping JobTitle enum...")
        conn.execute(text("DROP TYPE IF EXISTS jobtitle"))
        conn.commit()

        print("Dropping Department enum...")
        conn.execute(text("DROP TYPE IF EXISTS department"))
        conn.commit()

        print("Rollback completed!")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "downgrade":
        downgrade_database()
    else:
        upgrade_database()
