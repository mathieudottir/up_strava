"""
Gamification service - points, badges, and leveling system
"""
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.models.activity import Activity
from app.models.badge import Badge, UserBadge
from app.models.segment import SegmentEffort


class GamificationService:
    """
    Service for managing gamification logic
    """

    # Points multipliers by activity type
    ACTIVITY_TYPE_MULTIPLIERS = {
        "Run": 1.0,
        "Ride": 0.8,
        "Swim": 1.2,
        "Hike": 0.9,
        "Walk": 0.7,
        "VirtualRide": 0.6,
        "VirtualRun": 0.7,
    }

    @staticmethod
    def calculate_activity_points(activity_data: Dict[str, Any]) -> int:
        """
        Calculate points for an activity based on various metrics
        """
        distance_km = activity_data.get("distance", 0) / 1000
        elevation_m = activity_data.get("total_elevation_gain", 0)
        moving_time_hours = activity_data.get("moving_time", 0) / 3600
        activity_type = activity_data.get("type", "Run")

        # Base points from distance (1 point per km)
        distance_points = distance_km * 10

        # Elevation bonus (1 point per 10m)
        elevation_points = elevation_m / 10

        # Time bonus (5 points per hour)
        time_points = moving_time_hours * 5

        # Total base points
        base_points = distance_points + elevation_points + time_points

        # Apply activity type multiplier
        multiplier = GamificationService.ACTIVITY_TYPE_MULTIPLIERS.get(activity_type, 1.0)
        total_points = int(base_points * multiplier)

        return max(total_points, 1)  # Minimum 1 point

    @staticmethod
    def calculate_segment_effort_points(
        segment_data: Dict[str, Any],
        effort_data: Dict[str, Any],
        is_pr: bool = False
    ) -> int:
        """
        Calculate points for a segment effort
        """
        base_points = 50  # Base points for completing a segment

        # PR bonus
        if is_pr:
            base_points += 100

        # KOM/QOM ranking bonus
        kom_rank = effort_data.get("kom_rank")
        if kom_rank:
            if kom_rank == 1:
                base_points += 500
            elif kom_rank <= 3:
                base_points += 300
            elif kom_rank <= 10:
                base_points += 100

        return base_points

    @staticmethod
    def calculate_level(total_points: int) -> int:
        """
        Calculate user level based on total points
        Level formula: level = floor(sqrt(total_points / 100))
        """
        import math
        return max(1, math.floor(math.sqrt(total_points / 100)))

    @staticmethod
    async def check_and_award_badges(
        db: AsyncSession,
        user: User,
        activity: Activity = None
    ) -> list:
        """
        Check if user qualifies for any new badges
        Returns list of newly earned badges
        """
        earned_badges = []

        # Get all badges
        result = await db.execute(select(Badge))
        all_badges = result.scalars().all()

        # Get user's current badges
        user_badges_result = await db.execute(
            select(UserBadge).where(UserBadge.user_id == user.id)
        )
        user_badge_ids = {ub.badge_id for ub in user_badges_result.scalars().all()}

        # Check each badge
        for badge in all_badges:
            if badge.id in user_badge_ids:
                continue  # Already earned

            # Check if user qualifies (simplified logic)
            qualifies = await GamificationService._check_badge_qualification(
                db, user, badge
            )

            if qualifies:
                # Award badge
                user_badge = UserBadge(
                    user_id=user.id,
                    badge_id=badge.id,
                    progress=badge.requirement_value
                )
                db.add(user_badge)

                # Award points
                user.total_points += badge.points_reward
                user.level = GamificationService.calculate_level(user.total_points)

                earned_badges.append(badge)

        await db.commit()
        return earned_badges

    @staticmethod
    async def _check_badge_qualification(
        db: AsyncSession,
        user: User,
        badge: Badge
    ) -> bool:
        """
        Check if user qualifies for a specific badge
        """
        from sqlalchemy import func

        if badge.badge_type == "distance":
            # Check total distance across all activities
            result = await db.execute(
                select(func.sum(Activity.distance)).where(Activity.user_id == user.id)
            )
            total_distance = result.scalar() or 0
            return (total_distance / 1000) >= badge.requirement_value

        elif badge.badge_type == "elevation":
            # Check total elevation gain
            result = await db.execute(
                select(func.sum(Activity.total_elevation_gain)).where(Activity.user_id == user.id)
            )
            total_elevation = result.scalar() or 0
            return total_elevation >= badge.requirement_value

        elif badge.badge_type == "consistency":
            # Check number of activities
            result = await db.execute(
                select(func.count(Activity.id)).where(Activity.user_id == user.id)
            )
            activity_count = result.scalar() or 0
            return activity_count >= badge.requirement_value

        return False
