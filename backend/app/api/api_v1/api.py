"""
Main API router
"""
from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, activities, users, leaderboards, badges, challenges

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(activities.router, prefix="/activities", tags=["activities"])
api_router.include_router(leaderboards.router, prefix="/leaderboards", tags=["leaderboards"])
api_router.include_router(badges.router, prefix="/badges", tags=["badges"])
api_router.include_router(challenges.router, prefix="/challenges", tags=["challenges"])
