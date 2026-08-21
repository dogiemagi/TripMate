from fastapi import APIRouter, Query
from typing import Optional
from app.services.weather_service import WeatherService

router = APIRouter(prefix="/api/v1/weather", tags=["Weather & Forecast"])

@router.get("")
async def get_weather(
    city: str = Query(default="Delhi", description="Destination city name"),
    start_date: Optional[str] = Query(default=None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(default=None, description="End date (YYYY-MM-DD)"),
    days: int = Query(default=7, ge=1, le=16, description="Forecast days count")
):
    """
    Get live weather and date-range filtered forecasts with climate scoring.
    """
    return await WeatherService.get_weather(
        city_name=city,
        start_date=start_date,
        end_date=end_date,
        days=days
    )
