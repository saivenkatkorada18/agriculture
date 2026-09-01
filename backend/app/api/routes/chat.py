"""
AI Farming Assistant Chat Endpoints
"""
from fastapi import APIRouter, HTTPException, status
from backend.app.schemas.chat import ChatMessageRequest, ChatMessageResponse
from backend.app.services.chat_service import chat_service

router = APIRouter(prefix="/chat", tags=["AI Farming Assistant"])


@router.post(
    "",
    response_model=ChatMessageResponse,
    summary="Ask the AI Farming Assistant",
    description="Provides agronomic answers, disease mitigation steps, irrigation principles, and fertilizer guidance with safety disclaimers."
)
async def ask_farming_assistant(request: ChatMessageRequest):
    if not request.message or not request.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message content cannot be empty."
        )

    response = chat_service.answer_query(
        message=request.message,
        session_id=request.session_id,
        context_crop=request.context_crop,
        context_disease=request.context_disease,
    )
    return response


# ── Google Gemini Live & ElevenLabs Voice Assistant Endpoint ────────────────
import base64
import json
import os
import re
import urllib.request
from fastapi.responses import JSONResponse

@router.post("/voice", summary="Voice Assistant Endpoint (Gemini 2.0 Live & ElevenLabs)")
async def voice_assistant_endpoint(payload: dict):
    prompt = payload.get("prompt", "").strip()
    gemini_key = payload.get("gemini_api_key", "").strip() or os.getenv("GEMINI_API_KEY", "")
    eleven_key = payload.get("eleven_api_key", "").strip() or os.getenv("ELEVENLABS_API_KEY", "")
    voice_id = payload.get("voice_id", "").strip() or "21m00Tcm4TlvDq8ikWAM"

    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt text cannot be empty.")

    ai_text = None
    engine = "gemini-2.0-flash"

    if gemini_key:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={gemini_key}"
            headers = {"Content-Type": "application/json"}
            body = json.dumps({
                "system_instruction": {
                    "parts": [{
                        "text": "You are AgriGenius AI, an expert voice agronomist assistant. You speak warmly, concisely, and naturally to farmers and growers. Answer crop disease, soil, irrigation, pest control, and farming questions in 2-3 helpful sentences suitable for voice speech output."
                    }]
                },
                "contents": [{
                    "role": "user",
                    "parts": [{"text": prompt}]
                }]
            }).encode('utf-8')

            req = urllib.request.Request(url, data=body, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=12) as resp:
                if resp.status == 200:
                    res_data = json.loads(resp.read().decode('utf-8'))
                    candidates = res_data.get("candidates", [])
                    if candidates and "content" in candidates[0]:
                        parts = candidates[0]["content"].get("parts", [])
                        if parts:
                            ai_text = parts[0].get("text", "")
        except Exception as err:
            pass

    if not ai_text:
        resp = chat_service.answer_query(message=prompt)
        ai_text = resp.reply if hasattr(resp, 'reply') else str(resp)
        engine = "agronomy_service"

    plain_text = re.sub(r'<[^>]*>', '', ai_text)
    audio_b64 = None

    if eleven_key:
        try:
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": eleven_key
            }
            body = json.dumps({
                "text": plain_text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75
                }
            }).encode('utf-8')

            req = urllib.request.Request(url, data=body, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=12) as resp:
                if resp.status == 200:
                    audio_bytes = resp.read()
                    audio_b64 = base64.b64encode(audio_bytes).decode('utf-8')
                    engine = f"{engine}+elevenlabs"
        except Exception:
            pass

    return JSONResponse(content={
        "text": ai_text,
        "audio_b64": audio_b64,
        "engine": engine
    })

