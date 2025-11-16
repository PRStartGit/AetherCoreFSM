"""
Email Service with SMTP Support
Handles email sending with HTML templates
"""
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from typing import List, Optional, Dict, Any
from jinja2 import Template

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """Email service supporting SMTP and SendGrid"""

    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.smtp_tls = settings.SMTP_TLS
        self.smtp_ssl = settings.SMTP_SSL
        self.from_email = settings.FROM_EMAIL
        self.from_name = settings.FROM_NAME
        self.templates_dir = Path(settings.EMAIL_TEMPLATES_DIR)

    def _load_template(self, template_name: str) -> str:
        """Load HTML email template from file"""
        template_path = self.templates_dir / f"{template_name}.html"
        if not template_path.exists():
            raise FileNotFoundError(f"Email template not found: {template_name}")

        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _render_template(self, template_content: str, context: Dict[str, Any]) -> str:
        """Render Jinja2 template with context"""
        template = Template(template_content)
        return template.render(**context)

    def send_email_smtp(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        to_name: Optional[str] = None
    ) -> bool:
        """Send email using SMTP"""
        if not self.smtp_host or not self.smtp_user or not self.smtp_password:
            logger.warning("SMTP credentials not configured. Email not sent.")
            return False

        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = f"{to_name} <{to_email}>" if to_name else to_email

            # Attach HTML content
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)

            # Connect to SMTP server
            if self.smtp_ssl:
                server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)
            else:
                server = smtplib.SMTP(self.smtp_host, self.smtp_port)
                if self.smtp_tls:
                    server.starttls()

            # Login and send
            server.login(self.smtp_user, self.smtp_password)
            server.send_message(msg)
            server.quit()

            logger.info(f"Email sent successfully to {to_email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False

    def send_template_email(
        self,
        to_email: str,
        subject: str,
        template_name: str,
        context: Dict[str, Any],
        to_name: Optional[str] = None
    ) -> bool:
        """Send email using HTML template"""
        try:
            # Load and render template
            template_content = self._load_template(template_name)
            html_content = self._render_template(template_content, context)

            # Send email
            return self.send_email_smtp(to_email, subject, html_content, to_name)

        except Exception as e:
            logger.error(f"Failed to send template email: {str(e)}")
            return False

    # Specific email methods for common use cases

    def send_welcome_email(
        self,
        user_email: str,
        user_name: str,
        organization_name: str,
        user_role: str,
        temporary_password: str,
        assigned_sites: str,
        login_url: str
    ) -> bool:
        """Send welcome email to new user"""
        context = {
            'user_name': user_name,
            'user_email': user_email,
            'organization_name': organization_name,
            'user_role': user_role,
            'temporary_password': temporary_password,
            'assigned_sites': assigned_sites,
            'login_url': login_url,
            'role_permissions': self._get_role_permissions(user_role)
        }

        return self.send_template_email(
            to_email=user_email,
            subject=f"Welcome to {organization_name} - Zynthio Site Monitoring",
            template_name='user_welcome',
            context=context,
            to_name=user_name
        )

    def send_org_admin_welcome_email(
        self,
        admin_email: str,
        contact_person: str,
        organization_name: str,
        org_id: str,
        subscription_tier: str,
        temporary_password: str,
        reset_password_url: str
    ) -> bool:
        """Send welcome email to organization admin"""
        context = {
            'contact_person': contact_person,
            'organization_name': organization_name,
            'org_id': org_id,
            'subscription_tier': subscription_tier,
            'admin_email': admin_email,
            'contact_email': admin_email,
            'temporary_password': temporary_password,
            'reset_password_url': reset_password_url
        }

        return self.send_template_email(
            to_email=admin_email,
            subject=f"Welcome to Zynthio - {organization_name}",
            template_name='org_admin_welcome',
            context=context,
            to_name=contact_person
        )

    def send_password_reset_email(
        self,
        user_email: str,
        user_name: str,
        reset_url: str,
        reset_code: str,
        expiry_hours: int = 24
    ) -> bool:
        """Send password reset email"""
        context = {
            'user_name': user_name,
            'user_email': user_email,
            'reset_url': reset_url,
            'reset_code': reset_code,
            'expiry_hours': expiry_hours
        }

        return self.send_template_email(
            to_email=user_email,
            subject="Password Reset Request - Zynthio",
            template_name='password_reset',
            context=context,
            to_name=user_name
        )

    def send_weekly_performance_email(
        self,
        recipient_email: str,
        recipient_name: str,
        organization_name: str,
        week_start: str,
        week_end: str,
        report_data: Dict[str, Any]
    ) -> bool:
        """Send weekly performance report email"""
        context = {
            'recipient_name': recipient_name,
            'organization_name': organization_name,
            'week_start': week_start,
            'week_end': week_end,
            'report_date': week_end,
            **report_data  # Include all report metrics
        }

        return self.send_template_email(
            to_email=recipient_email,
            subject=f"Weekly Performance Report - {week_start} to {week_end}",
            template_name='weekly_performance_overall',
            context=context,
            to_name=recipient_name
        )

    def send_defect_report_email(
        self,
        recipient_email: str,
        recipient_name: str,
        organization_name: str,
        defects_data: Dict[str, Any]
    ) -> bool:
        """Send defect list report email"""
        context = {
            'recipient_name': recipient_name,
            'organization_name': organization_name,
            **defects_data
        }

        return self.send_template_email(
            to_email=recipient_email,
            subject=f"Defect Report - {organization_name}",
            template_name='defect_list_report',
            context=context,
            to_name=recipient_name
        )

    def _get_role_permissions(self, role: str) -> str:
        """Get formatted permissions list for role"""
        permissions = {
            'super_admin': [
                '<li>Manage all organizations and users</li>',
                '<li>View global analytics and reports</li>',
                '<li>Configure system settings</li>',
                '<li>Access all sites and data</li>'
            ],
            'org_admin': [
                '<li>Manage organization settings and users</li>',
                '<li>Create and manage sites</li>',
                '<li>View organization-wide reports</li>',
                '<li>Configure tasks and checklists</li>'
            ],
            'site_user': [
                '<li>Complete assigned checklists and tasks</li>',
                '<li>Report defects and issues</li>',
                '<li>View site performance metrics</li>',
                '<li>Upload photos and documentation</li>'
            ]
        }

        role_perms = permissions.get(role.lower(), permissions['site_user'])
        return ''.join(role_perms)


# Global email service instance
email_service = EmailService()


# Convenience functions for easy import
def send_welcome_email(*args, **kwargs):
    """Send welcome email"""
    return email_service.send_welcome_email(*args, **kwargs)


def send_org_admin_welcome_email(*args, **kwargs):
    """Send org admin welcome email"""
    return email_service.send_org_admin_welcome_email(*args, **kwargs)


def send_password_reset_email(*args, **kwargs):
    """Send password reset email"""
    return email_service.send_password_reset_email(*args, **kwargs)


def send_weekly_performance_email(*args, **kwargs):
    """Send weekly performance report"""
    return email_service.send_weekly_performance_email(*args, **kwargs)


def send_defect_report_email(*args, **kwargs):
    """Send defect report email"""
    return email_service.send_defect_report_email(*args, **kwargs)
