"""
Pydantic Schemas for System Health
"""
from typing import Dict, Any, List
from pydantic import BaseModel


class SystemHealthResponse(BaseModel):
    status: str
    version: str
    environment: str
    ml_engine: Dict[str, Any]
    database: Dict[str, Any]
    supported_classes_count: int
    uptime_seconds: float
