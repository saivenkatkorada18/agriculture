"""
Backend Configuration & Settings
"""
import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel, field_validator

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

BACKEND_DIR = BASE_DIR / "backend"
DATA_DIR = BACKEND_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
SAMPLE_DIR = BACKEND_DIR / "app" / "static" / "samples"

DATA_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
SAMPLE_DIR.mkdir(parents=True, exist_ok=True)


class Settings(BaseModel):
    app_name: str = "Soil & Crop Health Analyzer API"
    app_version: str = "1.0.0"
    app_env: str = os.getenv("APP_ENV", "development")
    api_prefix: str = "/api"
    
    # Security & CORS
    secret_key: str = os.getenv("SECRET_KEY", "")
    allowed_origins: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
    ]
    
    # Database / Supabase
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_anon_key: str = os.getenv("SUPABASE_ANON_KEY", "")
    supabase_service_key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    database_url: str = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR / 'app.db'}")
    
    # ML & AI Configuration
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    max_upload_size_bytes: int = 10 * 1024 * 1024  # 10MB
    confidence_threshold: float = 0.60
    model_path: str = os.getenv("MODEL_PATH", str(BASE_DIR / "ml" / "models" / "plant_disease_mobilenetv2.h5"))
    use_demo_fallback: bool = os.getenv("USE_DEMO_FALLBACK", "true").lower() == "true"


settings = Settings()
