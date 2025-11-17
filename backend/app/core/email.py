"""
Email Service with SMTP and SendGrid Support
Handles email sending with HTML templates
"""
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from typing import List, Optional, Dict, Any
from jinja2 import Template
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

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

    def send_email_sendgrid(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        to_name: Optional[str] = None
    ) -> bool:
        """Send email using SendGrid API"""
        sendgrid_api_key = getattr(settings, 'SENDGRID_API_KEY', None)

        if not sendgrid_api_key:
            logger.warning("SendGrid API key not configured. Email not sent.")
            return False

        try:
            # Create SendGrid message
            from_email_obj = Email(self.from_email, self.from_name)
            to_email_obj = To(to_email, to_name)
            content = Content("text/html", html_content)

            mail = Mail(
                from_email=from_email_obj,
                to_emails=to_email_obj,
                subject=subject,
                html_content=content
            )

            # Send email via SendGrid
            sg = SendGridAPIClient(sendgrid_api_key)
            response = sg.send(mail)

            logger.info(f"Email sent successfully via SendGrid to {to_email} (status: {response.status_code})")
            return True

        except Exception as e:
            logger.error(f"Failed to send email via SendGrid to {to_email}: {str(e)}")
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

            # Try SendGrid first, fall back to SMTP if not configured
            sendgrid_api_key = getattr(settings, 'SENDGRID_API_KEY', None)
            if sendgrid_api_key:
                return self.send_email_sendgrid(to_email, subject, html_content, to_name)
            else:
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

    def send_super_admin_welcome_email(
        self,
        admin_email: str,
        temporary_password: str,
        platform_url: str,
        deployment_date: str,
        total_organizations: int = 0,
        total_sites: int = 0,
        total_users: int = 1,
        active_checklists: int = 0
    ) -> bool:
        """Send welcome email to super admin when system is deployed"""
        context = {
            'admin_email': admin_email,
            'temporary_password': temporary_password,
            'platform_url': platform_url,
            'login_url': f"{platform_url}/login",
            'deployment_date': deployment_date,
            'total_organizations': total_organizations,
            'total_sites': total_sites,
            'total_users': total_users,
            'active_checklists': active_checklists,
            'email_service_status': '✅ Operational' if self.smtp_host else '⚠️ Not Configured',
            'database_status': '✅ Connected',
            'celery_status': '✅ Running'
        }

        return self.send_template_email(
            to_email=admin_email,
            subject="🚀 Zynthio Platform is Live!",
            template_name='super_admin_welcome',
            context=context,
            to_name='Super Admin'
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


def send_super_admin_welcome_email(*args, **kwargs):
    """Send super admin welcome email"""
    return email_service.send_super_admin_welcome_email(*args, **kwargs)
