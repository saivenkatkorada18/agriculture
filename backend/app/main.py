"""
Soil & Crop Health Analyzer — FastAPI Application Entrypoint
"""
from pathlib import Path
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from backend.app.config import settings, DATA_DIR, UPLOAD_DIR, SAMPLE_DIR
from backend.app.api.routes import analyze, analyses, chat, crops, health

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Production-grade AI & Computer Vision platform for agricultural plant disease detection, "
        "soil surface inspection, and AI agronomic assistance."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for image previews & uploads
DATA_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
SAMPLE_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/static/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")
app.mount("/static/samples", StaticFiles(directory=str(SAMPLE_DIR)), name="samples")

# Register API Routers under prefix
api_prefix = settings.api_prefix
app.include_router(analyze.router, prefix=api_prefix)
app.include_router(analyses.router, prefix=api_prefix)
app.include_router(chat.router, prefix=api_prefix)
app.include_router(crops.router, prefix=api_prefix)
app.include_router(health.router, prefix=api_prefix)
app.include_router(health.router)  # also available directly at /health


# Global exception handler for graceful JSON errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An internal server error occurred. Please try again or verify inputs.",
            "type": exc.__class__.__name__,
        },
    )


@app.get("/", tags=["Root"])
async def root():
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs_url": "/docs",
        "health_url": "/health",
        "api_prefix": settings.api_prefix,
    }
