from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import secrets
from app.core.database import get_db
from app.core.security import verify_password, create_access_token, get_password_hash
from app.models.user import User
from app.models.organization import Organization
from app.models.password_reset_token import PasswordResetToken
from app.schemas.auth import LoginRequest, Token, PasswordResetRequest, PasswordReset, PasswordChange, RegistrationRequest
from app.schemas.user import UserResponse
from app.core.dependencies import get_current_user
from app.models.user import UserRole
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

router = APIRouter()


@router.post("/login", response_model=Token)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login endpoint - authenticates user based on organization ID, email, and password.
    Returns JWT access token.
    """
    # Verify organization exists
    organization = db.query(Organization).filter(
        Organization.org_id == login_data.organization_id,
        Organization.is_active == True
    ).first()

    if not organization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid organization ID or credentials"
        )

    # Find user by email and organization
    user = db.query(User).filter(
        User.email == login_data.email,
        User.organization_id == organization.id
    ).first()

    # Also check for super admins (they don't have organization_id)
    if not user:
        user = db.query(User).filter(
            User.email == login_data.email,
            User.organization_id.is_(None)
        ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Verify password
    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # Create access token
    access_token = create_access_token(
        data={
            "user_id": user.id,
            "email": user.email,
            "role": user.role.value,
            "organization_id": user.organization_id
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "must_change_password": user.must_change_password
    }


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Get current authenticated user information."""
    return current_user


@router.post("/logout")
def logout():
    """
    Logout endpoint.
    Since we're using JWT tokens, logout is handled client-side by removing the token.
    This endpoint exists for consistency and future extensions.
    """
    return {"message": "Successfully logged out"}


