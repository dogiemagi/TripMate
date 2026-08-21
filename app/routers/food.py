from fastapi import APIRouter
from app.models.schemas import FoodQuery
from app.services.food_service import FoodService

router = APIRouter(prefix="/api/v1/food", tags=["Gastronomy & Dining"])

@router.post("/explore")
async def explore_food(query: FoodQuery):
    """
    Explore regional gastronomy, signature dishes with pronunciations, spots to try, and dietary filters.
    """
    return FoodService.get_city_gastronomy(query)

@router.get("")
async def get_food_by_city(city: str = "Rome"):
    """
    Quick GET endpoint for city food discovery.
    """
    return FoodService.get_city_gastronomy(FoodQuery(city=city))
