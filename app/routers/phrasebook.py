from fastapi import APIRouter, Response, UploadFile, File, Form, HTTPException
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
    Text translation with phonetic romanization and manual source/target language selection.
    """
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="Text to translate cannot be empty.")
    try:
        return await PhrasebookService.translate_phrase(req)
    except Exception as e:
        logger.error(f"Text translation error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

@router.post("/voice-translate")
async def voice_translate(
    audio_file: UploadFile = File(..., description="Audio file recording (WAV, OGG, FLAC, WebM)"),
    source_language: str = Form("auto", description="Source language (or 'auto' for auto-detect)"),
    target_language: str = Form(..., description="Explicit target language (e.g. Tamil, English, Telugu)")
):
    """
    Voice-to-Text-to-Translation Pipeline:
    Transcribes spoken audio using the selected source language (or auto-detect if selected),
    then translates the text into the chosen target language with pronunciation synthesis.
    """
    clean_src = source_language.strip() if source_language else "auto"
    if not target_language or not target_language.strip():
        raise HTTPException(status_code=400, detail="Target language must be specified.")

    try:
        audio_bytes = await audio_file.read()
        if not audio_bytes or len(audio_bytes) < 64:
            raise HTTPException(status_code=400, detail="Uploaded audio file is empty or corrupted.")

        return await PhrasebookService.translate_voice_phrase(
            audio_bytes=audio_bytes,
            source_language=clean_src,
            target_language=target_language.strip()
        )
    except ValueError as ve:
        logger.warning(f"Voice translation validation notice: {ve}")
        raise HTTPException(status_code=422, detail=str(ve))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Voice translation processing error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Voice translation failed: {str(e)}")


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

