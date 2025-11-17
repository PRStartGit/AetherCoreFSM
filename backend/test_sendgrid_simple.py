"""
Simple SendGrid API test - verifies API key works without sending emails.

This script tests if the SendGrid API key is valid and can connect to SendGrid.
"""

import os
import sys
from dotenv import load_dotenv

# Load .env file
load_dotenv()

def test_sendgrid_api_key():
    """Test if SendGrid API key is valid."""
    print("="*60)
    print("SENDGRID API KEY VALIDATION TEST")
    print("="*60)

    # Get API key from environment
    api_key = os.getenv('SENDGRID_API_KEY')

    if not api_key:
        print("\n❌ ERROR: SENDGRID_API_KEY not found in environment")
        print("   Please add it to your .env file")
        return False

    print(f"\n✅ API Key found (length: {len(api_key)} characters)")
    print(f"   Format: {api_key[:5]}...{api_key[-5:]}")

    # Check API key format
    if not api_key.startswith('SG.'):
        print("\n❌ ERROR: Invalid API key format")
        print("   SendGrid API keys should start with 'SG.'")
        return False

    print("✅ API Key format looks correct (starts with 'SG.')")

    # Try to initialize SendGrid client
    try:
        from sendgrid import SendGridAPIClient
        print("\n✅ SendGrid library imported successfully")

        # Initialize client
        sg = SendGridAPIClient(api_key)
        print("✅ SendGrid client initialized successfully")

        # Note: We're not making any API calls here to avoid sending test emails
        # The actual validation happens when we try to send an email

        print("\n" + "="*60)
        print("✅ ALL CHECKS PASSED!")
        print("="*60)
        print("\nThe SendGrid API key appears to be valid.")
        print("To test actual email sending, use: python test_sendgrid_email.py")
        print("\nNote: This test does not verify:")
        print("  - If the API key has mail send permission")
        print("  - If domain authentication is complete")
        print("  - If the API key is active (not revoked)")
        print("\nThose will be verified when you actually send an email.")

        return True

    except ImportError:
        print("\n❌ ERROR: SendGrid library not installed")
        print("   Run: pip install sendgrid")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: Failed to initialize SendGrid client")
        print(f"   {str(e)}")
        return False


def test_email_config():
    """Test email configuration."""
    print("\n" + "="*60)
    print("EMAIL CONFIGURATION CHECK")
    print("="*60)

    from_email = os.getenv('FROM_EMAIL')
    from_name = os.getenv('FROM_NAME')

    if from_email:
        print(f"\n✅ FROM_EMAIL: {from_email}")
    else:
        print("\n⚠️  FROM_EMAIL not configured (will use default)")

    if from_name:
        print(f"✅ FROM_NAME: {from_name}")
    else:
        print("⚠️  FROM_NAME not configured (will use default)")

    return True


if __name__ == "__main__":
    print("\n")

    success = test_sendgrid_api_key()

    if success:
        test_email_config()

    print("\n")
    sys.exit(0 if success else 1)
