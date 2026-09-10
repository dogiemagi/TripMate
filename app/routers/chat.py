from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from app.services.chat_service import get_chat_response, generate_chat_masterplan

router = APIRouter(prefix="/api/v1/chat", tags=["AI Chat Planning"])


class ChatMessage(BaseModel):
    role: str = Field(..., example="user")
    content: str = Field(..., example="Plan a 7-day Japan trip for 2 people with ₹2L budget")


class ChatRequest(BaseModel):
    messages: List[ChatMessage] = Field(..., description="Conversation history")
    destination: Optional[str] = Field(default="", description="Current destination context")


class ChatResponse(BaseModel):
    reply: str
    status: str = "ok"
    plan: Optional[Dict[str, Any]] = None


class ChatPlanRequest(BaseModel):
    destination: str = Field(..., example="Bali")
    days: Optional[int] = Field(default=7, example=7)
    party: Optional[str] = Field(default="Couple", example="Couple")
    budget: Optional[str] = Field(default="Balanced", example="Balanced")


@router.post("/message", response_model=ChatResponse)
async def chat_message(request: ChatRequest):
    """
    AI Travel Planning Chat endpoint.
    Accepts conversation history and returns an AI-generated travel planning response with synchronized plan.
    """
    messages = [{"role": m.role, "content": m.content} for m in request.messages]
    reply, plan = await get_chat_response(messages, destination=request.destination or "")
    return ChatResponse(reply=reply, status="ok", plan=plan)


@router.post("/plan")
async def chat_plan(request: ChatPlanRequest) -> Dict[str, Any]:
    """
    Generate structured Masterplan for the Tarzan Way chat experience.
    Returns geocoded map coordinates, numbered stop pins, route polyline path, and timeline.
    """
    plan = await generate_chat_masterplan(
        destination=request.destination,
        days=request.days or 7,
        party=request.party or "Couple",
        budget=request.budget or "Balanced"
    )
    return {
        "status": "success",
        "plan": plan
    }
