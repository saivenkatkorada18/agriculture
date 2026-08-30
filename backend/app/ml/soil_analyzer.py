"""
Soil Surface Visual Analysis Engine (OpenCV & Computer Vision)
-------------------------------------------------------------
Performs visual surface inspection on soil images:
- Apparent Moisture Estimation (HSV / LAB color darkness & saturation)
- Surface Cracking Detection (Canny edges, contours, fissure density)
- Dominant Soil Color Categorization (K-Means / Color space mapping)
- Surface Organic Residue & Vegetation Cover (ExG index)
- Soil Texture & Clodiness Roughness Index (Laplacian variance)

IMPORTANT:
This module provides visual surface indicators only. It does NOT
measure laboratory chemical properties (NPK, pH, heavy metals, exact moisture %).
"""
from typing import Dict, Any, List, Tuple
import numpy as np
import cv2
from PIL import Image

from ml.preprocessing.image_preprocessor import load_image_as_rgb_array


class SoilSurfaceAnalyzer:
    """Computer vision analysis for agricultural soil surfaces."""

    def __init__(self):
        self.disclaimer = (
            "This soil surface analysis is an optical estimate based on visible surface characteristics "
            "(color, cracking, apparent moisture, and residue). It does not replace laboratory chemical "
            "soil testing (NPK, pH, micronutrients, or calibrated electrical moisture probes)."
        )

    def analyze(self, image_input: Any) -> Dict[str, Any]:
        """
        Executes full visual soil surface inspection.
        """
        rgb = load_image_as_rgb_array(image_input)
        # Resize standard analysis canvas for deterministic metric computation
        analysis_canvas = cv2.resize(rgb, (400, 400), interpolation=cv2.INTER_AREA)

        # 1. Moisture & Darkness Analysis
        moisture_data = self._analyze_apparent_moisture(analysis_canvas)

        # 2. Surface Cracking & Fissures
        cracking_data = self._detect_surface_cracking(analysis_canvas)

        # 3. Color Classification
        color_data = self._classify_soil_color(analysis_canvas)

        # 4. Organic Matter & Residue Cover
        residue_data = self._analyze_organic_residue(analysis_canvas)

        # 5. Surface Texture & Roughness
        texture_data = self._analyze_surface_texture(analysis_canvas)

        # 6. Synthesize Health Recommendations
        recommendations = self._generate_soil_recommendations(
            moisture_level=moisture_data["moisture_level"],
            cracking_detected=cracking_data["cracking_detected"],
            crack_density_pct=cracking_data["crack_density_pct"],
            color_category=color_data["category"],
            residue_level=residue_data["residue_level"],
            roughness_level=texture_data["roughness_level"],
        )

        overall_status = "Optimal Surface Condition"
        if cracking_data["cracking_detected"] and moisture_data["moisture_level"] in ["Very Low (Dry)", "Low"]:
            overall_status = "Dry / Crusting Detected"
        elif moisture_data["moisture_level"] == "Saturated (Waterlogged)":
            overall_status = "High Moisture / Possible Waterlogging"
        elif cracking_data["cracking_detected"]:
            overall_status = "Surface Fissures Present"

        return {
            "analysis_type": "soil_surface",
            "overall_surface_condition": overall_status,
            "apparent_moisture": moisture_data,
            "surface_cracking": cracking_data,
            "soil_color": color_data,
            "organic_residue": residue_data,
            "surface_texture": texture_data,
            "recommendations": recommendations,
            "disclaimer": self.disclaimer,
            "is_lab_test": False,
        }

    def _analyze_apparent_moisture(self, rgb: np.ndarray) -> Dict[str, Any]:
        """
        Estimates visual moisture from HSV Value (brightness) and Saturation.
        Moist/wet soil reflects darker values (lower V) with richer tones.
        """
        hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
        v_channel = hsv[:, :, 2]
        s_channel = hsv[:, :, 1]

        mean_v = float(np.mean(v_channel))
        mean_s = float(np.mean(s_channel))

        # Moisture index: lower brightness + moderate-to-high saturation correlates with dampness
        # Scaled from 0 (very dry/pale) to 100 (saturated dark)
        moisture_score = np.clip(100.0 - (mean_v * 0.8) + (mean_s * 0.2), 0.0, 100.0)

        if moisture_score < 25:
            level = "Very Low (Dry)"
            desc = "Surface appears dry and pale, indicating potential topsoil dehydration."
        elif moisture_score < 50:
            level = "Low"
            desc = "Surface exhibits low moisture reflectivity with light coloration."
        elif moisture_score < 75:
            level = "Moderate (Moist)"
            desc = "Surface shows healthy dark damp coloration consistent with adequate topsoil moisture."
        else:
            level = "Saturated (Waterlogged)"
            desc = "Surface shows very dark, glossy or wet reflections, indicating high surface water content."

        return {
            "moisture_score": round(float(moisture_score), 1),
            "moisture_level": level,
            "description": desc,
            "mean_brightness_value": round(mean_v, 1),
        }

    def _detect_surface_cracking(self, rgb: np.ndarray) -> Dict[str, Any]:
        """
        Detects fissure networks and shrinkage cracks via edge and morphological contour analysis.
        """
        gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
        blurred = cv2.bilateralFilter(gray, 9, 75, 75)

        # Adaptive thresholding to isolate dark fissure lines
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 4
        )

        # Morphological closing to join continuous fissure paths
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        # Canny edge detector for boundary confirmation
        edges = cv2.Canny(blurred, 40, 120)
        crack_mask = cv2.bitwise_and(closed, edges)

        # Calculate crack pixel ratio
        total_pixels = rgb.shape[0] * rgb.shape[1]
        crack_pixels = np.count_nonzero(crack_mask)
        crack_density_pct = (crack_pixels / total_pixels) * 100.0

        # Find contours of crack networks
        contours, _ = cv2.findContours(crack_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        significant_cracks = [c for c in contours if cv2.arcLength(c, False) > 25]

        has_cracks = crack_density_pct > 1.2 or len(significant_cracks) >= 3

        if not has_cracks:
            severity = "None Detected"
            notes = "No significant surface fissure patterns or soil shrinkage cracks detected."
        elif crack_density_pct < 4.0:
            severity = "Minor Cracking"
            notes = "Mild surface fissures detected, common in drying clay or unmulched topsoil."
        else:
            severity = "Significant / Severe Cracking"
            notes = "Substantial crack network observed. Indicates severe drying, high clay shrinkage, or soil crusting."

        return {
            "cracking_detected": bool(has_cracks),
            "crack_density_pct": round(float(crack_density_pct), 2),
            "crack_count": len(significant_cracks),
            "severity": severity,
            "description": notes,
        }

    def _classify_soil_color(self, rgb: np.ndarray) -> Dict[str, Any]:
        """
        Extracts dominant color clusters and maps to soil classification archetypes.
        """
        # Average color channels
        mean_r = float(np.mean(rgb[:, :, 0]))
        mean_g = float(np.mean(rgb[:, :, 1]))
        mean_b = float(np.mean(rgb[:, :, 2]))

        # Hex representation
        hex_color = f"#{int(mean_r):02x}{int(mean_g):02x}{int(mean_b):02x}"

        # Color distance heuristic to identify soil color archetype
        if mean_r < 90 and mean_g < 80 and mean_b < 70:
            category = "Dark Humic / Organic-Rich"
            characteristics = "Dark brown or charcoal hue, typical of fertile soil with elevated decomposed organic matter."
        elif mean_r > 130 and mean_r > (mean_g * 1.15) and mean_g > mean_b:
            category = "Reddish / Laterite / Clay"
            characteristics = "Reddish or terracotta tone, suggesting presence of oxidized iron minerals or clay content."
        elif mean_r > 140 and mean_g > 130 and mean_b > 110:
            category = "Pale / Sandy / Silt"
            characteristics = "Light tan or sandy hue, commonly associated with coarse sand, low organic carbon, or sun-bleached silt."
        elif mean_r >= mean_g and mean_g >= mean_b:
            category = "Brown / Loamy Soil"
            characteristics = "Standard warm brown color, characteristic of balanced agricultural loam."
        else:
            category = "Grayish / Mineral Topsoil"
            characteristics = "Muted gray-brown tone, often found in compacted mineral soils or calcareous grounds."

        return {
            "dominant_rgb": [int(mean_r), int(mean_g), int(mean_b)],
            "dominant_hex": hex_color,
            "category": category,
            "characteristics": characteristics,
        }

    def _analyze_organic_residue(self, rgb: np.ndarray) -> Dict[str, Any]:
        """
        Uses Excess Green Index (ExG = 2G - R - B) and color thresholds to estimate
        surface vegetation, mulch, crop residue, or moss coverage.
        """
        r = rgb[:, :, 0].astype(np.float32)
        g = rgb[:, :, 1].astype(np.float32)
        b = rgb[:, :, 2].astype(np.float32)

        # Normalized Excess Green
        exg = (2.0 * g) - r - b
        green_mask = exg > 20.0

        green_coverage_pct = (np.count_nonzero(green_mask) / (rgb.shape[0] * rgb.shape[1])) * 100.0

        if green_coverage_pct < 3.0:
            level = "Bare Soil / Low Residue"
            desc = "Bare topsoil surface with minimal visible vegetation, residue, or mulch coverage."
        elif green_coverage_pct < 15.0:
            level = "Moderate Surface Residue"
            desc = "Visible crop stubble, weeds, or organic mulch fragments on topsoil."
        else:
            level = "High Surface Cover / Vegetation"
            desc = "Substantial vegetation, cover crop, or organic residue covering the ground."

        return {
            "green_coverage_pct": round(float(green_coverage_pct), 1),
            "residue_level": level,
            "description": desc,
        }

    def _analyze_surface_texture(self, rgb: np.ndarray) -> Dict[str, Any]:
        """
        Measures surface roughness, aggregate structure, and clodiness via Laplacian variance.
        """
        gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
        lap_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())

        if lap_var < 80:
            roughness = "Smooth / Fine / Possibly Compacted"
            desc = "Low surface variance indicating very fine, powdery tilth or smooth hard crusting."
        elif lap_var < 350:
            roughness = "Moderate Granular Tilth"
            desc = "Good granular crumb structure and aggregate distribution suitable for seedbed."
        else:
            roughness = "Coarse / Cloddy / Rocky"
            desc = "High surface roughness with visible aggregates, clods, or gravel fragments."

        return {
            "roughness_score": round(lap_var, 1),
            "roughness_level": roughness,
            "description": desc,
        }

    def _generate_soil_recommendations(
        self,
        moisture_level: str,
        cracking_detected: bool,
        crack_density_pct: float,
        color_category: str,
        residue_level: str,
        roughness_level: str,
    ) -> List[Dict[str, str]]:
        """
        Generates actionable, scientifically sound recommendations based on visual indicators.
        """
        recs = []

        # Moisture & Cracking recommendations
        if cracking_detected or "Dry" in moisture_level:
            recs.append({
                "title": "Evaluate Sub-Surface Moisture & Apply Irrigation",
                "category": "Water Management",
                "action": "Check moisture 5-10 cm beneath the surface using a trowel or finger test before irrigating. Apply slow, deep watering to prevent rapid runoff through crack channels."
            })
            recs.append({
                "title": "Apply Organic Mulch to Prevent Surface Crusting",
                "category": "Soil Conservation",
                "action": "Spread a 5-8 cm layer of organic mulch (straw, wood chips, or shredded leaves) to reduce evaporation, moderate soil temperature, and prevent future fissure development."
            })
        elif "Waterlogged" in moisture_level:
            recs.append({
                "title": "Improve Drainage & Avoid Water Ponding",
                "category": "Water Management",
                "action": "Hold off on irrigation. Inspect field drainage slopes or raised beds to prevent anaerobic root conditions and root rot fungal infections."
            })

        # Organic matter recommendations
        if "Pale" in color_category or "Bare" in residue_level:
            recs.append({
                "title": "Incorporate Compost or Organic Amendments",
                "category": "Soil Nutrition",
                "action": "Incorporate well-rotted farmyard manure, compost, or cover crops (e.g., clover, vetch) to boost soil organic carbon, moisture retention, and microbial biodiversity."
            })

        # Texture / Compaction recommendations
        if "Smooth" in roughness_level:
            recs.append({
                "title": "Aerate Topsoil to Relieve Surface Compaction",
                "category": "Tillage & Aeration",
                "action": "Perform light shallow harrowing or fork aeration to break surface crusts, facilitating rainfall infiltration and seedling emergence."
            })

        # General recommendation always included
        recs.append({
            "title": "Perform Routine Laboratory Soil Test",
            "category": "Standard Agronomy",
            "action": "Send composite core samples to an accredited agricultural lab every 2-3 years for precise N-P-K, pH, CEC, and organic matter quantification."
        })

        return recs
