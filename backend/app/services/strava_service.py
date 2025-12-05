"""
Strava API integration service
"""
import httpx
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from app.core.config import settings


class StravaService:
    """
    Service for interacting with Strava API
    """
    BASE_URL = "https://www.strava.com/api/v3"
    OAUTH_URL = "https://www.strava.com/oauth"

    def __init__(self):
        self.client_id = settings.STRAVA_CLIENT_ID
        self.client_secret = settings.STRAVA_CLIENT_SECRET
        self.redirect_uri = settings.STRAVA_REDIRECT_URI

    async def get_authorization_url(self, state: str = None) -> str:
        """
        Generate Strava OAuth authorization URL
        """
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": "read,activity:read_all,profile:read_all",
        }
        if state:
            params["state"] = state

        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{self.OAUTH_URL}/authorize?{query_string}"

    async def exchange_token(self, code: str) -> Dict[str, Any]:
        """
        Exchange authorization code for access token
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.OAUTH_URL}/token",
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "code": code,
                    "grant_type": "authorization_code",
                }
            )
            response.raise_for_status()
            return response.json()

    async def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Refresh expired access token
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.OAUTH_URL}/token",
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "refresh_token": refresh_token,
                    "grant_type": "refresh_token",
                }
            )
            response.raise_for_status()
            return response.json()

    async def get_athlete(self, access_token: str) -> Dict[str, Any]:
        """
        Get authenticated athlete profile
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/athlete",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            response.raise_for_status()
            return response.json()

    async def get_activities(
        self,
        access_token: str,
        after: Optional[int] = None,
        page: int = 1,
        per_page: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Get athlete activities
        """
        params = {"page": page, "per_page": per_page}
        if after:
            params["after"] = after

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/athlete/activities",
                headers={"Authorization": f"Bearer {access_token}"},
                params=params
            )
            response.raise_for_status()
            return response.json()

    async def get_activity(self, access_token: str, activity_id: int) -> Dict[str, Any]:
        """
        Get detailed activity data
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/activities/{activity_id}",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            response.raise_for_status()
            return response.json()

    async def get_segment(self, access_token: str, segment_id: int) -> Dict[str, Any]:
        """
        Get segment details
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/segments/{segment_id}",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            response.raise_for_status()
            return response.json()
