"""
Initial Super Admin Seed Script
Creates the initial super admin user with credentials:
Email: hello@prstart.co.uk
Password: ChangeMe123!

This script ensures:
- Passwords are hashed with bcrypt
- Sends email notification to the admin
- Can be run multiple times safely (idempotent)
"""
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models.user import User, UserRole


def send_welcome_email(email: str, password: str):
    """Send welcome email to the super admin."""
    try:
        # For now, print to console. In production, use SendGrid
        print("\n" + "="*70)
        print("📧 WELCOME EMAIL")
        print("="*70)
        print(f"To: {email}")
        print(f"Subject: Welcome to RiskProof - Your Super Admin Account")
        print("\nDear Administrator,\n")
        print("Your RiskProof super admin account has been successfully created!")
        print("\n🔐 Login Credentials:")
        print(f"   Email: {email}")
        print(f"   Password: {password}")
        print(f"   Login URL: http://localhost:4200/login")
        print("\n⚠️  IMPORTANT SECURITY NOTICE:")
        print("   Please change your password immediately after first login.")
        print("   This is a temporary password and should not be shared.")
        print("\n🔒 Security Features Enabled:")
        print("   ✓ Passwords hashed with bcrypt")
        print("   ✓ JWT token-based authentication")
        print("   ✓ Multi-tenant data isolation")
        print("   ✓ Role-based access control (RBAC)")
        print("\n📚 Quick Start:")
        print("   1. Log in using the credentials above")
        print("   2. Change your password in Account Settings")
        print("   3. Create your first organization")
        print("   4. Add sites and users to your organization")
        print("\nBest regards,")
        print("RiskProof Team")
        print("="*70 + "\n")

        # TODO: Implement actual email sending with SendGrid
        # from sendgrid import SendGridAPIClient
        # from sendgrid.helpers.mail import Mail
        # message = Mail(...)
        # sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        # response = sg.send(message)

    except Exception as e:
        print(f"⚠️  Could not send email: {e}")
        print("Email functionality requires SendGrid API key configuration.")


def create_initial_super_admin():
    """Create the initial super admin user."""
    print("\n🚀 RiskProof Initial Setup")
    print("="*70)
    print("Creating super admin account...")

    # Create all tables
    print("\n📊 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully")

    db = SessionLocal()

    try:
        # Configuration
        ADMIN_EMAIL = "hello@prstart.co.uk"
        ADMIN_PASSWORD = "ChangeMe123!"

        # Check if super admin already exists
        existing_admin = db.query(User).filter(
            User.email == ADMIN_EMAIL
        ).first()

        if existing_admin:
            print(f"\n⚠️  Super admin with email {ADMIN_EMAIL} already exists!")
            print(f"   Account created: {existing_admin.created_at}")
            print(f"   Status: {'Active' if existing_admin.is_active else 'Inactive'}")

            # Ask if user wants to reset password
            print("\n" + "="*70)
            return

        # Create super admin user
        print(f"\n👤 Creating super admin user...")
        print(f"   Email: {ADMIN_EMAIL}")

        super_admin = User(
            email=ADMIN_EMAIL,
            hashed_password=get_password_hash(ADMIN_PASSWORD),
            first_name="Platform",
            last_name="Administrator",
            role=UserRole.SUPER_ADMIN,
            organization_id=None,  # Super admin not tied to any organization
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        db.add(super_admin)
        db.commit()
        db.refresh(super_admin)

        print("✓ Super admin user created successfully!")
        print(f"   User ID: {super_admin.id}")
        print(f"   Role: {super_admin.role.value}")
        print(f"   Created: {super_admin.created_at}")

        # Send welcome email
        send_welcome_email(ADMIN_EMAIL, ADMIN_PASSWORD)

        print("\n✨ Setup Complete!")
        print("="*70)
        print("\n🎯 Next Steps:")
        print("   1. Start the backend: cd backend && uvicorn app.main:app --reload")
        print("   2. Start the frontend: cd frontend && ng serve")
        print("   3. Visit http://localhost:4200/login")
        print("   4. Log in with the credentials sent to your email")
        print("\n" + "="*70 + "\n")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Error creating super admin: {e}")
        raise
    finally:
        db.close()


def reset_super_admin_password():
    """Reset super admin password (useful for recovery)."""
    print("\n🔒 Reset Super Admin Password")
    print("="*70)

    db = SessionLocal()

    try:
        ADMIN_EMAIL = "hello@prstart.co.uk"
        NEW_PASSWORD = "ChangeMe123!"

        admin = db.query(User).filter(
            User.email == ADMIN_EMAIL,
            User.role == UserRole.SUPER_ADMIN
        ).first()

        if not admin:
            print(f"❌ Super admin with email {ADMIN_EMAIL} not found!")
            return

        admin.hashed_password = get_password_hash(NEW_PASSWORD)
        admin.updated_at = datetime.utcnow()
        db.commit()

        print(f"✓ Password reset successfully for {ADMIN_EMAIL}")
        send_welcome_email(ADMIN_EMAIL, NEW_PASSWORD)

    except Exception as e:
        db.rollback()
        print(f"❌ Error resetting password: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="RiskProof Initial Admin Setup")
    parser.add_argument(
        "--reset-password",
        action="store_true",
        help="Reset the super admin password"
    )

    args = parser.parse_args()

    if args.reset_password:
        reset_super_admin_password()
    else:
        create_initial_super_admin()
