"""
Activity endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List
from pydantic import BaseModel
from datetime import datetime

from app.db.database import get_db
from app.models.activity import Activity
from app.models.user import User
from app.services.strava_service import StravaService
from app.services.gamification_service import GamificationService

router = APIRouter()
strava_service = StravaService()
gamification_service = GamificationService()


class ActivityResponse(BaseModel):
    id: int
    strava_activity_id: int
    name: str
    activity_type: str
    distance: float
    moving_time: int
    total_elevation_gain: float
    points_earned: int
    start_date: datetime


@router.get("/", response_model=List[ActivityResponse])
async def get_activities(
    user_id: int,
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db)
):
    """
    Get user activities
    """
    result = await db.execute(
        select(Activity)
        .where(Activity.user_id == user_id)
        .order_by(desc(Activity.start_date))
        .offset(skip)
        .limit(limit)
    )
    activities = result.scalars().all()

    return [
        ActivityResponse(
            id=a.id,
            strava_activity_id=a.strava_activity_id,
            name=a.name,
            activity_type=a.activity_type,
            distance=a.distance / 1000,  # Convert to km
            moving_time=a.moving_time,
            total_elevation_gain=a.total_elevation_gain,
            points_earned=a.points_earned,
            start_date=a.start_date
        )
        for a in activities
    ]


@router.post("/sync")
async def sync_activities(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Sync activities from Strava
    """
    # Get user
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Check if token needs refresh
    if user.token_expires_at < datetime.utcnow():
        # Refresh token
        token_data = await strava_service.refresh_access_token(user.refresh_token)
        user.access_token = token_data["access_token"]
        user.refresh_token = token_data["refresh_token"]
        user.token_expires_at = datetime.fromtimestamp(token_data["expires_at"])
        await db.commit()

    # Get activities from Strava
    strava_activities = await strava_service.get_activities(user.access_token)

    new_activities = 0
    for strava_activity in strava_activities:
        # Check if activity already exists
        existing = await db.execute(
            select(Activity).where(
                Activity.strava_activity_id == strava_activity["id"]
            )
        )
        if existing.scalar_one_or_none():
            continue

        # Calculate points
        points = gamification_service.calculate_activity_points(strava_activity)

        # Create activity
        activity = Activity(
            strava_activity_id=strava_activity["id"],
            user_id=user.id,
            name=strava_activity["name"],
            activity_type=strava_activity["type"],
            distance=strava_activity["distance"],
            moving_time=strava_activity["moving_time"],
            elapsed_time=strava_activity["elapsed_time"],
            total_elevation_gain=strava_activity.get("total_elevation_gain", 0),
            average_speed=strava_activity.get("average_speed"),
            max_speed=strava_activity.get("max_speed"),
            start_date=datetime.fromisoformat(strava_activity["start_date"].replace("Z", "+00:00")),
            points_earned=points
        )
        db.add(activity)

        # Update user points
        user.total_points += points
        user.level = gamification_service.calculate_level(user.total_points)

        new_activities += 1

    user.last_sync = datetime.utcnow()
    await db.commit()

    # Check for new badges
    earned_badges = await gamification_service.check_and_award_badges(db, user)

    return {
        "synced": new_activities,
        "total_points": user.total_points,
        "level": user.level,
        "new_badges": len(earned_badges)
    }
