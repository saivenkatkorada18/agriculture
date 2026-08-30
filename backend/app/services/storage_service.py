"""
Storage Service for Image Uploads and Sample Assets
"""
import uuid
import shutil
from pathlib import Path
from typing import Tuple
from PIL import Image

from backend.app.config import UPLOAD_DIR, SAMPLE_DIR


class StorageService:
    """Handles local/cloud saving of image assets."""

    @staticmethod
    def save_upload_bytes(image_bytes: bytes, original_filename: str = "upload.jpg") -> Tuple[str, Path]:
        """
        Saves raw image bytes with unique filename to upload directory.
        Returns (relative_url_path, absolute_file_path).
        """
        ext = Path(original_filename).suffix.lower()
        if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
            ext = ".jpg"

        unique_id = f"img_{uuid.uuid4().hex[:12]}{ext}"
        target_path = UPLOAD_DIR / unique_id

        with open(target_path, "wb") as f:
            f.write(image_bytes)

        url_path = f"/static/uploads/{unique_id}"
        return url_path, target_path


storage_service = StorageService()
