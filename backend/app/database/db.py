"""
Database Interface & Storage Adapter
------------------------------------
Provides unified database persistence supporting both Supabase PostgreSQL
and zero-config SQLite local development mode.
"""
import sqlite3
import json
import uuid
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional
import httpx

from backend.app.config import settings, DATA_DIR

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages analysis persistence and history records across Supabase and SQLite."""

    def __init__(self):
        self.db_path = DATA_DIR / "app.db"
        self._init_sqlite()

    @property
    def supabase_enabled(self) -> bool:
        return bool(settings.supabase_url and (settings.supabase_anon_key or settings.supabase_service_key))

    def _get_supabase_headers(self) -> Dict[str, str]:
        key = settings.supabase_service_key or settings.supabase_anon_key
        return {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation",
        }

    def _init_sqlite(self):
        """Initializes SQLite tables if not existing."""
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analyses (
                    id TEXT PRIMARY KEY,
                    user_id TEXT DEFAULT 'demo-farmer-user',
                    analysis_type TEXT NOT NULL,
                    image_url TEXT NOT NULL,
                    title TEXT NOT NULL,
                    subtitle TEXT,
                    prediction TEXT,
                    confidence REAL,
                    status TEXT NOT NULL,
                    result_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_analyses_type ON analyses(analysis_type);
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_analyses_created ON analyses(created_at);
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_sessions (
                    id TEXT PRIMARY KEY,
                    user_id TEXT DEFAULT 'demo-farmer-user',
                    created_at TEXT NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_messages (
                    id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    message TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (session_id) REFERENCES chat_sessions(id) ON DELETE CASCADE
                )
            """)
            conn.commit()

    def save_analysis(self, analysis_data: Dict[str, Any]) -> str:
        """Saves a plant or soil analysis result to SQLite and Supabase (if available)."""
        analysis_id = analysis_data.get("id") or str(uuid.uuid4())
        analysis_type = analysis_data.get("analysis_type", "plant_disease")
        created_at = analysis_data.get("created_at") or datetime.now(timezone.utc).isoformat()
        image_url = analysis_data.get("image_url", "")

        if analysis_type == "plant_disease":
            title = f"{analysis_data.get('crop', 'Crop')} — {analysis_data.get('prediction', 'Diagnosis')}"
            subtitle = f"Confidence: {analysis_data.get('confidence', 0)}%"
            prediction = analysis_data.get("prediction", "")
            confidence = float(analysis_data.get("confidence", 0))
            status = analysis_data.get("status", "Analyzed")
        else:
            title = f"Soil Surface: {analysis_data.get('overall_surface_condition', 'Inspected')}"
            moisture = analysis_data.get("apparent_moisture", {}).get("moisture_level", "Unknown")
            subtitle = f"Apparent Moisture: {moisture}"
            prediction = analysis_data.get("overall_surface_condition", "")
            confidence = None
            status = analysis_data.get("overall_surface_condition", "Analyzed")

        result_json_str = json.dumps(analysis_data)

        # 1. Save to local SQLite
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO analyses 
                (id, user_id, analysis_type, image_url, title, subtitle, prediction, confidence, status, result_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                analysis_id,
                "demo-farmer-user",
                analysis_type,
                image_url,
                title,
                subtitle,
                prediction,
                confidence,
                status,
                result_json_str,
                created_at,
            ))
            conn.commit()

        # 2. Sync to Supabase if configured
        if self.supabase_enabled:
            try:
                supabase_payload = {
                    "id": analysis_id,
                    "analysis_type": analysis_type,
                    "image_url": image_url,
                    "title": title,
                    "subtitle": subtitle,
                    "prediction": prediction,
                    "confidence": confidence,
                    "status": status,
                    "result_json": analysis_data,
                    "created_at": created_at,
                }
                url = f"{settings.supabase_url.rstrip('/')}/rest/v1/analyses"
                with httpx.Client(timeout=5.0) as client:
                    resp = client.post(url, json=supabase_payload, headers=self._get_supabase_headers())
                    if resp.status_code not in (200, 201):
                        logger.warning(f"Supabase sync returned status {resp.status_code}: {resp.text}")
            except Exception as exc:
                logger.warning(f"Could not sync analysis record to Supabase: {exc}")

        return analysis_id

    def get_analysis_by_id(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves raw analysis record by ID from Supabase or SQLite fallback."""
        if self.supabase_enabled:
            try:
                url = f"{settings.supabase_url.rstrip('/')}/rest/v1/analyses?id=eq.{analysis_id}&select=result_json"
                with httpx.Client(timeout=5.0) as client:
                    resp = client.get(url, headers=self._get_supabase_headers())
                    if resp.status_code == 200:
                        data = resp.json()
                        if data and len(data) > 0 and "result_json" in data[0]:
                            res = data[0]["result_json"]
                            return res if isinstance(res, dict) else json.loads(res)
            except Exception as exc:
                logger.warning(f"Supabase read failed for ID {analysis_id}: {exc}")

        # Fallback to local SQLite
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT result_json FROM analyses WHERE id = ?", (analysis_id,))
            row = cursor.fetchone()
            if row:
                return json.loads(row["result_json"])
        return None

    def list_analyses(
        self,
        analysis_type: Optional[str] = None,
        status: Optional[str] = None,
        query: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """Lists analysis summaries with filtering."""
        if self.supabase_enabled:
            try:
                url = f"{settings.supabase_url.rstrip('/')}/rest/v1/analyses?select=id,analysis_type,image_url,title,subtitle,status,confidence,created_at&order=created_at.desc&limit={limit}&offset={offset}"
                if analysis_type and analysis_type != "all":
                    url += f"&analysis_type=eq.{analysis_type}"
                with httpx.Client(timeout=5.0) as client:
                    resp = client.get(url, headers=self._get_supabase_headers())
                    if resp.status_code == 200:
                        return resp.json()
            except Exception as exc:
                logger.warning(f"Supabase list_analyses failed, falling back to SQLite: {exc}")

        # Fallback to local SQLite
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            query_sql = "SELECT id, analysis_type, image_url, title, subtitle, status, confidence, created_at FROM analyses WHERE 1=1"
            params: List[Any] = []

            if analysis_type and analysis_type != "all":
                query_sql += " AND analysis_type = ?"
                params.append(analysis_type)

            if status and status != "all":
                query_sql += " AND status LIKE ?"
                params.append(f"%{status}%")

            if query:
                query_sql += " AND (title LIKE ? OR subtitle LIKE ? OR prediction LIKE ?)"
                params.extend([f"%{query}%", f"%{query}%", f"%{query}%"])

            query_sql += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
            params.extend([limit, offset])

            cursor.execute(query_sql, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def delete_analysis(self, analysis_id: str) -> bool:
        """Deletes an analysis record."""
        if self.supabase_enabled:
            try:
                url = f"{settings.supabase_url.rstrip('/')}/rest/v1/analyses?id=eq.{analysis_id}"
                with httpx.Client(timeout=5.0) as client:
                    client.delete(url, headers=self._get_supabase_headers())
            except Exception as exc:
                logger.warning(f"Supabase delete failed for ID {analysis_id}: {exc}")

        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM analyses WHERE id = ?", (analysis_id,))
            conn.commit()
            return cursor.rowcount > 0

    def get_stats(self) -> Dict[str, Any]:
        """Calculates dashboard analytics."""
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM analyses")
            total = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM analyses WHERE analysis_type = 'plant_disease' AND status = 'Healthy Crop'")
            healthy = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM analyses WHERE analysis_type = 'plant_disease' AND status = 'Disease Detected'")
            diseased = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM analyses WHERE analysis_type = 'soil_surface'")
            soil_scans = cursor.fetchone()[0]

            return {
                "total_analyses": total,
                "healthy_crops": healthy,
                "diseases_detected": diseased,
                "soil_analyses": soil_scans,
            }


db_manager = DatabaseManager()

