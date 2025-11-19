"""
Add new super admin user
Email: test@test.com
Password: test123

This script creates a new super admin that can be used for testing.
"""
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models.user import User, UserRole


def add_super_admin():
    """Add a new super admin user."""
    print("\n" + "="*70)
    print("Adding New Super Admin")
    print("="*70)

    # Create all tables (in case they don't exist)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Configuration
        ADMIN_EMAIL = "test@test.com"
        ADMIN_PASSWORD = "test123"

        # Check if super admin already exists
        existing_admin = db.query(User).filter(
            User.email == ADMIN_EMAIL
        ).first()

        if existing_admin:
            print(f"\n[!] User with email {ADMIN_EMAIL} already exists!")
            print(f"   Account created: {existing_admin.created_at}")
            print(f"   Role: {existing_admin.role.value}")
            print(f"   Status: {'Active' if existing_admin.is_active else 'Inactive'}")
            print("\n" + "="*70 + "\n")
            return

        # Create super admin user
        print(f"\n[*] Creating super admin user...")
        print(f"   Email: {ADMIN_EMAIL}")
        print(f"   Password: {ADMIN_PASSWORD}")

        super_admin = User(
            email=ADMIN_EMAIL,
            hashed_password=get_password_hash(ADMIN_PASSWORD),
            first_name="Test",
            last_name="Admin",
            role=UserRole.SUPER_ADMIN,
            organization_id=None,  # Super admin not tied to any organization
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        db.add(super_admin)
        db.commit()
        db.refresh(super_admin)

        print("[OK] Super admin user created successfully!")
        print(f"   User ID: {super_admin.id}")
        print(f"   Role: {super_admin.role.value}")
        print(f"   Created: {super_admin.created_at}")

        print("\n" + "="*70)
        print("LOGIN CREDENTIALS")
        print("="*70)
        print(f"   Organization Code: vig (or any valid org code)")
        print(f"   Email: {ADMIN_EMAIL}")
        print(f"   Password: {ADMIN_PASSWORD}")
        print(f"   Login URL: http://localhost:4200/login")
        print("\n" + "="*70 + "\n")

    except Exception as e:
        db.rollback()
        print(f"\n[ERROR] Error creating super admin: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    add_super_admin()
