from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.models.user import User
from app.models.organization import Organization
from app.schemas.auth import LoginRequest, Token
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
