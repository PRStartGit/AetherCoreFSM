"""
Send Super Admin Welcome Email to hello@prstart.co.uk

This script sends the initial welcome email to the first super admin
with login credentials for the production Zynthio platform.
"""

import os
import sys
import secrets
import string
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_secure_password(length=16):
    """Generate a secure random password."""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password

def send_superadmin_email():
    """Send welcome email to first super admin."""
    print("="*60)
    print("SUPER ADMIN WELCOME EMAIL SENDER")
    print("="*60)

    # Configuration
    admin_email = 'hello@prstart.co.uk'
    temporary_password = generate_secure_password(16)
    platform_url = 'https://zynthio.com'
    deployment_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')

    print(f"\nSending welcome email to: {admin_email}")
    print(f"Platform URL: {platform_url}")
    print(f"Deployment Date: {deployment_date}")
    print(f"\nGenerated Password: {temporary_password}")
    print("(This will be sent in the email)")

    # Import email service
    try:
        from app.core.email import send_super_admin_welcome_email

        print("\n" + "="*60)
        print("Sending email via SendGrid...")
        print("="*60)

        success = send_super_admin_welcome_email(
            admin_email=admin_email,
            temporary_password=temporary_password,
            platform_url=platform_url,
            deployment_date=deployment_date,
            total_organizations=0,
            total_sites=0,
            total_users=1,
            active_checklists=0
        )

        if success:
            print("\n" + "="*60)
            print("[SUCCESS] SUPER ADMIN WELCOME EMAIL SENT!")
            print("="*60)
            print(f"\nEmail sent to: {admin_email}")
            print(f"\nLogin credentials:")
            print(f"  URL: {platform_url}")
            print(f"  Email: {admin_email}")
            print(f"  Password: {temporary_password}")
            print("\nIMPORTANT: Save these credentials securely!")
            print("The super admin should change their password after first login.")
            print("\nNext steps:")
            print("  1. Check inbox at hello@prstart.co.uk")
            print("  2. Login to https://zynthio.com")
            print("  3. Change password on first login")
            print("  4. Start creating organizations and sites")
            return True
        else:
            print("\n[ERROR] Failed to send email")
            print("Check the logs above for details")
            return False

    except ImportError as e:
        print(f"\n[ERROR] Failed to import email service: {e}")
        print("Make sure you're running this from the backend directory")
        return False
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n")
    success = send_superadmin_email()
    print("\n")
    sys.exit(0 if success else 1)
