"""
User endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from pydantic import BaseModel

from app.db.database import get_db
from app.models.user import User
from app.models.activity import Activity

router = APIRouter()


class UserProfile(BaseModel):
    id: int
    strava_id: int
    username: str | None
    firstname: str | None
    lastname: str | None
    profile_picture: str | None
    total_points: int
    level: int
    activity_count: int
    total_distance: float
    total_elevation: float


class UserStats(BaseModel):
    total_activities: int
    total_distance: float
    total_elevation: float
    total_points: int
    level: int
    badges_count: int


@router.get("/{user_id}", response_model=UserProfile)
async def get_user_profile(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get user profile with stats
    """
    # Get user
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Get activity stats
    activity_count_result = await db.execute(
        select(func.count(Activity.id)).where(Activity.user_id == user_id)
    )
    activity_count = activity_count_result.scalar() or 0

    distance_result = await db.execute(
        select(func.sum(Activity.distance)).where(Activity.user_id == user_id)
    )
    total_distance = distance_result.scalar() or 0

    elevation_result = await db.execute(
        select(func.sum(Activity.total_elevation_gain)).where(Activity.user_id == user_id)
    )
    total_elevation = elevation_result.scalar() or 0

    return UserProfile(
        id=user.id,
        strava_id=user.strava_id,
        username=user.username,
        firstname=user.firstname,
        lastname=user.lastname,
        profile_picture=user.profile_picture,
        total_points=user.total_points,
        level=user.level,
        activity_count=activity_count,
        total_distance=total_distance / 1000,  # Convert to km
        total_elevation=total_elevation
    )


@router.get("/{user_id}/stats", response_model=UserStats)
async def get_user_stats(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get detailed user statistics
    """
    from app.models.badge import UserBadge

    # Get user
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Get stats
    activity_count = await db.execute(
        select(func.count(Activity.id)).where(Activity.user_id == user_id)
    )
    total_activities = activity_count.scalar() or 0

    distance = await db.execute(
        select(func.sum(Activity.distance)).where(Activity.user_id == user_id)
    )
    total_distance = distance.scalar() or 0

    elevation = await db.execute(
        select(func.sum(Activity.total_elevation_gain)).where(Activity.user_id == user_id)
    )
    total_elevation = elevation.scalar() or 0

    badges = await db.execute(
        select(func.count(UserBadge.id)).where(UserBadge.user_id == user_id)
    )
    badges_count = badges.scalar() or 0

    return UserStats(
        total_activities=total_activities,
        total_distance=total_distance / 1000,
        total_elevation=total_elevation,
        total_points=user.total_points,
        level=user.level,
        badges_count=badges_count
    )
