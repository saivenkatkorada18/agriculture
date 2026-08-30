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
