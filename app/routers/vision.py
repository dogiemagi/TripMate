from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from app.services.gemini_vision_service import MultimodalVisionService

router = APIRouter(prefix="/api/v1/vision", tags=["Multimodal Vision AI"])

@router.post("/analyze")
async def analyze_landmark_or_menu(
    file: UploadFile = File(...),
    mode: str = Form(default="landmark", description="landmark | menu | luggage | scene"),
    prompt: Optional[str] = Form(default=None, description="Optional custom AI question or prompt")
):
    """
    Multimodal Visual Intelligence:
    - Landmark identification & historical breakdown
    - Foreign menu translation, ingredient check & allergen scanner
    - Photo-based travel tips and optimal photography angles
    """
    try:
        contents = await file.read()
        return await MultimodalVisionService.analyze_image(
            image_bytes=contents,
            filename=file.filename or "upload.jpg",
            mode=mode,
            user_prompt=prompt
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Visual analysis failed: {str(e)}")
