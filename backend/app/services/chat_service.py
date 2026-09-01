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

        if "blight" in msg_lower or "spot" in msg_lower or (context_disease and "blight" in context_disease.lower()):
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

        elif "soil" in msg_lower and ("crack" in msg_lower or "dry" in msg_lower or "crust" in msg_lower):
            response_text = (
                "### Mitigating Soil Surface Cracking and Dry Crusting\n\n"
                "Surface cracking occurs when clay-rich topsoil dries rapidly after wetting, shrinking and tearing soil aggregates apart.\n\n"
                "**Recommended Action Steps:**\n"
                "1. **Depth Check:** Test soil moisture 5–10 cm below the surface. Topsoil cracks do not always mean root-zone depletion.\n"
                "2. **Slow, Deep Irrigation:** Avoid torrential watering which washes silt into cracks. Use slow drip lines or oscillating emitters.\n"
                "3. **Mulching Shield:** Apply a 5–8 cm layer of straw, woodchips, or dry leaf mulch. Mulch shields soil from direct solar radiation and eliminates surface crusting.\n"
                "4. **Organic Matter:** In between cropping cycles, incorporate compost or well-rotted farmyard manure to improve aggregate stability and water-holding capacity."
            )
            suggested_actions = [
                "Apply 5-8 cm organic mulch",
                "Perform finger moisture probe test",
                "Add compost during next bed preparation",
            ]
            related_topics = ["Mulch Selection", "Soil Water Holding Capacity", "Cover Crops"]

        elif "fertilizer" in msg_lower or "npk" in msg_lower or "nitrogen" in msg_lower:
            response_text = (
                "### Agricultural Soil Fertility & Balanced Nutrient Principles\n\n"
                "Optimal crop productivity relies on balanced macronutrients (**N-P-K**):\n\n"
                "- **Nitrogen (N):** Drives vegetative shoot and leaf growth. Deficiency shows as generalized yellowing (chlorosis) of older lower leaves.\n"
                "- **Phosphorus (P):** Crucial for early root elongation and flowering. Deficiency manifests as purplish discoloration on leaf undersides.\n"
                "- **Potassium (K):** Regulates stomatal water movement and disease resistance. Deficiency causes marginal leaf scorch.\n\n"
                "> **Agronomic Best Practice:** Always obtain an accredited soil laboratory test before applying high concentrations of chemical fertilizers. Over-application can cause salt toxicity and groundwater leaching."
            )
            suggested_actions = [
                "Send soil core samples for lab analysis",
                "Side-dress with well-rotted compost",
                "Avoid high nitrogen during flowering stage",
            ]
            related_topics = ["Organic Soil Amendments", "Soil pH Correction", "Foliar Micronutrient Feeds"]

        elif "prevent" in msg_lower or "organic" in msg_lower or "pest" in msg_lower:
            response_text = (
                "### Integrated Pest & Disease Prevention (IPM)\n\n"
                "**1. Crop Rotation:** Rotate plant families (e.g. Solanaceae -> Fabaceae -> Brassicaceae) on a 3-year cycle to break soil-borne disease life cycles.\n"
                "**2. Airflow & Trellising:** Prune excess suckers and stake crops to maximize sun penetration and breeze, which dries leaves fast.\n"
                "**3. Beneficial Insects:** Plant companion flowers (marigolds, sweet alyssum, dill) to attract hoverflies, lacewings, and predatory wasps.\n"
                "**4. Weekly Scouting:** Check leaf undersides and stems once a week for early pest colonies or fungal spots before outbreaks spread."
            )
            suggested_actions = [
                "Map 3-year crop rotation schedule",
                "Install stakes/trellises for upright growth",
                "Introduce companion insectary flowering plants",
            ]
            related_topics = ["Companion Planting", "Crop Rotation Charts", "Biological Pest Controls"]

        else:
            response_text = (
                f"### Agricultural Advisory: {message.strip().capitalize()}\n\n"
                "Maintaining high crop vigor requires an integrated management approach:\n\n"
                "- **Foliage Health:** Regularly inspect leaves for lesions, mold, or discoloration.\n"
                "- **Soil Vitality:** Maintain organic matter with cover crops and compost to support beneficial mycorrhizal fungi.\n"
                "- **Water Management:** Water deeply and infrequently to promote deep root growth rather than shallow, drought-vulnerable roots.\n\n"
                "Feel free to ask specific questions regarding plant disease diagnosis, soil surface cracking, organic pest controls, or fertilization schedules!"
            )
            suggested_actions = [
                "Upload a crop leaf image for disease diagnosis",
                "Upload a soil image for surface moisture inspection",
                "Ask about specific crop care tips",
            ]
            related_topics = ["Plant Disease Scanner", "Soil Moisture Analysis", "Organic Pest Control"]

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

