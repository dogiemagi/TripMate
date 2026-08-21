from fastapi import APIRouter
from app.models.schemas import PhrasebookQuery
from app.services.phrasebook_service import PhrasebookService

router = APIRouter(prefix="/api/v1/phrasebook", tags=["Audio Phrasebook & Guide"])

@router.post("/phrases")
async def get_phrases(query: PhrasebookQuery):
    """
    Multilingual travel phrases with phonetic romanization and speech synthesis config.
    """
    return PhrasebookService.get_phrases(query)
