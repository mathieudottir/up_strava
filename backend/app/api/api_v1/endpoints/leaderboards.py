"""
Leaderboard endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List
from pydantic import BaseModel

from app.db.database import get_db
from app.models.leaderboard import Leaderboard, LeaderboardEntry
from app.models.user import User

router = APIRouter()


class LeaderboardEntryResponse(BaseModel):
    rank: int
    user_id: int
    username: str | None
    firstname: str | None
    lastname: str | None
    profile_picture: str | None
    score: int


class LeaderboardResponse(BaseModel):
    id: int
    name: str
    description: str | None
    leaderboard_type: str
    entries: List[LeaderboardEntryResponse]


@router.get("/", response_model=List[LeaderboardResponse])
async def get_leaderboards(
    db: AsyncSession = Depends(get_db)
):
    """
    Get all active leaderboards
    """
    result = await db.execute(
        select(Leaderboard).where(Leaderboard.is_active == True)
    )
    leaderboards = result.scalars().all()

    response = []
    for lb in leaderboards:
        # Get entries for this leaderboard
        entries_result = await db.execute(
            select(LeaderboardEntry, User)
            .join(User)
            .where(LeaderboardEntry.leaderboard_id == lb.id)
            .order_by(LeaderboardEntry.rank)
            .limit(50)
        )

        entries = [
            LeaderboardEntryResponse(
                rank=entry.rank,
                user_id=user.id,
                username=user.username,
                firstname=user.firstname,
                lastname=user.lastname,
                profile_picture=user.profile_picture,
                score=entry.score
            )
            for entry, user in entries_result.all()
        ]

        response.append(
            LeaderboardResponse(
                id=lb.id,
                name=lb.name,
                description=lb.description,
                leaderboard_type=lb.leaderboard_type.value,
                entries=entries
            )
        )

    return response


@router.get("/global", response_model=List[LeaderboardEntryResponse])
async def get_global_leaderboard(
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """
    Get global leaderboard by total points
    """
    result = await db.execute(
        select(User)
        .where(User.is_active == True)
        .order_by(desc(User.total_points))
        .limit(limit)
    )
    users = result.scalars().all()

    return [
        LeaderboardEntryResponse(
            rank=idx + 1,
            user_id=user.id,
            username=user.username,
            firstname=user.firstname,
            lastname=user.lastname,
            profile_picture=user.profile_picture,
            score=user.total_points
        )
        for idx, user in enumerate(users)
    ]
