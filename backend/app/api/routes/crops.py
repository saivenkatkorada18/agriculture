"""
Crops & Disease Encyclopedia Endpoints
"""
import json
from fastapi import APIRouter, HTTPException, status
from ml.config.config import DISEASE_INFO_PATH

router = APIRouter(prefix="/crops", tags=["Crop Encyclopedia"])


@router.get(
    "",
    summary="List Supported Crops & Diseases",
    description="Returns the complete agronomic dictionary of supported crops, diseases, symptoms, and organic/chemical controls."
)
async def list_supported_crops():
    if DISEASE_INFO_PATH.exists():
        with open(DISEASE_INFO_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"classes": {}}


@router.get(
    "/{crop_name}",
    summary="Get Diseases for a Specific Crop",
    description="Retrieves all registered diseases, symptoms, and treatments for a single crop family."
)
async def get_crop_diseases(crop_name: str):
    if not DISEASE_INFO_PATH.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Disease database not found.")

    with open(DISEASE_INFO_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    crop_matches = {}
    target_crop = crop_name.lower().replace("_", " ")

    for class_id, info in data.get("classes", {}).items():
        if target_crop in info.get("crop", "").lower():
            crop_matches[class_id] = info

    if not crop_matches:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No diseases found for crop '{crop_name}'."
        )

    return {"crop": crop_name, "diseases": crop_matches}
