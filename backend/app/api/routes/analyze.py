"""
Image Analysis Endpoints (Plant Disease & Soil Surface)
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse

from ml.preprocessing.image_preprocessor import validate_image_bytes
from backend.app.services.plant_service import plant_service
from backend.app.services.soil_service import soil_service
from backend.app.schemas.analysis import PlantAnalysisResult, SoilAnalysisResult

router = APIRouter(prefix="/analyze", tags=["Image Analysis"])


@router.post(
    "/plant",
    response_model=PlantAnalysisResult,
    summary="Analyze Crop Foliage for Plant Diseases",
    description="Uploads a crop leaf image (JPG/PNG/WEBP) and executes CNN/CV classification to detect diseases, confidence scores, and recommendations."
)
async def analyze_plant_disease(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No image file provided.")

    image_bytes = await file.read()
    is_valid, err_msg, _ = validate_image_bytes(image_bytes)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=err_msg or "Invalid image file."
        )

    try:
        result = plant_service.process_and_analyze(image_bytes, filename=file.filename or "leaf.jpg")
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Plant disease analysis failed: {str(e)}"
        )


@router.post(
    "/soil",
    response_model=SoilAnalysisResult,
    summary="Analyze Soil Surface Characteristics",
    description="Uploads a soil surface image and runs computer vision to estimate apparent moisture, surface cracking, soil color classification, texture, and organic residue."
)
async def analyze_soil_surface(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No image file provided.")

    image_bytes = await file.read()
    is_valid, err_msg, _ = validate_image_bytes(image_bytes)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=err_msg or "Invalid image file."
        )

    try:
        result = soil_service.process_and_analyze(image_bytes, filename=file.filename or "soil.jpg")
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Soil surface analysis failed: {str(e)}"
        )
