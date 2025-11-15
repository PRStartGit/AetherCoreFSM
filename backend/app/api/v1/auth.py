from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import secrets
from app.core.database import get_db
from app.core.security import verify_password, create_access_token, get_password_hash
from app.models.user import User
from app.models.organization import Organization
from app.models.password_reset_token import PasswordResetToken
from app.schemas.auth import LoginRequest, Token, PasswordResetRequest, PasswordReset
from app.schemas.user import UserResponse
from app.core.dependencies import get_current_user

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

    return {"access_token": access_token, "token_type": "bearer"}


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
