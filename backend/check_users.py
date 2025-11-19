"""
Check what users exist in the database
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.user import User
from app.models.organization import Organization


def check_users():
    """List all users in the database."""
    print("\n" + "="*70)
    print("DATABASE USERS CHECK")
    print("="*70)

    db = SessionLocal()

    try:
        # Get all organizations
        orgs = db.query(Organization).all()
        print(f"\n[ORGANIZATIONS] Found {len(orgs)} organizations:")
        for org in orgs:
            print(f"   - {org.name} (org_id: {org.org_id}, id: {org.id})")

        # Get all users
        users = db.query(User).all()
        print(f"\n[USERS] Found {len(users)} users:")
        for user in users:
            org_name = "None (Super Admin)" if user.organization_id is None else f"Org ID: {user.organization_id}"
            print(f"\n   Email: {user.email}")
            print(f"   Name: {user.first_name} {user.last_name}")
            print(f"   Role: {user.role.value}")
            print(f"   Organization: {org_name}")
            print(f"   Active: {user.is_active}")
            print(f"   User ID: {user.id}")

        print("\n" + "="*70 + "\n")

    except Exception as e:
        print(f"\n[ERROR] Error checking users: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    check_users()
