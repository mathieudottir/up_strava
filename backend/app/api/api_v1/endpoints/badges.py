"""
Badge endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from pydantic import BaseModel
from datetime import datetime

from app.db.database import get_db
from app.models.badge import Badge, UserBadge

router = APIRouter()


class BadgeResponse(BaseModel):
    id: int
    name: str
    description: str
    badge_type: str
    icon_url: str | None
    points_reward: int
    rarity: str
    is_earned: bool = False
    earned_at: datetime | None = None


@router.get("/", response_model=List[BadgeResponse])
async def get_all_badges(
    user_id: int | None = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all badges, optionally showing user's earned status
    """
    # Get all badges
    result = await db.execute(select(Badge))
    badges = result.scalars().all()

    # Get user's earned badges if user_id provided
    earned_badges_map = {}
    if user_id:
        user_badges_result = await db.execute(
            select(UserBadge).where(UserBadge.user_id == user_id)
        )
        for ub in user_badges_result.scalars().all():
            earned_badges_map[ub.badge_id] = ub.earned_at

    return [
        BadgeResponse(
            id=b.id,
            name=b.name,
            description=b.description,
            badge_type=b.badge_type.value,
            icon_url=b.icon_url,
            points_reward=b.points_reward,
            rarity=b.rarity,
            is_earned=b.id in earned_badges_map,
            earned_at=earned_badges_map.get(b.id)
        )
        for b in badges
    ]


@router.get("/user/{user_id}", response_model=List[BadgeResponse])
async def get_user_badges(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all badges earned by a user
    """
    result = await db.execute(
        select(UserBadge, Badge)
        .join(Badge)
        .where(UserBadge.user_id == user_id)
    )

    badges_data = result.all()

    return [
        BadgeResponse(
            id=badge.id,
            name=badge.name,
            description=badge.description,
            badge_type=badge.badge_type.value,
            icon_url=badge.icon_url,
            points_reward=badge.points_reward,
            rarity=badge.rarity,
            is_earned=True,
            earned_at=user_badge.earned_at
        )
        for user_badge, badge in badges_data
    ]
