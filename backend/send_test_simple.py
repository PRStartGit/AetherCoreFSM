"""
Simple test email sender without emoji characters (Windows compatible)
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def send_test_email():
    """Send test email using SendGrid."""
    print("="*60)
    print("SENDGRID TEST EMAIL SENDER")
    print("="*60)

    # Get configuration
    api_key = os.getenv('SENDGRID_API_KEY')
    from_email = os.getenv('FROM_EMAIL', 'hello@prstart.co.uk')
    from_name = os.getenv('FROM_NAME', 'Zynthio Site Monitoring')
    to_email = 'hello@prstart.co.uk'

    print(f"\nConfiguration:")
    print(f"  FROM: {from_name} <{from_email}>")
    print(f"  TO: {to_email}")
    print(f"  API Key: {api_key[:10]}...{api_key[-5:] if api_key else 'NOT SET'}")

    if not api_key:
        print("\n[ERROR] SENDGRID_API_KEY not found in .env file")
        return False

    # Create HTML email content
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            .success-box {{ background: white; padding: 20px; border-left: 4px solid #4caf50; margin: 20px 0; }}
            .info {{ background: #e3f2fd; padding: 15px; border-radius: 5px; margin: 15px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>SendGrid Test Email</h1>
                <p>Zynthio Email Service Test</p>
            </div>
            <div class="content">
                <div class="success-box">
                    <h2>[SUCCESS]</h2>
                    <p><strong>SendGrid integration is working correctly!</strong></p>
                </div>

                <h3>Test Details:</h3>
                <div class="info">
                    <p><strong>Sent At:</strong> {timestamp}</p>
                    <p><strong>From:</strong> {from_name} &lt;{from_email}&gt;</p>
                    <p><strong>To:</strong> {to_email}</p>
                    <p><strong>Service:</strong> SendGrid API</p>
                </div>

                <h3>What This Means:</h3>
                <ul>
                    <li>SendGrid API key is valid and active</li>
                    <li>Email service is properly configured</li>
                    <li>Emails can be sent from hello@prstart.co.uk</li>
                    <li>Ready for production deployment</li>
                </ul>

                <h3>Next Steps:</h3>
                <ol>
                    <li>Deploy to production with the API key</li>
                    <li>Test welcome emails for new users</li>
                    <li>Monitor delivery in SendGrid Activity dashboard</li>
                </ol>

                <p style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd;">
                    <strong>Note:</strong> This is an automated test email sent from the Zynthio backend service.
                </p>
            </div>
        </div>
    </body>
    </html>
    """

    try:
        print("\n" + "="*60)
        print("Sending test email via SendGrid API...")
        print("="*60)

        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail, Email, To, Content

        # Create message
        from_email_obj = Email(from_email, from_name)
        to_email_obj = To(to_email)
        subject = "[SUCCESS] SendGrid Test Email - Zynthio Integration Working"
        content = Content("text/html", html_content)

        mail = Mail(
            from_email=from_email_obj,
            to_emails=to_email_obj,
            subject=subject,
            html_content=content
        )

        # Send email
        sg = SendGridAPIClient(api_key)
        response = sg.send(mail)

        print(f"\n[SUCCESS] Email sent to {to_email}")
        print(f"   Status Code: {response.status_code}")

        if response.status_code == 202:
            print("\n" + "="*60)
            print("[SUCCESS] EMAIL SENT SUCCESSFULLY!")
            print("="*60)
            print(f"\nCheck your inbox at {to_email}")
            print("(also check spam folder if you don't see it)")
            print("\nYou can also monitor delivery at:")
            print("https://app.sendgrid.com/email_activity")
            return True
        else:
            print(f"\n[WARNING] Unexpected status code: {response.status_code}")
            return False

    except ImportError:
        print("\n[ERROR] SendGrid library not installed")
        print("   Run: pip install sendgrid")
        return False
    except Exception as e:
        print(f"\n[ERROR] Failed to send email")
        print(f"   {str(e)}")

        # Show more details if available
        if hasattr(e, 'body'):
            print(f"   Response body: {e.body}")
        if hasattr(e, 'status_code'):
            print(f"   Status code: {e.status_code}")

        return False


if __name__ == "__main__":
    print("\n")
    success = send_test_email()
    print("\n")
    sys.exit(0 if success else 1)
