from fastapi import APIRouter, Query
from app.models.schemas import CurrencyConvertRequest
from app.services.currency_service import CurrencyBudgetService

router = APIRouter(prefix="/api/v1/budget", tags=["Currency & Budget"])

@router.post("/convert")
async def convert_currency(request: CurrencyConvertRequest):
    """
    Real-time foreign exchange converter.
    """
    return await CurrencyBudgetService.convert(request)

@router.get("/estimate")
async def estimate_budget(
    city: str = Query(default="Tokyo"),
    days: int = Query(default=5, ge=1, le=30),
    style: str = Query(default="midrange", description="backpacker | midrange | luxury")
):
    """
    Calculate estimated travel expense breakdown (hotel, food, transit, activities).
    """
    return CurrencyBudgetService.get_trip_budget_estimate(city=city, days=days, style=style)
