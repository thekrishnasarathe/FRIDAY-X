import json
from typing import Optional, List, Dict, Any
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.core.brain import process_command
from app.core.response_engine import stream_chat_with_agent
from app.modules.voice.speak import speak_text

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    speak: bool = False
    mode: Optional[str] = "assistant"
    history: Optional[List[Dict[str, Any]]] = None


class ChatStreamRequest(BaseModel):
    message: str
    mode: Optional[str] = "assistant"
    history: Optional[List[Dict[str, Any]]] = None


@router.post("")
@router.post("/")
def chat_with_friday(request: ChatRequest):
    response = process_command(request.message)

    if request.speak:
        speak_text(response)

    return {
        "user_input": request.message,
        "friday_response": response
    }


@router.post("/stream")
def chat_stream(request: ChatStreamRequest):
    def event_stream():
        for event in stream_chat_with_agent(request.message, request.history, request.mode or "assistant"):
            yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
