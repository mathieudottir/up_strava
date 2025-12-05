"""
Badge models - gamification badges and achievements
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.database import Base


class BadgeType(str, enum.Enum):
    """Badge category types"""
    DISTANCE = "distance"
    ELEVATION = "elevation"
    SPEED = "speed"
    CONSISTENCY = "consistency"
    CHALLENGE = "challenge"
    SPECIAL = "special"


class Badge(Base):
    """
    Badge/Achievement definition
    """
    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)

    # Badge details
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=False)
    badge_type = Column(SQLEnum(BadgeType), nullable=False)
    icon_url = Column(String, nullable=True)

    # Requirements
    requirement_value = Column(Integer, nullable=False)  # e.g., 100km, 1000m elevation
    requirement_description = Column(Text, nullable=True)

    # Gamification
    points_reward = Column(Integer, default=0)
    rarity = Column(String, default="common")  # common, rare, epic, legendary

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user_badges = relationship("UserBadge", back_populates="badge", cascade="all, delete-orphan")


class UserBadge(Base):
    """
    User earned badges
    """
    __tablename__ = "user_badges"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    badge_id = Column(Integer, ForeignKey("badges.id"), nullable=False)

    # Earned details
    earned_at = Column(DateTime, default=datetime.utcnow)
    progress = Column(Integer, default=0)  # Current progress towards badge

    # Relationships
    user = relationship("User", back_populates="user_badges")
    badge = relationship("Badge", back_populates="user_badges")
