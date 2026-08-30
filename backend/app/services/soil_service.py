"""
Soil Surface Visual Analysis Service
"""
import uuid
from datetime import datetime, timezone
from typing import Dict, Any

from backend.app.ml.soil_analyzer import SoilSurfaceAnalyzer
from backend.app.services.storage_service import storage_service
from backend.app.database.db import db_manager


class SoilAnalysisService:
    def __init__(self):
        self.analyzer = SoilSurfaceAnalyzer()

    def process_and_analyze(self, image_bytes: bytes, filename: str = "soil.jpg") -> Dict[str, Any]:
        """
        Coordinates storage, OpenCV visual soil surface inspection, and database saving.
        """
        image_url, _ = storage_service.save_upload_bytes(image_bytes, filename)

        raw_result = self.analyzer.analyze(image_bytes)

        analysis_id = str(uuid.uuid4())
        created_at = datetime.now(timezone.utc).isoformat()

        complete_result = {
            "id": analysis_id,
            "image_url": image_url,
            "created_at": created_at,
            **raw_result,
        }

        db_manager.save_analysis(complete_result)

        return complete_result


soil_service = SoilAnalysisService()
