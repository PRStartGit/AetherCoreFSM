#!/usr/bin/env python3
"""
Script to email documentation files to hello@prstart.co.uk
"""
import os
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition

def send_documentation_email():
    # SendGrid API key from environment
    api_key = os.getenv('SENDGRID_API_KEY')
    if not api_key:
        print("ERROR: SENDGRID_API_KEY not found in environment")
        return False

    # Email configuration
    from_email = os.getenv('FROM_EMAIL', 'noreply@zynthio.com')
    to_email = 'hello@prstart.co.uk'
    subject = 'AetherCoreFSM Documentation - Handover & System Reference'

    # Email body
    html_content = """
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #0891b2;">AetherCoreFSM (Zynthio) Documentation</h2>

            <p>Hello,</p>

            <p>Attached are the complete documentation files for the AetherCoreFSM (Zynthio) food safety management platform:</p>

            <ol>
                <li><strong>AetherCoreFSM_Handover_Updated.md</strong> - Comprehensive handover document including:
                    <ul>
                        <li>Recent critical fixes and deployments</li>
                        <li>Server access credentials and SSH setup</li>
                        <li>Git workflow and deployment procedures</li>
                        <li>Environment configuration</li>
                        <li>Common issues and solutions</li>
                        <li>Code style preferences</li>
                    </ul>
                </li>
                <li><strong>AetherCoreFSM_System_Documentation.md</strong> - Complete system reference including:
                    <ul>
                        <li>Full API documentation</li>
                        <li>Database schema with ERD diagrams</li>
                        <li>Architecture overview</li>
                        <li>Frontend component documentation</li>
                        <li>Authentication and security</li>
                        <li>User workflows</li>
                        <li>Deployment procedures</li>
                        <li>Troubleshooting guide</li>
                    </ul>
                </li>
            </ol>

            <p>These documents are ready to be shared with other developers or Claude sessions for continued development.</p>

            <h3 style="color: #0891b2;">Recent Updates (January 22, 2025)</h3>
            <ul>
                <li>✅ Fixed photo upload/display in temperature monitoring (commit df6afcf)</li>
                <li>✅ Fixed password reset button endpoint mismatch (commit 34ea4bc)</li>
                <li>✅ Enabled SendGrid email integration for password resets (commit 1797a76)</li>
            </ul>

            <p>All changes have been deployed to production at <strong>165.22.122.116</strong>.</p>

            <p style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e5e7eb; color: #6b7280; font-size: 14px;">
                This email was sent automatically by the AetherCoreFSM system.<br>
                Generated on January 22, 2025
            </p>
        </div>
    </body>
    </html>
    """

    # Create message
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )

    # Read and attach handover document
    handover_path = '/mnt/desktop/AetherCoreFSM_Handover_Updated.md'
    try:
        with open(handover_path, 'r', encoding='utf-8') as f:
            handover_content = f.read()

        handover_attachment = Attachment(
            FileContent(base64.b64encode(handover_content.encode()).decode()),
            FileName('AetherCoreFSM_Handover_Updated.md'),
            FileType('text/markdown'),
            Disposition('attachment')
        )
        message.add_attachment(handover_attachment)
        print(f"✓ Attached handover document ({len(handover_content)} bytes)")
    except Exception as e:
        print(f"ERROR reading handover document: {e}")
        return False

    # Read and attach system documentation
    system_doc_path = '/mnt/desktop/AetherCoreFSM_System_Documentation.md'
    try:
        with open(system_doc_path, 'r', encoding='utf-8') as f:
            system_doc_content = f.read()

        system_doc_attachment = Attachment(
            FileContent(base64.b64encode(system_doc_content.encode()).decode()),
            FileName('AetherCoreFSM_System_Documentation.md'),
            FileType('text/markdown'),
            Disposition('attachment')
        )
        message.add_attachment(system_doc_attachment)
        print(f"✓ Attached system documentation ({len(system_doc_content)} bytes)")
    except Exception as e:
        print(f"ERROR reading system documentation: {e}")
        return False

    # Send email
    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)

        if response.status_code in [200, 202]:
            print(f"\n{'='*60}")
            print(f"✓ EMAIL SENT SUCCESSFULLY")
            print(f"{'='*60}")
            print(f"To: {to_email}")
            print(f"Subject: {subject}")
            print(f"Status Code: {response.status_code}")
            print(f"Attachments: 2 files")
            print(f"  - AetherCoreFSM_Handover_Updated.md")
            print(f"  - AetherCoreFSM_System_Documentation.md")
            print(f"{'='*60}\n")
            return True
        else:
            print(f"ERROR: Unexpected status code {response.status_code}")
            print(f"Response: {response.body}")
            return False

    except Exception as e:
        print(f"ERROR sending email: {e}")
        return False

if __name__ == '__main__':
    success = send_documentation_email()
    exit(0 if success else 1)
