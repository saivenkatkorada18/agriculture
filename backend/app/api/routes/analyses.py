"""
Analysis History Endpoints
"""
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, status, Query

from backend.app.database.db import db_manager
from backend.app.schemas.analysis import AnalysisHistorySummary

router = APIRouter(prefix="/analyses", tags=["Analysis History"])


@router.get(
    "",
    response_model=List[AnalysisHistorySummary],
    summary="List Analysis Records",
    description="Retrieves a list of previous plant and soil analyses with optional filtering by type, status, and text search."
)
async def list_analyses(
    analysis_type: Optional[str] = Query(None, description="Filter by 'plant_disease' or 'soil_surface'"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status (e.g. Healthy, Disease)"),
    search: Optional[str] = Query(None, alias="q", description="Search by crop, disease, or title"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    results = db_manager.list_analyses(
        analysis_type=analysis_type,
        status=status_filter,
        query=search,
        limit=limit,
        offset=offset,
    )
    return results


@router.get(
    "/stats/summary",
    summary="Get Dashboard Statistics",
    description="Returns aggregate counts of total analyses, healthy plants, diseases detected, and soil scans."
)
async def get_dashboard_stats() -> Dict[str, Any]:
    return db_manager.get_stats()


@router.get(
    "/{analysis_id}",
    summary="Get Analysis Details",
    description="Retrieves complete JSON details of a single analysis by its unique ID."
)
async def get_analysis_detail(analysis_id: str):
    record = db_manager.get_analysis_by_id(analysis_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis with ID '{analysis_id}' was not found."
        )
    return record


@router.delete(
    "/{analysis_id}",
    summary="Delete Analysis Record",
    description="Removes an analysis record from the database."
)
async def delete_analysis_record(analysis_id: str):
    success = db_manager.delete_analysis(analysis_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis with ID '{analysis_id}' was not found or could not be deleted."
        )
    return {"status": "success", "message": f"Analysis {analysis_id} deleted successfully."}
