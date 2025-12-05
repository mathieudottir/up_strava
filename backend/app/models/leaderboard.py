"""
Leaderboard models - rankings and competition
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum as SQLEnum, UniqueConstraint, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.database import Base


class LeaderboardType(str, enum.Enum):
    """Leaderboard category types"""
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    ALL_TIME = "all_time"
    SEGMENT = "segment"


class Leaderboard(Base):
    """
    Leaderboard definition
    """
    __tablename__ = "leaderboards"

    id = Column(Integer, primary_key=True, index=True)

    # Leaderboard details
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    leaderboard_type = Column(SQLEnum(LeaderboardType), nullable=False)

    # Period (for time-based leaderboards)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)

    # Segment specific (optional)
    segment_id = Column(Integer, ForeignKey("segments.id"), nullable=True)

    # Status
    is_active = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    entries = relationship("LeaderboardEntry", back_populates="leaderboard", cascade="all, delete-orphan")


class LeaderboardEntry(Base):
    """
    User entries in leaderboards
    """
    __tablename__ = "leaderboard_entries"

    id = Column(Integer, primary_key=True, index=True)

    leaderboard_id = Column(Integer, ForeignKey("leaderboards.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Ranking
    rank = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)  # Points, distance, or time

    # Timestamps
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Ensure one entry per user per leaderboard
    __table_args__ = (
        UniqueConstraint('leaderboard_id', 'user_id', name='unique_leaderboard_user'),
    )

    # Relationships
    leaderboard = relationship("Leaderboard", back_populates="entries")
    user = relationship("User", back_populates="leaderboard_entries")
