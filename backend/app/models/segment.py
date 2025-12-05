"""
Segment models - represents Strava segments and efforts
"""
from sqlalchemy import Column, Integer, String, DateTime, Float, BigInteger, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.database import Base


class Segment(Base):
    """
    Segment model from Strava
    """
    __tablename__ = "segments"

    id = Column(Integer, primary_key=True, index=True)
    strava_segment_id = Column(BigInteger, unique=True, index=True, nullable=False)

    # Segment details
    name = Column(String, nullable=False)
    activity_type = Column(String, nullable=False)
    distance = Column(Float, nullable=False)  # meters
    average_grade = Column(Float, nullable=True)
    maximum_grade = Column(Float, nullable=True)
    elevation_high = Column(Float, nullable=True)
    elevation_low = Column(Float, nullable=True)
    total_elevation_gain = Column(Float, nullable=True)

    # Location
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    country = Column(String, nullable=True)
    start_latlng = Column(JSON, nullable=True)
    end_latlng = Column(JSON, nullable=True)

    # Stats
    effort_count = Column(Integer, default=0)
    athlete_count = Column(Integer, default=0)

    # Gamification
    base_points = Column(Integer, default=100)
    difficulty_multiplier = Column(Float, default=1.0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    efforts = relationship("SegmentEffort", back_populates="segment", cascade="all, delete-orphan")


class SegmentEffort(Base):
    """
    Segment effort - a user's attempt at a segment
    """
    __tablename__ = "segment_efforts"

    id = Column(Integer, primary_key=True, index=True)
    strava_effort_id = Column(BigInteger, unique=True, index=True, nullable=False)

    segment_id = Column(Integer, ForeignKey("segments.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Effort details
    elapsed_time = Column(Integer, nullable=False)  # seconds
    moving_time = Column(Integer, nullable=False)  # seconds
    start_date = Column(DateTime, nullable=False)

    # Performance metrics
    average_heartrate = Column(Float, nullable=True)
    max_heartrate = Column(Float, nullable=True)
    average_watts = Column(Float, nullable=True)

    # Ranking
    kom_rank = Column(Integer, nullable=True)
    pr_rank = Column(Integer, nullable=True)

    # Gamification
    points_earned = Column(Integer, default=0)
    is_personal_best = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    segment = relationship("Segment", back_populates="efforts")
