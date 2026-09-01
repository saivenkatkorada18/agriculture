"""
AI Farming Assistant Service
----------------------------
Provides contextual agronomic guidance on crop health, disease prevention,
soil management, organic treatments, and irrigation best practices.
Integrates Google Gemini AI with fallback to an offline agronomy knowledge base.
"""
import uuid
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
import httpx

from backend.app.config import settings

logger = logging.getLogger(__name__)


class FarmingAssistantService:
    def __init__(self):
        self.disclaimer = (
            "This AI farming assistant provides general agronomic guidance based on established agricultural best practices. "
            "For severe or localized crop failure risks, always verify diagnoses with a certified local agricultural extension officer or agronomist."
        )

    def _call_gemini_api(
        self,
        message: str,
        context_crop: Optional[str] = None,
        context_disease: Optional[str] = None,
    ) -> Optional[str]:
        """Calls Google Gemini 2.5 Flash API for agronomic advice."""
        if not settings.gemini_api_key:
            return None

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={settings.gemini_api_key}"
        
        context_info = ""
        if context_crop:
            context_info += f"\n- Target Crop: {context_crop}"
        if context_disease:
            context_info += f"\n- Identified Condition/Disease: {context_disease}"

        system_instruction = (
            "You are an expert agronomist and AI farming assistant for the Soil & Crop Health Analyzer application. "
            "Provide helpful, practical, structured agronomic advice using clean Markdown (headers, bullet points, bold text). "
            "Cover organic treatments, cultural practices, irrigation, and IPM principles where applicable."
            f"{context_info}\n\nFarmer Question: {message}"
        )

        payload = {
            "contents": [
                {
                    "parts": [{"text": system_instruction}]
                }
            ]
        }

        try:
            with httpx.Client(timeout=10.0) as client:
                resp = client.post(url, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts and "text" in parts[0]:
                            return parts[0]["text"]
                else:
                    logger.warning(f"Gemini API returned status {resp.status_code}: {resp.text}")
        except Exception as exc:
            logger.warning(f"Failed to query Gemini API: {exc}")

        return None

    def answer_query(
        self,
        message: str,
        session_id: Optional[str] = None,
        context_crop: Optional[str] = None,
        context_disease: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generates an agronomic response with actionable steps, related topics, and disclaimers.
        """
        active_session = session_id or str(uuid.uuid4())
        created_at = datetime.now(timezone.utc).isoformat()

        # 1. Attempt Gemini AI Generation
        gemini_response = self._call_gemini_api(message, context_crop, context_disease)
        if gemini_response:
            return {
                "session_id": active_session,
                "message": gemini_response,
                "role": "assistant",
                "suggested_actions": [
                    "Inspect crop leaf symptoms carefully",
                    "Verify irrigation and moisture levels",
                    "Consult local agronomist for persistent issues",
                ],
                "related_topics": ["Agronomic Management", "Soil Moisture", "Integrated Pest Management"],
                "disclaimer": self.disclaimer,
                "created_at": created_at,
            }

        # 2. Knowledge Base Heuristic Engine Fallback
        msg_lower = message.lower()
        suggested_actions: List[str] = []
        related_topics: List[str] = []

        if "season" in msg_lower or "which crop" in msg_lower or "best crop" in msg_lower or "plant" in msg_lower and "good" in msg_lower:
            response_text = (
                "### 🌾 Seasonal Crop Selection & Cultivation Advisory\n\n"
                "Selecting the right crop for the current agricultural season is critical for high yields and disease resistance:\n\n"
                "**1. Monsoon / Kharif Season (June – October):**\n"
                "- **Top Crops:** Rice/Paddy, Maize (Corn), Cotton, Soybean, Groundnut, Pigeon Pea (Arhar).\n"
                "- **Agronomic Tips:** Ensure good field drainage to prevent waterlogging; monitor for fungal leaf spot diseases in humid conditions.\n\n"
                "**2. Winter / Rabi Season (October – March):**\n"
                "- **Top Crops:** Wheat, Mustard, Chickpea (Gram), Barley, Potato, Tomato, Peas.\n"
                "- **Agronomic Tips:** Water deeply during early tillering and flowering stages; scout for rust and powdery mildew.\n\n"
                "**3. Summer / Zaid Season (March – June):**\n"
                "- **Top Crops:** Watermelon, Cucumber, Muskmelon, Okra (Lady Finger), Bitter Gourd, Leafy Greens.\n"
                "- **Agronomic Tips:** Use drip irrigation and organic straw mulch to conserve moisture under intense solar heat."
            )
            suggested_actions = [
                "Test soil pH and moisture before planting",
                "Apply organic compost to seedbeds",
                "Plan 3-year crop rotation schedule",
            ]
            related_topics = ["Kharif Crops", "Rabi Season", "Soil Moisture Testing"]

        elif "blight" in msg_lower or "spot" in msg_lower or (context_disease and "blight" in context_disease.lower()):
            response_text = (
                "### Foliar Blight & Leaf Spot Management Strategy\n\n"
                "**1. Cultural Sanitation:**\n"
                "- Promptly remove and safely bag heavily spotted or necrotic leaves from the lower canopy.\n"
                "- Never compost diseased foliage, as fungal spores (*Alternaria* or *Phytophthora*) can survive home composting temperatures.\n\n"
                "**2. Moisture & Irrigation Controls:**\n"
                "- Avoid overhead sprinkler watering. Convert to drip irrigation or soaker hoses to keep foliage dry.\n"
                "- Water early in the morning so incidental leaf wetness evaporates quickly in the morning sun.\n\n"
                "**3. Organic & Chemical Options:**\n"
                "- *Organic:* Apply copper soap or *Bacillus subtilis* bio-fungicide at 7-10 day intervals during humid weather.\n"
                "- *Conventional:* Protective sprays with chlorothalonil or mancozeb before extended rain events."
            )
            suggested_actions = [
                "Inspect lower leaves for concentric brown rings",
                "Apply organic straw mulch around plant base",
                "Switch to drip or ground-level watering",
            ]
            related_topics = ["Fungicide Rotation", "Crop Spacing", "Drip Irrigation Setup"]

        elif "ph" in msg_lower or "soil" in msg_lower and ("acid" in msg_lower or "alkaline" in msg_lower or "test" in msg_lower):
            response_text = (
                "### 🧪 Soil pH & Nutrient Availability Advisory\n\n"
                "Soil pH directly dictates whether plant roots can absorb essential macronutrients:\n\n"
                "- **Optimal Range:** Most vegetables and agronomic crops thrive in **pH 6.0 – 7.0** (slightly acidic to neutral).\n"
                "- **Acidic Soil (< 6.0):** Restricts phosphorus and calcium availability. Remedy: Apply agricultural lime (calcium carbonate) 2-3 weeks before sowing.\n"
                "- **Alkaline Soil (> 7.5):** Restricts iron, zinc, and manganese. Remedy: Incorporate elemental sulfur or well-rotted organic compost.\n\n"
                "> **Recommendation:** Perform an electrical conductivity (EC) and pH test every season before applying chemical fertilizers."
            )
            suggested_actions = [
                "Measure soil pH with digital probe or lab sample",
                "Add agricultural lime for acidic beds",
                "Incorporate compost to buffer soil pH",
            ]
            related_topics = ["Soil Testing", "Nutrient Deficiencies", "Organic Compost"]

        elif "water" in msg_lower or "irrigation" in msg_lower or "drip" in msg_lower:
            response_text = (
                "### 💧 Water & Irrigation Best Practices\n\n"
                "**1. Morning Irrigation:** Water crops early in the morning (6 AM – 9 AM). Leaf wetness overnight is the #1 catalyst for fungal spore germination.\n"
                "**2. Drip System Advantage:** Drip irrigation delivers water directly to root zones, saving up to 50% more water than overhead sprayers while keeping leaves completely dry.\n"
                "**3. Finger Probe Test:** Insert a finger 5 cm into the topsoil. If dry, irrigate deeply. If moist, hold irrigation to prevent root rot."
            )
            suggested_actions = [
                "Install drip irrigation emitters",
                "Water early in the morning",
                "Mulch beds to retain root moisture",
            ]
            related_topics = ["Drip Irrigation", "Soil Moisture", "Root Rot Prevention"]

        elif "prevent" in msg_lower or "organic" in msg_lower or "pest" in msg_lower:
            response_text = (
                "### 🐛 Integrated Pest & Disease Prevention (IPM)\n\n"
                "**1. Organic Neem Spray:** Apply cold-pressed neem oil (5 ml/L water with mild soap) every 10–14 days to deter aphids, thrips, and whiteflies.\n"
                "**2. Companion Flowers:** Plant French Marigolds and Alyssum alongside crops to attract predatory lacewings, ladybugs, and hoverflies.\n"
                "**3. Yellow Sticky Traps:** Hang yellow sticky cards 15 cm above the crop canopy to monitor flying insect populations early."
            )
            suggested_actions = [
                "Spray neem oil every 10-14 days",
                "Hang yellow sticky pest traps",
                "Plant marigolds around crop borders",
            ]
            related_topics = ["Neem Oil Spray", "Companion Planting", "Insect Trap Cards"]

        else:
            response_text = (
                f"### 🌾 Agronomic Advisory: {message.strip().capitalize()}\n\n"
                "Maintaining optimal crop vitality requires an integrated management approach:\n\n"
                "- **Crop Selection:** Choose high-yielding, disease-resistant varieties adapted to your current season.\n"
                "- **Foliage Inspection:** Scout lower leaves weekly for brown lesions, mildew powder, or pest feeding.\n"
                "- **Soil Health:** Maintain organic matter with compost to buffer soil pH and promote strong root systems.\n\n"
                "Select one of the FAQ options above or ask any specific question about crop choices, diseases, soil pH, or irrigation!"
            )
            suggested_actions = [
                "Ask which crop is best for this season",
                "Upload a crop leaf image for disease scan",
                "Check soil moisture and pH guidelines",
            ]
            related_topics = ["Seasonal Crops", "Disease Scanner", "Organic Treatments"]

        return {
            "session_id": active_session,
            "message": response_text,
            "role": "assistant",
            "suggested_actions": suggested_actions,
            "related_topics": related_topics,
            "disclaimer": self.disclaimer,
            "created_at": created_at,
        }


chat_service = FarmingAssistantService()

