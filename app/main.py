import os
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from app.config import settings
from app.routers import (
    weather,
    vision,
    itinerary,
    food,
    budget,
    packing,
    phrasebook
)

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("voyage.main")

# FastAPI App
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "VoyageAI is a production-grade, multimodal AI travel platform. "
        "It integrates real-time weather forecasts, AI multimodal vision analysis, "
        "interactive day-by-day trip planning, gastronomy discovery, currency conversions, "
        "smart packing checklists, and multilingual audio phrasebooks."
    ),
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(weather.router)
app.include_router(vision.router)
app.include_router(itinerary.router)
app.include_router(food.router)
app.include_router(budget.router)
app.include_router(packing.router)
app.include_router(phrasebook.router)

# Healthcheck for Render & Cloud Monitors
@app.get("/healthz", tags=["System"])
async def healthcheck():
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }

# Mount static web frontend files
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    @app.get("/", include_in_schema=False)
    async def serve_index():
        return FileResponse(os.path.join(static_dir, "index.html"))

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global error on {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "An internal server error occurred.",
            "detail": str(exc) if settings.DEBUG else "Please contact support."
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
