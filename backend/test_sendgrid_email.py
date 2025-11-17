"""
Test script for SendGrid email functionality.

This script tests:
1. SendGrid API connection
2. Email sending with SendGrid
3. Fallback to SMTP if SendGrid not configured
"""

import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.core.email import email_service

def print_test(test_name):
    """Print test header."""
    print(f"\n{'='*60}")
    print(f"TEST: {test_name}")
    print('='*60)

def print_success(message):
    """Print success message."""
    print(f"✅ {message}")

def print_error(message):
    """Print error message."""
    print(f"❌ {message}")

def print_info(message):
    """Print info message."""
    print(f"ℹ️  {message}")


def test_sendgrid_configuration():
    """Test SendGrid configuration."""
    print_test("SendGrid Configuration Check")

    from app.core.config import settings

    # Check if SendGrid API key is configured
    sendgrid_api_key = getattr(settings, 'SENDGRID_API_KEY', None)

    if sendgrid_api_key:
        print_success(f"SendGrid API key configured (length: {len(sendgrid_api_key)})")
        return True
    else:
        print_error("SendGrid API key not configured")
        print_info("Add SENDGRID_API_KEY to your .env file")
        print_info("Get your API key from: https://app.sendgrid.com/settings/api_keys")
        return False


def test_smtp_configuration():
    """Test SMTP configuration."""
    print_test("SMTP Configuration Check")

    if email_service.smtp_host and email_service.smtp_user and email_service.smtp_password:
        print_success("SMTP credentials configured")
        print_info(f"SMTP Host: {email_service.smtp_host}")
        print_info(f"SMTP Port: {email_service.smtp_port}")
        print_info(f"SMTP User: {email_service.smtp_user}")
        return True
    else:
        print_error("SMTP credentials not fully configured")
        return False


def test_send_test_email():
    """Test sending an actual email."""
    print_test("Send Test Email")

    from app.core.config import settings

    # Check which method will be used
    sendgrid_api_key = getattr(settings, 'SENDGRID_API_KEY', None)

    if sendgrid_api_key:
        print_info("Will use SendGrid API to send test email")
    elif email_service.smtp_host:
        print_info("Will use SMTP to send test email")
    else:
        print_error("No email service configured")
        return False

    # Ask for recipient email
    test_email = input("\nEnter test recipient email address: ").strip()

    if not test_email:
        print_error("No email address provided")
        return False

    print_info(f"Sending test email to: {test_email}")

    # Create test email content
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
            .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📧 SendGrid Test Email</h1>
            </div>
            <div class="content">
                <h2>Success!</h2>
                <p>This is a test email from Zynthio's SendGrid integration.</p>
                <p>If you're reading this, the email service is working correctly!</p>
                <p><strong>Timestamp:</strong> {timestamp}</p>
            </div>
        </div>
    </body>
    </html>
    """

    from datetime import datetime
    html_content = html_content.format(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # Try to send email
    try:
        if sendgrid_api_key:
            success = email_service.send_email_sendgrid(
                to_email=test_email,
                subject="SendGrid Test Email - Zynthio",
                html_content=html_content,
                to_name="Test User"
            )
        else:
            success = email_service.send_email_smtp(
                to_email=test_email,
                subject="SMTP Test Email - Zynthio",
                html_content=html_content,
                to_name="Test User"
            )

        if success:
            print_success(f"Test email sent successfully to {test_email}")
            print_info("Check your inbox (and spam folder) for the test email")
            return True
        else:
            print_error("Failed to send test email")
            return False

    except Exception as e:
        print_error(f"Error sending test email: {str(e)}")
        return False


def run_all_tests():
    """Run all email tests."""
    print("\n" + "="*60)
    print("SENDGRID EMAIL SERVICE TEST SUITE")
    print("="*60)

    results = []

    # Configuration tests
    results.append(("SendGrid Configuration", test_sendgrid_configuration()))
    results.append(("SMTP Configuration", test_smtp_configuration()))

    # Check if at least one service is configured
    from app.core.config import settings
    sendgrid_configured = getattr(settings, 'SENDGRID_API_KEY', None) is not None
    smtp_configured = email_service.smtp_host and email_service.smtp_user and email_service.smtp_password

    if sendgrid_configured or smtp_configured:
        # Ask if user wants to send a test email
        print("\n" + "="*60)
        send_test = input("Would you like to send a test email? (yes/no): ").strip().lower()

        if send_test in ['yes', 'y']:
            results.append(("Send Test Email", test_send_test_email()))
    else:
        print_error("\nNo email service configured. Please configure SendGrid or SMTP first.")

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")

    print("\n" + "="*60)
    print(f"TOTAL: {passed}/{total} tests passed")
    print("="*60)

    # Configuration instructions
    print("\n" + "="*60)
    print("SENDGRID CONFIGURATION INSTRUCTIONS")
    print("="*60)
    print("\n1. Get your SendGrid API Key:")
    print("   - Go to https://app.sendgrid.com/settings/api_keys")
    print("   - Click 'Create API Key'")
    print("   - Give it a name (e.g., 'Zynthio Production')")
    print("   - Select 'Full Access' or at minimum 'Mail Send' permission")
    print("   - Copy the API key (you'll only see it once!)")
    print("\n2. Add to your .env file:")
    print("   SENDGRID_API_KEY=your_api_key_here")
    print("   FROM_EMAIL=hello@zynthio.com")
    print("   FROM_NAME=Zynthio Site Monitoring")
    print("\n3. Verify domain authentication:")
    print("   - Go to https://app.sendgrid.com/settings/sender_auth/domains")
    print("   - Add zynthio.com domain")
    print("   - Add the DNS records to your domain provider")
    print("   - Wait for verification (can take up to 48 hours)")
    print("\n4. Restart the backend:")
    print("   docker compose restart backend")
    print("="*60)

    return all(result for _, result in results if test_name != "Send Test Email")


if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