@router.post("/change-password")
def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change password for authenticated user.
    Requires old password for verification.
    """
    # Verify old password
    if not verify_password(password_data.old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )

    # Update to new password
    current_user.hashed_password = get_password_hash(password_data.new_password)
    current_user.must_change_password = False  # Clear forced password change flag
    db.commit()

    print(f"\n{'='*80}")
    print(f"PASSWORD CHANGED")
    print(f"{'='*80}")
    print(f"User: {current_user.full_name} ({current_user.email})")
    print(f"{'='*80}\n")

    return {"message": "Password changed successfully"}


@router.post("/forgot-password")
def request_password_reset(
    request_data: PasswordResetRequest,
    db: Session = Depends(get_db)
):
    """
    Request password reset - generates a token and logs reset link.
    For security, always returns success even if email doesn't exist.
    """
    # Verify organization exists
    organization = db.query(Organization).filter(
        Organization.org_id == request_data.organization_id,
        Organization.is_active == True
    ).first()

    if organization:
        # Find user by email and organization
        user = db.query(User).filter(
            User.email == request_data.email,
            User.organization_id == organization.id
        ).first()

        # Also check for super admins (they don't have organization_id)
        if not user:
            user = db.query(User).filter(
                User.email == request_data.email,
                User.organization_id.is_(None)
            ).first()

        if user:
            # Generate secure token
            reset_token = secrets.token_urlsafe(32)

            # Create token record (expires in 1 hour)
            token_record = PasswordResetToken(
                token=reset_token,
                user_id=user.id,
                expires_at=datetime.utcnow() + timedelta(hours=1)
            )
            db.add(token_record)
            db.commit()

            # Log reset link to console (no email service yet)
            reset_link = f"http://localhost:4200/reset-password?token={reset_token}"
            print(f"\n{'='*80}")
            print(f"PASSWORD RESET REQUESTED")
            print(f"{'='*80}")
            print(f"User: {user.full_name} ({user.email})")
            print(f"Organization: {request_data.organization_id}")
            print(f"Reset Link: {reset_link}")
            print(f"Token expires at: {token_record.expires_at} UTC")
            print(f"{'='*80}\n")

    # Always return success for security (don't reveal if email exists)
    return {
        "message": "If an account exists with that email, a password reset link has been sent."
    }


@router.post("/reset-password")
def reset_password(
    reset_data: PasswordReset,
    db: Session = Depends(get_db)
):
    """
    Reset password using a valid token.
    """
    # Find token in database
    token_record = db.query(PasswordResetToken).filter(
        PasswordResetToken.token == reset_data.token
    ).first()

    if not token_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )

    # Check if token is valid (not expired and not used)
    if not token_record.is_valid():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )

    # Get the user
    user = db.query(User).filter(User.id == token_record.user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found"
        )

    # Update user's password
    user.hashed_password = get_password_hash(reset_data.new_password)

    # Mark token as used
    token_record.used = 1  # SQLite uses 1 for True

    db.commit()

    print(f"\n{'='*80}")
    print(f"PASSWORD SUCCESSFULLY RESET")
    print(f"{'='*80}")
    print(f"User: {user.full_name} ({user.email})")
    print(f"{'='*80}\n")

    return {"message": "Password has been successfully reset. You can now login with your new password."}


def send_welcome_email(email: str, org_id: str, password: str, company_name: str) -> bool:
    """
    Send welcome email to new trial user.
    Returns True if email sent successfully, False otherwise.
    """
    try:
        smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        smtp_user = os.getenv('SMTP_USER', '')
        smtp_password = os.getenv('SMTP_PASSWORD', '')
        from_email = os.getenv('FROM_EMAIL', 'hello@zynthio.com')
        from_name = os.getenv('FROM_NAME', 'Zynthio')

        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Welcome to Zynthio - Your Trial Account is Ready!'
        msg['From'] = f'{from_name} <{from_email}>'
        msg['To'] = email

        # Email body
        html = f'''
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
        .button {{ display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
        .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
        .credentials {{ background: white; padding: 15px; border-left: 4px solid #667eea; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Welcome to Zynthio!</h1>
            <p>Your Safety Management Platform</p>
        </div>
        <div class="content">
            <h2>Hello {company_name},</h2>
            <p>Thank you for signing up for Zynthio! Your trial account has been created and is ready to use.</p>

            <div class="credentials">
                <h3>Your Login Credentials:</h3>
                <p><strong>Organization ID:</strong> {org_id}</p>
                <p><strong>Email:</strong> {email}</p>
                <p><strong>Password:</strong> {password}</p>
                <p><strong>URL:</strong> <a href="https://zynthio.com">https://zynthio.com</a></p>
            </div>

            <p>As an Organization Admin, you can:</p>
            <ul>
                <li>Create and manage sites</li>
                <li>Add team members</li>
                <li>Configure safety checklists</li>
                <li>View reports and analytics</li>
                <li>Monitor compliance across your organization</li>
            </ul>

            <center>
                <a href="https://zynthio.com" class="button">Login to Zynthio</a>
            </center>

            <p><strong>Important:</strong> We recommend changing your password after your first login for security.</p>

            <p>If you have any questions or need assistance getting started, feel free to reach out to our support team.</p>

            <p>Best regards,<br>The Zynthio Team</p>
        </div>
        <div class="footer">
            <p>This email was sent from Zynthio Site Monitoring Platform</p>
            <p>2025 Zynthio. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
'''

        text = f'''
Welcome to Zynthio!

Thank you for signing up! Your trial account has been created.

Login Credentials:
------------------
Organization ID: {org_id}
Email: {email}
Password: {password}
URL: https://zynthio.com

As an Organization Admin, you can manage sites, add team members, configure safety checklists, and monitor compliance.

We recommend changing your password after your first login.

Best regards,
The Zynthio Team
'''

        # Attach parts
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)

        # Send email
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()

        print(f"Welcome email sent to {email}")
        return True
    except Exception as e:
        print(f"Failed to send welcome email: {str(e)}")
        return False


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_trial(
    registration: RegistrationRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new trial account.
    Creates organization and admin user.
    Sends welcome email with credentials.
    """
    # Check if org_id already exists
    existing_org = db.query(Organization).filter(
        Organization.org_id == registration.org_id.lower().strip()
    ).first()

    if existing_org:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization ID already exists. Please choose a different one."
        )

    # Check if admin email already exists
    existing_user = db.query(User).filter(
        User.email == registration.admin_email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email address already in use."
        )

    # Get active promotion to determine trial period
    from app.models.promotion import Promotion
    active_promotion = db.query(Promotion).filter(Promotion.is_active == True).first()
    trial_days = active_promotion.trial_days if active_promotion else 30  # Default to 30 days
    
    # Create organization
    new_org = Organization(
        name=registration.company_name,
        org_id=registration.org_id.lower().strip(),
        contact_person=registration.contact_person,
        contact_email=registration.contact_email,
        contact_phone=registration.contact_phone,
        address=registration.address,
        is_active=True,
        is_trial=True,
        subscription_tier="basic",
        subscription_start_date=datetime.utcnow(),
        subscription_end_date=datetime.utcnow() + timedelta(days=trial_days)  # Dynamic trial period
    )

    db.add(new_org)
    db.flush()  # Get the org ID before creating user

    # Create admin user
    admin_user = User(
        email=registration.admin_email,
        hashed_password=get_password_hash(registration.admin_password),
        first_name=registration.admin_first_name,
        last_name=registration.admin_last_name,
        role=UserRole.ORG_ADMIN,
        organization_id=new_org.id,
        is_active=True,
        must_change_password=False
    )

    db.add(admin_user)
    db.commit()
    db.refresh(new_org)
    db.refresh(admin_user)

    # Send welcome email (non-blocking, continue even if email fails)
    send_welcome_email(
        email=registration.admin_email,
        org_id=new_org.org_id,
        password=registration.admin_password,
        company_name=registration.company_name
    )

    print(f"\n{'='*80}")
    print(f"NEW TRIAL REGISTRATION")
    print(f"{'='*80}")
    print(f"Company: {new_org.name}")
    print(f"Org ID: {new_org.org_id}")
    print(f"Admin: {admin_user.full_name} ({admin_user.email})")
    print(f"Trial ends: {new_org.subscription_end_date}")
    print(f"{'='*80}\n")

    return {
        "message": "Registration successful! Check your email for login credentials.",
        "organization_id": new_org.org_id,
        "trial_end_date": new_org.subscription_end_date
    }
