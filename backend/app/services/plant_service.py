"""
Plant Disease Service
"""
import uuid
from datetime import datetime, timezone
from typing import Dict, Any

from backend.app.ml.plant_classifier import PlantDiseaseClassifier
from backend.app.services.storage_service import storage_service
from backend.app.database.db import db_manager


class PlantAnalysisService:
    def __init__(self):
        self.classifier = PlantDiseaseClassifier()

    def process_and_analyze(self, image_bytes: bytes, filename: str = "leaf.jpg") -> Dict[str, Any]:
        """
        Coordinates storage, ML classification, and persistence.
        """
        # Save image file
        image_url, _ = storage_service.save_upload_bytes(image_bytes, filename)

        # Run prediction
        raw_result = self.classifier.predict(image_bytes)

        # Attach identifiers and timestamp
        analysis_id = str(uuid.uuid4())
        created_at = datetime.now(timezone.utc).isoformat()

        complete_result = {
            "id": analysis_id,
            "image_url": image_url,
            "created_at": created_at,
            **raw_result,
        }

        # Persist to database
        db_manager.save_analysis(complete_result)

        return complete_result


plant_service = PlantAnalysisService()
