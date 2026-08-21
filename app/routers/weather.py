from fastapi import APIRouter, Query
from app.services.weather_service import WeatherService

router = APIRouter(prefix="/api/v1/weather", tags=["Weather & Forecast"])

@router.get("")
async def get_weather(
    city: str = Query(default="Tokyo", description="Destination city name"),
    days: int = Query(default=7, ge=1, le=14, description="Forecast days count")
):
    """
    Get live weather, 7-day forecast, travel climate score, and packing suggestions.
    """
    return await WeatherService.get_weather(city_name=city, days=days)
