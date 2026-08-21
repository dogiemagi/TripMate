from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class WeatherQuery(BaseModel):
    city: str
    days: Optional[int] = 7

class ItineraryRequest(BaseModel):
    destination: str = Field(..., example="Tokyo, Japan")
    days: int = Field(default=3, ge=1, le=14)
    travel_style: str = Field(default="Balanced", example="Adventure | Cultural | Foodie | Luxury | Budget | Balanced")
    pace: str = Field(default="Moderate", example="Relaxed | Moderate | Fast-Paced")
    interests: List[str] = Field(default=["Food", "Sightseeing", "Photography", "Culture"])
    budget_level: str = Field(default="Moderate", example="Backpacker | Moderate | Premium | Luxury")

class FoodQuery(BaseModel):
    city: str = Field(..., example="Rome")
    dietary_preferences: Optional[List[str]] = Field(default=[])

class CurrencyConvertRequest(BaseModel):
    from_currency: str = Field(default="USD", example="USD")
    to_currency: str = Field(default="EUR", example="EUR")
    amount: float = Field(default=100.0, gt=0)

class PackingChecklistRequest(BaseModel):
    destination: str = Field(..., example="Kyoto")
    days: int = Field(default=5, ge=1)
    season: str = Field(default="Spring", example="Spring | Summer | Autumn | Winter")
    activities: List[str] = Field(default=["Walking", "Sightseeing", "Dining", "Temple Visits"])
    gender_or_type: Optional[str] = "General"

class PhrasebookQuery(BaseModel):
    language: str = Field(default="Japanese", example="Japanese | Spanish | French | Italian | German | Hindi | Arabic")
    category: Optional[str] = Field(default="All", example="Greetings | Dining | Emergency | Transport | Shopping | All")
