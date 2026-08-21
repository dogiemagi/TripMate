from fastapi import APIRouter
from app.models.schemas import ItineraryRequest
from app.services.itinerary_service import ItineraryService

router = APIRouter(prefix="/api/v1/itinerary", tags=["Smart Itinerary Planner"])

@router.post("/generate")
async def generate_itinerary(request: ItineraryRequest):
    """
    Generate an interactive day-by-day travel plan with geocoded coordinates, activities, costs in INR, and timeline.
    """
    return await ItineraryService.generate_itinerary(request)
