"""
Authentication Endpoints.
Login with JWT tokens and user profile retrieval.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr

from backend.app.core.security import create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int = 3600
    user: dict


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest):
    """
    Authenticates user. For development and demo purposes,
    supports standard role demo accounts.
    """
    # Demo credentials map for fast local onboarding
    demo_users = {
        "admin@example.com": {"id": "11111111-1111-1111-1111-111111111111", "name": "System Admin", "role": "admin"},
        "researcher@example.com": {"id": "22222222-2222-2222-2222-222222222222", "name": "Rita Researcher", "role": "researcher"},
        "campaigns@example.com": {"id": "33333333-3333-3333-3333-333333333333", "name": "Carlos Campaigner", "role": "campaign_manager"},
        "developer@example.com": {"id": "44444444-4444-4444-4444-444444444444", "name": "Devon Developer", "role": "developer"},
    }

    email_clean = payload.email.lower()
    if email_clean in demo_users and payload.password == "Password123!":
        user_info = demo_users[email_clean]
        token_data = {
            "sub": user_info["id"],
            "email": email_clean,
            "full_name": user_info["name"],
            "role": user_info["role"]
        }
        token = create_access_token(token_data)
        return TokenResponse(
            access_token=token,
            expires_in=3600,
            user={
                "id": user_info["id"],
                "email": email_clean,
                "full_name": user_info["name"],
                "role": user_info["role"],
                "is_active": True
            }
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password"
    )


@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):
    """Returns profile for currently authenticated user."""
    return current_user
