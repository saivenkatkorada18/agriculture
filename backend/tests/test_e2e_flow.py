"""
End-to-End System Verification Script
"""
import io
import httpx
from PIL import Image

def run_e2e_verification():
    print("=" * 60)
    print("RUNNING END-TO-END VERIFICATION OF SOIL & CROP HEALTH ANALYZER")
    print("=" * 60)

    client = httpx.Client(base_url="http://127.0.0.1:8000")

    # 1. Health check
    res = client.get("/api/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    health_data = res.json()
    print(f"[OK] Backend Health: {health_data['status']} | Model Mode: {health_data['ml_engine']['inference_mode']}")

    # 2. Plant Disease Analysis
    leaf_img = Image.new("RGB", (224, 224), color=(34, 139, 34))
    buf = io.BytesIO()
    leaf_img.save(buf, format="JPEG")
    leaf_bytes = buf.getvalue()

    res = client.post("/api/analyze/plant", files={"file": ("leaf.jpg", leaf_bytes, "image/jpeg")})
    assert res.status_code == 200, f"Plant analysis failed: {res.text}"
    plant_result = res.json()
    print(f"[OK] Plant Analysis Result: {plant_result['crop']} — {plant_result['prediction']} ({plant_result['confidence']}%)")
    print(f"     Status: {plant_result['status']} | Scientific: {plant_result['scientific_name']}")
    plant_id = plant_result["id"]

    # 3. Soil Surface Analysis
    soil_img = Image.new("RGB", (224, 224), color=(100, 70, 45))
    buf2 = io.BytesIO()
    soil_img.save(buf2, format="JPEG")
    soil_bytes = buf2.getvalue()

    res = client.post("/api/analyze/soil", files={"file": ("soil.jpg", soil_bytes, "image/jpeg")})
    assert res.status_code == 200, f"Soil analysis failed: {res.text}"
    soil_result = res.json()
    print(f"[OK] Soil Analysis Result: {soil_result['overall_surface_condition']}")
    print(f"     Apparent Moisture: {soil_result['apparent_moisture']['moisture_level']} (Score: {soil_result['apparent_moisture']['moisture_score']})")
    print(f"     Cracking Density: {soil_result['surface_cracking']['crack_density_pct']}% ({soil_result['surface_cracking']['severity']})")
    print(f"     Dominant Hue: {soil_result['soil_color']['category']}")
    soil_id = soil_result["id"]

    # 4. AI Farming Assistant Chat
    chat_payload = {
        "message": "How do I prevent Early Blight in tomatoes?",
        "context_crop": "Tomato",
        "context_disease": "Early Blight",
    }
    res = client.post("/api/chat", json=chat_payload)
    assert res.status_code == 200, f"Chat failed: {res.text}"
    chat_result = res.json()
    print(f"[OK] AI Farming Assistant Responded:")
    print(f"     Preview: {chat_result['message'][:120]}...")
    print(f"     Suggested actions: {chat_result['suggested_actions']}")

    # 5. History and Stats
    res = client.get("/api/analyses")
    assert res.status_code == 200
    history = res.json()
    print(f"[OK] History Archives: {len(history)} records retrieved.")

    res = client.get(f"/api/analyses/{plant_id}")
    assert res.status_code == 200
    print(f"[OK] Single Analysis Detail: Successfully retrieved record {plant_id[:8]}")

    res = client.get("/api/analyses/stats/summary")
    assert res.status_code == 200
    stats = res.json()
    print(f"[OK] Dashboard Stats: Total {stats['total_analyses']} scans (Healthy: {stats['healthy_crops']}, Pathologies: {stats['diseases_detected']}, Soil: {stats['soil_analyses']})")

    # 6. Crops Encyclopedia
    res = client.get("/api/crops")
    assert res.status_code == 200
    crops_data = res.json()
    print(f"[OK] Crop Pathology Encyclopedia: {len(crops_data.get('classes', {}))} disease classes registered.")

    # 7. Frontend check
    frontend_res = httpx.get("http://localhost:3000")
    assert frontend_res.status_code == 200
    print(f"[OK] Frontend Web App: Serving live at http://localhost:3000 (HTTP 200)")

    print("\nALL END-TO-END VERIFICATION CHECKS PASSED PERFECTLY!\n")

if __name__ == "__main__":
    run_e2e_verification()
