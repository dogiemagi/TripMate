from fastapi import APIRouter, Response
from app.models.schemas import PhrasebookQuery, TranslationRequest
from app.services.phrasebook_service import PhrasebookService
import httpx
import logging

logger = logging.getLogger("voyage.phrasebook")
router = APIRouter(prefix="/api/v1/phrasebook", tags=["Audio Phrasebook & Guide"])

@router.post("/phrases")
async def get_phrases(query: PhrasebookQuery):
    """
    Multilingual travel phrases with phonetic romanization and speech synthesis config.
    """
    return PhrasebookService.get_phrases(query)

@router.post("/translate")
async def translate_text(req: TranslationRequest):
    """
    Live voice & text translation with phonetic romanization and pronunciation synthesis.
    """
    return await PhrasebookService.translate_phrase(req)


@router.get("/audio")
async def get_phrase_audio(text: str, lang: str = "hi"):
    """
    Streams crisp native audio pronunciation using high-fidelity TTS.
    Works unconditionally on all devices and browsers.
    """
    lang_clean = lang.split("-")[0].lower()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://translate.google.com/"
    }
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.get(
                "https://translate.google.com/translate_tts",
                params={"ie": "UTF-8", "tl": lang_clean, "client": "tw-ob", "q": text},
                headers=headers
            )
            if resp.status_code == 200 and len(resp.content) > 100:
                return Response(
                    content=resp.content,
                    media_type="audio/mpeg",
                    headers={"Cache-Control": "public, max-age=86400"}
                )
    except Exception as e:
        logger.warning(f"Audio TTS fetch error: {e}")

    return Response(status_code=404)

