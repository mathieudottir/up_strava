"""
Challenge endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from pydantic import BaseModel
from datetime import datetime

from app.db.database import get_db
from app.models.challenge import Challenge, UserChallenge

router = APIRouter()


class ChallengeResponse(BaseModel):
    id: int
    name: str
    description: str
    challenge_type: str
    target_value: int
    points_reward: int
    start_date: datetime
    end_date: datetime
    is_active: bool
    image_url: str | None
    user_progress: int | None = None
    is_completed: bool = False


@router.get("/", response_model=List[ChallengeResponse])
async def get_challenges(
    user_id: int | None = None,
    active_only: bool = True,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all challenges, optionally showing user's progress
    """
    # Get challenges
    query = select(Challenge)
    if active_only:
        query = query.where(Challenge.is_active == True)

    result = await db.execute(query)
    challenges = result.scalars().all()

    # Get user's progress if user_id provided
    user_progress_map = {}
    if user_id:
        user_challenges_result = await db.execute(
            select(UserChallenge).where(UserChallenge.user_id == user_id)
        )
        for uc in user_challenges_result.scalars().all():
            user_progress_map[uc.challenge_id] = (uc.current_progress, uc.is_completed)

    return [
        ChallengeResponse(
            id=c.id,
            name=c.name,
            description=c.description,
            challenge_type=c.challenge_type.value,
            target_value=c.target_value,
            points_reward=c.points_reward,
            start_date=c.start_date,
            end_date=c.end_date,
            is_active=c.is_active,
            image_url=c.image_url,
            user_progress=user_progress_map.get(c.id, (0, False))[0],
            is_completed=user_progress_map.get(c.id, (0, False))[1]
        )
        for c in challenges
    ]


@router.post("/{challenge_id}/join")
async def join_challenge(
    challenge_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Join a challenge
    """
    # Check if challenge exists
    result = await db.execute(
        select(Challenge).where(Challenge.id == challenge_id)
    )
    challenge = result.scalar_one_or_none()

    if not challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Challenge not found"
        )

    # Check if user already joined
    existing = await db.execute(
        select(UserChallenge).where(
            UserChallenge.user_id == user_id,
            UserChallenge.challenge_id == challenge_id
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already joined this challenge"
        )

    # Create user challenge
    user_challenge = UserChallenge(
        user_id=user_id,
        challenge_id=challenge_id,
        current_progress=0,
        is_completed=False
    )
    db.add(user_challenge)
    await db.commit()

    return {"message": "Successfully joined challenge"}


@router.get("/user/{user_id}", response_model=List[ChallengeResponse])
async def get_user_challenges(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get challenges a user has joined
    """
    result = await db.execute(
        select(UserChallenge, Challenge)
        .join(Challenge)
        .where(UserChallenge.user_id == user_id)
    )

    challenges_data = result.all()

    return [
        ChallengeResponse(
            id=challenge.id,
            name=challenge.name,
            description=challenge.description,
            challenge_type=challenge.challenge_type.value,
            target_value=challenge.target_value,
            points_reward=challenge.points_reward,
            start_date=challenge.start_date,
            end_date=challenge.end_date,
            is_active=challenge.is_active,
            image_url=challenge.image_url,
            user_progress=user_challenge.current_progress,
            is_completed=user_challenge.is_completed
        )
        for user_challenge, challenge in challenges_data
    ]
