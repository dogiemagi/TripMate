from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class WeatherQuery(BaseModel):
    city: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    days: Optional[int] = 7

class ItineraryRequest(BaseModel):
    destination: str = Field(..., example="Delhi, India")
    days: int = Field(default=3, ge=1, le=14)
    travel_style: str = Field(default="Balanced", example="Adventure | Cultural | Foodie | Luxury | Budget | Balanced")
    pace: str = Field(default="Moderate", example="Relaxed | Moderate | Fast-Paced")
    interests: List[str] = Field(default=["Food", "Sightseeing", "Photography", "Culture"])
    budget_level: str = Field(default="Moderate", example="Backpacker | Moderate | Premium | Luxury")

class FoodQuery(BaseModel):
    city: str = Field(..., example="Rome")
    dietary_preferences: Optional[List[str]] = Field(default=[])

class CurrencyConvertRequest(BaseModel):
    from_currency: str = Field(default="INR", example="INR")
    to_currency: str = Field(default="USD", example="USD")
    amount: float = Field(default=1000.0, gt=0)

class PackingChecklistRequest(BaseModel):
    destination: str = Field(..., example="Goa")
    days: int = Field(default=5, ge=1)
    season: str = Field(default="Summer", example="Spring | Summer | Autumn | Winter")
    activities: List[str] = Field(default=["Walking", "Sightseeing", "Dining", "Beach"])
    gender_or_type: Optional[str] = "General"

class PhrasebookQuery(BaseModel):
    language: str = Field(default="Hindi", example="Hindi | Tamil | Telugu | Urdu | Bengali | Marathi | Japanese | French")
    category: Optional[str] = Field(default="All", example="Greetings | Dining | Emergency | Transport | Shopping | All")

class TranslationRequest(BaseModel):
    text: str = Field(..., example="Where is the train station?")
    source_language: str = Field(default="auto", example="auto | English | Tamil | Telugu | Hindi | French")
    target_language: str = Field(default="Tamil", example="Tamil | Telugu | English | Hindi | Japanese | French")

