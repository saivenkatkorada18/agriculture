"""
System Health & Status Endpoint
"""
import time
from fastapi import APIRouter
from backend.app.schemas.health import SystemHealthResponse
from backend.app.config import settings
from backend.app.ml.plant_classifier import PlantDiseaseClassifier

router = APIRouter(tags=["Health & Status"])
START_TIME = time.time()


@router.get(
    "/health",
    response_model=SystemHealthResponse,
    summary="System Health & Model Status",
    description="Returns backend server health, ML engine loading status, database mode, and uptime."
)
async def check_health():
    classifier = PlantDiseaseClassifier()
    return {
        "status": "healthy",
        "version": settings.app_version,
        "environment": settings.app_env,
        "ml_engine": {
            "neural_model_loaded": classifier.model_loaded,
            "inference_mode": "CNN_MobileNetV2" if classifier.model_loaded else "CV_Foliar_Engine",
            "model_path": str(classifier.model_path),
            "confidence_threshold": settings.confidence_threshold,
        },
        "database": {
            "mode": "supabase" if (settings.supabase_url and settings.supabase_anon_key) else "local_sqlite",
            "status": "connected",
        },
        "supported_classes_count": len(classifier.classes),
        "uptime_seconds": round(time.time() - START_TIME, 2),
    }
