"""
Authentication endpoints - Strava OAuth2
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from pydantic import BaseModel

from app.db.database import get_db
from app.models.user import User
from app.services.strava_service import StravaService
from app.core.security import create_access_token

router = APIRouter()
strava_service = StravaService()


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int


@router.get("/strava/authorize")
async def strava_authorize():
    """
    Get Strava OAuth authorization URL
    """
    auth_url = await strava_service.get_authorization_url()
    return {"authorization_url": auth_url}


@router.get("/strava/callback")
async def strava_callback(
    code: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Handle Strava OAuth callback and create/update user
    """
    try:
        # Exchange code for tokens
        token_data = await strava_service.exchange_token(code)

        # Get athlete data
        athlete_data = await strava_service.get_athlete(token_data["access_token"])

        # Check if user exists
        result = await db.execute(
            select(User).where(User.strava_id == athlete_data["id"])
        )
        user = result.scalar_one_or_none()

        if user:
            # Update existing user
            user.access_token = token_data["access_token"]
            user.refresh_token = token_data["refresh_token"]
            user.token_expires_at = datetime.fromtimestamp(token_data["expires_at"])
            user.username = athlete_data.get("username")
            user.firstname = athlete_data.get("firstname")
            user.lastname = athlete_data.get("lastname")
            user.profile_picture = athlete_data.get("profile")
            user.updated_at = datetime.utcnow()
        else:
            # Create new user
            user = User(
                strava_id=athlete_data["id"],
                username=athlete_data.get("username"),
                firstname=athlete_data.get("firstname"),
                lastname=athlete_data.get("lastname"),
                email=athlete_data.get("email"),
                profile_picture=athlete_data.get("profile"),
                access_token=token_data["access_token"],
                refresh_token=token_data["refresh_token"],
                token_expires_at=datetime.fromtimestamp(token_data["expires_at"]),
            )
            db.add(user)

        await db.commit()
        await db.refresh(user)

        # Create JWT token for our app
        jwt_token = create_access_token({"sub": str(user.id)})

        return TokenResponse(
            access_token=jwt_token,
            user_id=user.id
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Authentication failed: {str(e)}"
        )


@router.get("/me")
async def get_current_user(
    token: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get current authenticated user
    """
    from app.core.security import verify_token

    payload = verify_token(token)
    user_id = int(payload.get("sub"))

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {
        "id": user.id,
        "strava_id": user.strava_id,
        "username": user.username,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "profile_picture": user.profile_picture,
        "total_points": user.total_points,
        "level": user.level,
        "is_premium": user.is_premium,
    }
