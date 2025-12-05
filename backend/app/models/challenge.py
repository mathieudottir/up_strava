"""
Challenge models - time-based challenges and competitions
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.database import Base


class ChallengeType(str, enum.Enum):
    """Challenge types"""
    DISTANCE = "distance"
    ELEVATION = "elevation"
    ACTIVITIES = "activities"
    TIME = "time"
    SEGMENTS = "segments"


class Challenge(Base):
    """
    Challenge definition - time-bound competitive goals
    """
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)

    # Challenge details
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    challenge_type = Column(SQLEnum(ChallengeType), nullable=False)

    # Target and rewards
    target_value = Column(Integer, nullable=False)  # e.g., 100km, 10 activities
    points_reward = Column(Integer, default=0)

    # Period
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    # Status
    is_active = Column(Boolean, default=True)

    # Visual
    image_url = Column(String, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user_challenges = relationship("UserChallenge", back_populates="challenge", cascade="all, delete-orphan")


class UserChallenge(Base):
    """
    User participation in challenges
    """
    __tablename__ = "user_challenges"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    challenge_id = Column(Integer, ForeignKey("challenges.id"), nullable=False)

    # Progress tracking
    current_progress = Column(Integer, default=0)
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)

    # Timestamps
    joined_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="user_challenges")
    challenge = relationship("Challenge", back_populates="user_challenges")
