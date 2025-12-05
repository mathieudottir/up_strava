"""
User model - represents athletes from Strava
"""
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.database import Base


class User(Base):
    """
    User/Athlete model linked to Strava account
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    strava_id = Column(BigInteger, unique=True, index=True, nullable=False)
    username = Column(String, index=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String, unique=True, index=True)
    profile_picture = Column(String, nullable=True)

    # OAuth tokens
    access_token = Column(String, nullable=False)
    refresh_token = Column(String, nullable=False)
    token_expires_at = Column(DateTime, nullable=False)

    # Gamification stats
    total_points = Column(Integer, default=0)
    level = Column(Integer, default=1)

    # Account status
    is_active = Column(Boolean, default=True)
    is_premium = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_sync = Column(DateTime, nullable=True)

    # Relationships
    activities = relationship("Activity", back_populates="user", cascade="all, delete-orphan")
    user_badges = relationship("UserBadge", back_populates="user", cascade="all, delete-orphan")
    leaderboard_entries = relationship("LeaderboardEntry", back_populates="user", cascade="all, delete-orphan")
    user_challenges = relationship("UserChallenge", back_populates="user", cascade="all, delete-orphan")
