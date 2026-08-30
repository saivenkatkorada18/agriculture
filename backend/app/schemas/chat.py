"""
Pydantic Schemas for AI Farming Assistant
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class ChatMessageRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, description="Farmer or researcher agricultural question")
    session_id: Optional[str] = Field(None, description="Optional conversational session ID")
    context_crop: Optional[str] = Field(None, description="Optional crop context (e.g. Tomato, Corn)")
    context_disease: Optional[str] = Field(None, description="Optional diagnosed disease context")


class ChatMessageResponse(BaseModel):
    session_id: str
    message: str
    role: str = "assistant"
    suggested_actions: List[str] = []
    related_topics: List[str] = []
    disclaimer: str
    created_at: str
