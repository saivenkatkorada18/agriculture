"""
Unit & Integration Tests for Soil & Crop Health Analyzer API
"""
import io
import pytest
from PIL import Image
from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def create_test_image_bytes(color: tuple = (34, 139, 34), size: tuple = (100, 100), format: str = "JPEG") -> bytes:
    """Helper to generate in-memory synthetic image bytes."""
    img = Image.new("RGB", size, color=color)
    buf = io.BytesIO()
    img.save(buf, format=format)
    return buf.getvalue()


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "Soil & Crop Health Analyzer" in data["name"]


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "ml_engine" in data
    assert data["supported_classes_count"] >= 10


def test_analyze_plant_endpoint():
    # Green image (foliage)
    img_bytes = create_test_image_bytes(color=(40, 160, 40))
    files = {"file": ("leaf.jpg", img_bytes, "image/jpeg")}
    response = client.post("/api/analyze/plant", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["analysis_type"] == "plant_disease"
    assert "prediction" in data
    assert "confidence" in data
    assert "disclaimer" in data
    assert "top_predictions" in data
    assert len(data["top_predictions"]) > 0


def test_analyze_soil_endpoint():
    # Brown/Earth image (soil)
    img_bytes = create_test_image_bytes(color=(120, 80, 50))
    files = {"file": ("soil.jpg", img_bytes, "image/jpeg")}
    response = client.post("/api/analyze/soil", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["analysis_type"] == "soil_surface"
    assert "apparent_moisture" in data
    assert "surface_cracking" in data
    assert "soil_color" in data
    assert "recommendations" in data
    assert data["is_lab_test"] is False


def test_invalid_image_upload():
    # Empty file
    files = {"file": ("empty.jpg", b"", "image/jpeg")}
    response = client.post("/api/analyze/plant", files=files)
    assert response.status_code in [400, 422]

    # Non-image file
    files = {"file": ("script.sh", b"echo 'test'", "text/plain")}
    response = client.post("/api/analyze/plant", files=files)
    assert response.status_code in [400, 422]


def test_chat_assistant_endpoint():
    payload = {"message": "How do I prevent early blight in tomatoes?"}
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "assistant"
    assert "Blight" in data["message"] or "Sanitation" in data["message"]
    assert len(data["suggested_actions"]) > 0
    assert "disclaimer" in data


def test_analyses_history_and_deletion():
    # First create an analysis
    img_bytes = create_test_image_bytes(color=(50, 150, 50))
    files = {"file": ("leaf.jpg", img_bytes, "image/jpeg")}
    post_res = client.post("/api/analyze/plant", files=files)
    assert post_res.status_code == 200
    analysis_id = post_res.json()["id"]

    # Retrieve history list
    list_res = client.get("/api/analyses")
    assert list_res.status_code == 200
    analyses = list_res.json()
    assert any(a["id"] == analysis_id for a in analyses)

    # Retrieve single detail
    detail_res = client.get(f"/api/analyses/{analysis_id}")
    assert detail_res.status_code == 200
    assert detail_res.json()["id"] == analysis_id

    # Retrieve dashboard stats
    stats_res = client.get("/api/analyses/stats/summary")
    assert stats_res.status_code == 200
    assert stats_res.json()["total_analyses"] >= 1

    # Delete record
    del_res = client.delete(f"/api/analyses/{analysis_id}")
    assert del_res.status_code == 200
