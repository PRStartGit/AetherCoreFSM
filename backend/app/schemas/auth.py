from pydantic import BaseModel, EmailStr
from typing import Optional


class Token(BaseModel):
    """Token response schema."""
    access_token: str
    token_type: str = "bearer"
    must_change_password: bool = False


class TokenData(BaseModel):
    """Token data schema."""
    email: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[str] = None
    organization_id: Optional[int] = None


class LoginRequest(BaseModel):
    """Login request schema."""
    organization_id: str  # e.g., "vig"
    email: EmailStr
    password: str


class PasswordChange(BaseModel):
    """Password change request schema."""
    old_password: str
    new_password: str


class PasswordResetRequest(BaseModel):
    """Request password reset schema."""
    organization_id: str  # e.g., "vig"
    email: EmailStr


class PasswordReset(BaseModel):
    """Reset password with token schema."""
    token: str
    new_password: str


class RegistrationRequest(BaseModel):
    """Registration request schema for new trial sign-ups."""
    # Organization details
    company_name: str
    org_id: str  # Desired organization ID (e.g., "acme", "restaurant123")

    # Contact details
    contact_person: str
    contact_email: EmailStr
    contact_phone: Optional[str] = None
    address: Optional[str] = None

    # Admin user details
    admin_first_name: str
    admin_last_name: str
    admin_email: EmailStr
    admin_password: str
