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
