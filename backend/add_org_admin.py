"""
Add a new organization admin user
Email: admin@vig.com
Password: admin123
Organization: vig
"""
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.organization import Organization


def add_org_admin():
    """Add a new org admin user."""
    print("\n" + "="*70)
    print("Adding New Organization Admin")
    print("="*70)

    db = SessionLocal()

    try:
        # Configuration
        ADMIN_EMAIL = "admin@vig.com"
        ADMIN_PASSWORD = "admin123"
        ORG_CODE = "vig"

        # Find organization
        org = db.query(Organization).filter(
            Organization.org_id == ORG_CODE
        ).first()

        if not org:
            print(f"\n[ERROR] Organization with code '{ORG_CODE}' not found!")
            return

        print(f"\n[OK] Found organization: {org.name} (ID: {org.id})")

        # Check if user already exists
        existing_user = db.query(User).filter(
            User.email == ADMIN_EMAIL
        ).first()

        if existing_user:
            print(f"\n[!] User with email {ADMIN_EMAIL} already exists!")
            print(f"   Account created: {existing_user.created_at}")
            print(f"   Role: {existing_user.role.value}")
            print(f"   Status: {'Active' if existing_user.is_active else 'Inactive'}")
            print("\n" + "="*70 + "\n")
            return

        # Create org admin user
        print(f"\n[*] Creating organization admin user...")
        print(f"   Email: {ADMIN_EMAIL}")
        print(f"   Password: {ADMIN_PASSWORD}")
        print(f"   Organization: {org.name}")

        org_admin = User(
            email=ADMIN_EMAIL,
            hashed_password=get_password_hash(ADMIN_PASSWORD),
            first_name="VIG",
            last_name="Admin",
            role=UserRole.ORG_ADMIN,
            organization_id=org.id,
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        db.add(org_admin)
        db.commit()
        db.refresh(org_admin)

        print("[OK] Organization admin user created successfully!")
        print(f"   User ID: {org_admin.id}")
        print(f"   Role: {org_admin.role.value}")
        print(f"   Created: {org_admin.created_at}")

        print("\n" + "="*70)
        print("LOGIN CREDENTIALS")
        print("="*70)
        print(f"   Organization Code: {ORG_CODE}")
        print(f"   Email: {ADMIN_EMAIL}")
        print(f"   Password: {ADMIN_PASSWORD}")
        print(f"   Login URL: http://localhost:4200/login")
        print("\n" + "="*70 + "\n")

    except Exception as e:
        db.rollback()
        print(f"\n[ERROR] Error creating org admin: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    add_org_admin()
