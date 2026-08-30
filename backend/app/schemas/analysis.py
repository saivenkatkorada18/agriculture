"""
Pydantic Schemas for Plant & Soil Image Analysis
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class TopPrediction(BaseModel):
    class_id: str
    crop: str
    disease_name: str
    confidence: float
    is_healthy: bool


class PlantAnalysisResult(BaseModel):
    id: str
    analysis_type: str = "plant_disease"
    image_url: str
    crop: str
    prediction: str
    class_id: str
    confidence: float
    is_healthy: bool
    status: str
    is_low_confidence: bool
    confidence_warning: Optional[str] = None
    scientific_name: str
    severity: str
    symptoms: str
    causes: str
    organic_treatment: List[str]
    chemical_treatment: List[str]
    prevention_tips: List[str]
    top_predictions: List[TopPrediction]
    inference_engine: str
    disclaimer: str
    created_at: str


class SoilMoistureMetrics(BaseModel):
    moisture_score: float
    moisture_level: str
    description: str
    mean_brightness_value: float


class SoilCrackingMetrics(BaseModel):
    cracking_detected: bool
    crack_density_pct: float
    crack_count: int
    severity: str
    description: str


class SoilColorMetrics(BaseModel):
    dominant_rgb: List[int]
    dominant_hex: str
    category: str
    characteristics: str


class SoilResidueMetrics(BaseModel):
    green_coverage_pct: float
    residue_level: str
    description: str


class SoilTextureMetrics(BaseModel):
    roughness_score: float
    roughness_level: str
    description: str


class SoilRecommendation(BaseModel):
    title: str
    category: str
    action: str


class SoilAnalysisResult(BaseModel):
    id: str
    analysis_type: str = "soil_surface"
    image_url: str
    overall_surface_condition: str
    apparent_moisture: SoilMoistureMetrics
    surface_cracking: SoilCrackingMetrics
    soil_color: SoilColorMetrics
    organic_residue: SoilResidueMetrics
    surface_texture: SoilTextureMetrics
    recommendations: List[SoilRecommendation]
    disclaimer: str
    is_lab_test: bool = False
    created_at: str


class AnalysisHistorySummary(BaseModel):
    id: str
    analysis_type: str
    image_url: str
    title: str
    subtitle: str
    status: str
    confidence: Optional[float] = None
    created_at: str


class AnalysisFilterParams(BaseModel):
    analysis_type: Optional[str] = None
    crop: Optional[str] = None
    status: Optional[str] = None
    query: Optional[str] = None
    limit: int = 50
    offset: int = 0
