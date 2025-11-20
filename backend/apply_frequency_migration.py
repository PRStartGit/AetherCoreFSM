"""
Apply EHO-compliant frequency enum values to the database
"""
import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:changeme@localhost:5432/zynthio")

# Parse DATABASE_URL for psycopg2
# Format: postgresql://user:password@host:port/database
url_parts = DATABASE_URL.replace("postgresql://", "").split("@")
user_pass = url_parts[0].split(":")
host_db = url_parts[1].split("/")
host_port = host_db[0].split(":")

conn_params = {
    "user": user_pass[0],
    "password": user_pass[1] if len(user_pass) > 1 else "",
    "host": host_port[0],
    "port": host_port[1] if len(host_port) > 1 else "5432",
    "database": host_db[1] if len(host_db) > 1 else "zynthio"
}

try:
    # Connect to database
    conn = psycopg2.connect(**conn_params)
    conn.autocommit = True
    cursor = conn.cursor()
    
    print("Connected to database successfully")
    print("Adding new frequency enum values...")
    
    # Add new enum values
    new_values = [
        'quarterly',
        'every_2_hours',
        'per_batch',
        'per_delivery',
        'continuous',
        'as_needed'
    ]
    
    for value in new_values:
        try:
            cursor.execute(f"ALTER TYPE checklistfrequency ADD VALUE IF NOT EXISTS '{value}'")
            print(f"✓ Added enum value: {value}")
        except Exception as e:
            print(f"✗ Error adding {value}: {e}")
    
    print("\n✅ Migration completed successfully!")
    
    # Verify the enum values
    cursor.execute("""
        SELECT e.enumlabel 
        FROM pg_enum e
        JOIN pg_type t ON e.enumtypid = t.oid
        WHERE t.typname = 'checklistfrequency'
        ORDER BY e.enumsortorder
    """)
    
    print("\nCurrent enum values:")
    for row in cursor.fetchall():
        print(f"  - {row[0]}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
    raise
