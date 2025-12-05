"""
Database models
"""
from app.models.user import User
from app.models.activity import Activity
from app.models.segment import Segment, SegmentEffort
from app.models.badge import Badge, UserBadge
from app.models.leaderboard import Leaderboard, LeaderboardEntry
from app.models.challenge import Challenge, UserChallenge

__all__ = [
    "User",
    "Activity",
    "Segment",
    "SegmentEffort",
    "Badge",
    "UserBadge",
    "Leaderboard",
    "LeaderboardEntry",
    "Challenge",
    "UserChallenge",
]
