"""
Activity model - represents Strava activities
"""
from sqlalchemy import Column, Integer, String, DateTime, Float, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.database import Base


class Activity(Base):
    """
    Activity model from Strava (runs, rides, etc.)
    """
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    strava_activity_id = Column(BigInteger, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Activity details
    name = Column(String, nullable=False)
    activity_type = Column(String, nullable=False)  # Run, Ride, Swim, etc.
    distance = Column(Float, nullable=False)  # meters
    moving_time = Column(Integer, nullable=False)  # seconds
    elapsed_time = Column(Integer, nullable=False)  # seconds
    total_elevation_gain = Column(Float, default=0)  # meters
    average_speed = Column(Float, nullable=True)  # m/s
    max_speed = Column(Float, nullable=True)  # m/s
    average_heartrate = Column(Float, nullable=True)
    max_heartrate = Column(Float, nullable=True)
    average_watts = Column(Float, nullable=True)

    # Activity date and location
    start_date = Column(DateTime, nullable=False)
    timezone = Column(String, nullable=True)

    # Gamification
    points_earned = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="activities")
