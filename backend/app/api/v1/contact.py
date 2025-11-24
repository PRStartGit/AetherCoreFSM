"""
Contact Form API Endpoint
Public endpoint for sales/general inquiries
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
import logging
from datetime import datetime
import uuid

from app.core.email import email_service

logger = logging.getLogger(__name__)

router = APIRouter()


class ContactFormSubmission(BaseModel):
    """Contact form submission schema"""
    name: str
    email: EmailStr
    company: Optional[str] = None
    phone: Optional[str] = None
    message: str
    inquiry_type: Optional[str] = 'general'


@router.post('/submit')
async def submit_contact_form(submission: ContactFormSubmission):
    """
    Submit a contact form inquiry.
    Sends notification email to hello@zynthio.co.uk and confirmation to submitter.
    """
    try:
        submission_id = str(uuid.uuid4())[:8].upper()

        # Send notification email to Zynthio team
        inquiry_type_labels = {
            'general': 'General Inquiry',
            'sales': 'Sales / Pricing',
            'demo': 'Demo Request',
            'support': 'Technical Support'
        }
        inquiry_label = inquiry_type_labels.get(submission.inquiry_type, 'General Inquiry')

        team_email_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #0EA5E9;">New Contact Form Submission</h2>
            <p><strong>Submission ID:</strong> {submission_id}</p>
            <p><strong>Inquiry Type:</strong> {inquiry_label}</p>
            <hr style="border: 1px solid #eee;">
            <h3>Contact Details</h3>
            <p><strong>Name:</strong> {submission.name}</p>
            <p><strong>Email:</strong> {submission.email}</p>
            <p><strong>Company:</strong> {submission.company or 'Not provided'}</p>
            <p><strong>Phone:</strong> {submission.phone or 'Not provided'}</p>
            <hr style="border: 1px solid #eee;">
            <h3>Message</h3>
            <p>{submission.message}</p>
            <hr style="border: 1px solid #eee;">
            <p style="color: #666; font-size: 12px;">Submitted at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
        </body>
        </html>
        """

        email_service.send_email_sendgrid(
            to_email="hello@zynthio.co.uk",
            subject=f"[{inquiry_label}] New inquiry from {submission.name}",
            html_content=team_email_content,
            to_name="Zynthio Team"
        )

        # Send confirmation email to submitter
        confirmation_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #0EA5E9;">Thank You for Contacting Us!</h2>
            <p>Hi {submission.name},</p>
            <p>We have received your message and will get back to you within 24 hours.</p>
            <p><strong>Your Reference ID:</strong> {submission_id}</p>
            <hr style="border: 1px solid #eee;">
            <h3>Your Message</h3>
            <p>{submission.message}</p>
            <hr style="border: 1px solid #eee;">
            <p>Best regards,<br>The Zynthio Team</p>
            <p style="color: #666; font-size: 12px;">
                Zynthio - Food Safety Compliance Made Simple<br>
                <a href="https://zynthio.co.uk" style="color: #0EA5E9;">zynthio.co.uk</a>
            </p>
        </body>
        </html>
        """

        email_service.send_email_sendgrid(
            to_email=submission.email,
            subject="Thank you for contacting Zynthio",
            html_content=confirmation_content,
            to_name=submission.name
        )

        logger.info(f"Contact form submitted: {submission_id} from {submission.email}")

        return {
            "success": True,
            "message": "Your message has been sent successfully",
            "submission_id": submission_id
        }

    except Exception as e:
        logger.error(f"Error processing contact form: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to send message. Please try again later."
        )
