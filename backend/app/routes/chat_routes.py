from fastapi import APIRouter
from pydantic import BaseModel

from app.core.brain import process_command
from app.modules.voice.speak import speak_text

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    speak: bool = False  # optionally speak the response aloud

@router.post("/")
def chat_with_friday(request: ChatRequest):
    response = process_command(request.message)

    if request.speak:
        speak_text(response)

    return {
        "user_input": request.message,
        "friday_response": response
    }