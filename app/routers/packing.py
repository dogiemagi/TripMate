from fastapi import APIRouter
from app.models.schemas import PackingChecklistRequest
from app.services.packing_service import PackingService

router = APIRouter(prefix="/api/v1/packing", tags=["Smart Packing Assistant"])

@router.post("/generate")
async def generate_packing_list(request: PackingChecklistRequest):
    """
    Generate climate & activity-aware packing checklist with essential luggage recommendations.
    """
    return PackingService.generate_checklist(request)
