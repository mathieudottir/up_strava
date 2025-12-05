"""
Main FastAPI application entry point for Strava Gamification Platform
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.db.database import init_db
from app.api.api_v1.api import api_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup
    logger.info("Starting up Strava Gamification Platform...")
    await init_db()
    logger.info("Database initialized successfully")

    yield

    # Shutdown
    logger.info("Shutting down Strava Gamification Platform...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Gamification platform for Strava activities with points, badges, and leaderboards",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    """
    Root endpoint - health check
    """
    return {
        "message": "Strava Gamification Platform API",
        "version": "1.0.0",
        "status": "active"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}
